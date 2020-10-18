import random
import math
from .field import FieldElement
from .protocol_data import ProtocolData
from .merkle import MerkleTree
from .fri import Fri, reverseOrder, reverse_int, create_fri_op
from .polynomial import Poly, interpolate_poly
from . import polynomial
from .hash_chain import HashChainWriter, HashChainReader
from typing import List, Tuple, Dict, Any


def compute_Fib(firstElement: int = 1, secondElement: int = 2, total: int = 1000):
    a_1 = FieldElement(firstElement)
    a_2 = FieldElement(secondElement)

    L = [a_1, a_2]
    for i in range(total - 2):
        L.append(L[-2]**2 + L[-1]**2)
    return L


def create_pol_traces(xi, sequence: List[FieldElement]) -> List[Tuple[Poly, int]]:
    seq_len = len(sequence)
    temp = 1
    x_values: List[int] = []
    for _ in sequence:
        x_values.append(temp)
        temp *= xi
    pol = interpolate_poly(x_values, sequence)  # has degree <=seq_len-1

    # condition on the polynomial.

    '''
    pol(xi**(k+2)) = pol(xi**k)**2 + pol(xi**(k+1))**2 for k=0,...,n-3   (deg<=2n)
    equi
    f_0(x) = pol(x*(xi**2)) - pol(x)**2 + pol(x*xi)**2 == 0 for x=xi**k , k=0,...,n-3
    equi

    h_0 = f_0(x) * (x-xi**(n-2))*(x-xi**(n-1)) / (x**n-1) is a polynomial of degree <= 2n - (n-2) = n + 2

    h_1 = (pol(x)-1)/(x-xi) poly of degree <= n-1
    h_2 = (pol(x)-pol(xi**(n-1)) )/(x-xi**(n-1)) poly of degree <= n-1
    '''

    X = polynomial.X

    # Fibonacci condition
    # f_0(x)=0 for x=xi**k, k=0,...,seq_len-3
    f_0 = (pol(X * xi * xi) - ((pol**2) + (pol(X * xi)**2)))       # deg(f_0) <= 2*(seq_len-1)
    # complete it to have 0 on xi**k for k<= power of two
    deg = int(2**math.ceil(math.log2(seq_len - 2)))
    f_temp = f_0
    root = xi**(seq_len - 2)
    for k in range(seq_len - 2, deg):
        f_temp *= (X - root)
        root *= xi

    h_0 = f_temp // (X**deg - 1)                                    # deg(h_0) <= seq_len
    # Boundary conditions:
    h_1 = (pol - sequence[0]) // (X - 1)                            # deg(h_1) <= seq_len-2
    h_2 = (pol - sequence[-1]) // (X - xi**(seq_len - 1))           # deg(h_2) <= seq_len-2
    return [(h_0, seq_len), (h_1, seq_len - 2), (h_2, seq_len - 2)]


def create_coefficients(randomizer, k):
    return [(randomizer.randN(), randomizer.randN()) for _ in range(k)]


def composition(polynomials, coef, total_deg: int):
    H = sum(c1 * f + c2 * Poly.monomial(total_deg - d) * f
            for (f, d), (c1, c2) in zip(polynomials, coef))
    # H = randN() * h_0 + randN() * h_1 + randN() * h_2 + X * X * (randN() * h_1 + randN() * h_2)
    return H


def set_merkle_element(name: str, tree: MerkleTree, index: int, hash_chain: HashChainWriter):
    hash_chain[name] = list(tree.reveal_path(index))


def set_merkle_elements(
        name: str, trees: List[MerkleTree], index: int, hash_chain: HashChainWriter):
    hash_chain[name] = [list(tree.reveal_path(index)) for tree in trees]


def create_proof(
        pro_data: ProtocolData, firstElement, secondElement) -> Dict[str, Any]:

    print('\n-------------------------- Starting the prover --------------------------')

    print(' === Computing Fibonacci and condition polynomials')

    total = pro_data.fib_sequence_length + 1
    # Compute Fibonacci
    fib_trace = compute_Fib(firstElement=1, secondElement=2, total=pro_data.fib_sequence_length)
    # verifier_data.update({'first': 1, 'second': fib_trace[-1], 'total': total - 1})
    hash_chain = HashChainWriter()
    hash_chain['first'] = firstElement
    hash_chain['second'] = secondElement
    hash_chain['last'] = fib_trace[-1]

    print(' === Computing condition polynomials')
    # Create the condition polynomials
    polynomials = create_pol_traces(pro_data.xi, fib_trace)
    print(' === Creating merkle trees for polynomials')
    polynomials_merkle_tress = [MerkleTree(f.fast_eval(pro_data.xi, pro_data.xi_order, pro_data.coset))
                                for f, d in polynomials]
    polynomials_merkle_roots = [tree.root for tree in polynomials_merkle_tress]
    hash_chain['pol_merkle_roots'] = polynomials_merkle_roots

    deg = max(d for _, d in polynomials)
    # print(f'max is {deg}')
    # for f, d in polynomials:
    #     print(d)
    #     print(f)
    deg_power = math.ceil(math.log2(deg))
    deg = 1 << deg_power
    hash_chain['deg'] = deg

    num_poly = len(polynomials)
    hash_chain['num_poly'] = num_poly

    print(' === Creating composition polynomial')

    # Create the composition polynomial
    coef = create_coefficients(hash_chain, num_poly)
    H = composition(polynomials, coef, deg)
    H_merkle = MerkleTree(H.fast_eval(pro_data.xi, pro_data.xi_order, 1))
    hash_chain['H_merkle_root'] = H_merkle.root  # The same as first tree in the FRI trees.

    # Show that H is the composition of polynomials
    index_comp = hash_chain.random_int(pro_data.xi_order)
    set_merkle_elements('merkle_paths', polynomials_merkle_tress, index_comp, hash_chain)
    set_merkle_element('H_merkle_path', H_merkle, index_comp, hash_chain)

    print(' === Creating the FRI forest')

    # Create the FRI Merkle trees
    H_trace = H.fast_eval(pro_data.xi, pro_data.xi_order, 1)   # Using the same trace as before.
    friCommit = Fri(reverseOrder(H_trace))
    num_fri_trees = deg_power + 1
    hash_chain['num_fri_trees'] = num_fri_trees
    fri_coef = [hash_chain.randN() for _ in range(num_fri_trees - 1)]
    fri_op = [create_fri_op(alpha) for alpha in fri_coef]
    for op in fri_op:
        friCommit.fri_step(op)
    hash_chain['fri_roots'] = friCommit._roots
    # print(f'fri_coef are {fri_coef}')
    # print(f'H has degree {deg}')
    # print(f'#trees = {num_fri_trees}')
    # print(H)
    # friCommit.print_fri()

    # Show that the FRI trees are consistent
    index_fri = hash_chain.random_int(total)
    hash_chain['fri_paths'] = friCommit.reveal_path(index_fri, len(fri_coef) + 1)

    print(' === Final tree is constant')

    # Show that the last FRI tree is constant
    last_tree_width = total >> (num_fri_trees - 1)
    index_last_fri_1 = hash_chain.random_int(last_tree_width)
    index_last_fri_2 = hash_chain.random_int(last_tree_width)
    hash_chain['last_fri_path_1'] = friCommit.get_merkle_path(num_fri_trees - 1, index_last_fri_1)
    hash_chain['last_fri_path_2'] = friCommit.get_merkle_path(num_fri_trees - 1, index_last_fri_2)

    return hash_chain.dict
