import random
import math
from .field import FieldElement
from .protocol_data import ProtocolData
from .merkle import MerkleTree
from .fri import Fri, reverseOrder, reverse_int, create_fri_op
from .polynomial import Poly, interpolate_poly_FFT
from . import polynomial
from .hash_chain import HashChainWriter, HashChainReader
from .prover import create_coefficients
from typing import List, Tuple, Dict, Any


def evaluate_composition(values, randomizer, d: int):
    H = sum(randomizer.randN() * value1 + randomizer.randN() * monomial_times_values
            for value1, monomial_times_values in values)
    # H = randN() * h_0 + randN() * h_1 + randN() * h_2 + X * X * (randN() * h_1 + randN() * h_2)
    return H


def get_check_merkle_element(name: str, root: str, index: int, hash_chain: HashChainReader) -> str:
    merkle_path = hash_chain[name]
    assert MerkleTree.check_path(index, iter(merkle_path), root),\
        f'Merkle tree path is invalid'
    return merkle_path[0]


def get_check_merkle_elements(
        name: str, roots: List[str], index: int, hash_chain: HashChainReader) -> List[str]:
    merkle_paths = hash_chain[name]
    checks = [MerkleTree.check_path(index, iter(path), root)
              for path, root in zip(merkle_paths, roots)]
    assert any(checks),\
        f'Merkle tree paths are invalid\n{checks}'
    return [path[0] for path in merkle_paths]


def verify(
        pro_data: ProtocolData, verifier_data: Dict[str, Any]) -> bool:

    print('\n------------------------- Starting the verifier -------------------------')
    total = pro_data.fib_sequence_length + 1
    # Verifier
    hash_chain = HashChainReader(verifier_data)
    firstElement = hash_chain['first']
    secondElement = hash_chain['second']
    lastElement = hash_chain['last']

    # Create the condition polynomials
    polynomials_merkle_roots = hash_chain['pol_merkle_roots']

    deg = hash_chain['deg']
    deg_power = int(math.log2(deg))

    num_poly = hash_chain['num_poly']

    # Create the composition polynomial
    coef = create_coefficients(hash_chain, num_poly)
    H_merkle_root = hash_chain['H_merkle_root']  # The same as first tree in the FRI trees.

    # Verify that H is the composition of polynomials
    index_comp = hash_chain.random_int(pro_data.xi_order)
    get_check_merkle_elements('merkle_paths', polynomials_merkle_roots, index_comp, hash_chain)
    get_check_merkle_element('H_merkle_path', H_merkle_root, index_comp, hash_chain)

    # Create the FRI Merkle trees
    height = int(math.log2(total))
    num_fri_trees = hash_chain['num_fri_trees']
    fri_coef = [hash_chain.randN() for _ in range(num_fri_trees - 1)]
    fri_op = [create_fri_op(alpha) for alpha in fri_coef]
    fri_roots = hash_chain['fri_roots']

    # Show that the FRI trees are consistent
    index_fri = hash_chain.random_int(total)
    fri_paths = hash_chain['fri_paths']
    assert Fri.check_path(index_fri, height, fri_op, fri_paths, fri_roots), \
        f'FRI is invalid'

    # Show that the last FRI tree is constant
    last_tree_width = total >> (num_fri_trees - 1)
    index_last_fri_1 = hash_chain.random_int(last_tree_width)
    index_last_fri_2 = hash_chain.random_int(last_tree_width)
    last_fri_path_1 = hash_chain['last_fri_path_1']
    last_fri_path_2 = hash_chain['last_fri_path_2']
    last_root = fri_roots[-1]
    assert MerkleTree.check_path(index_last_fri_1, iter(last_fri_path_1), last_root) and \
        MerkleTree.check_path(index_last_fri_2, iter(last_fri_path_2), last_root), \
        f'Last FRI tree has invalid pathes'
    assert last_fri_path_1[0] == last_fri_path_2[0], \
        f'Last tree is not constant'

    return True
