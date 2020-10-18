import math
from .merkle import MerkleTree
from .field import FieldElement, ExtElement, getElement

from typing import List, Any, TypeVar, List, Callable

T = TypeVar('T')
BinaryOp = Callable[[ExtElement, ExtElement], ExtElement]


def create_fri_op(alpha: ExtElement):
    def op(even_elem: ExtElement, odd_elem: ExtElement) \
            -> ExtElement:
        return (even_elem + odd_elem) + alpha * (even_elem - odd_elem)

    return op


def reverseOrder(L: List[T]) -> List[T]:
    """
    Reorder the elements of the list so that their binary representation of the index is reversed.
    For example, for a list of size 16 (4 bits), the object at index 13=b1101 will be instead at
    index 11=b1011.
    In general, the object of index b(a_0 a_1 ... a_n) will move to index b(a_n ... a_1 a_0).
    """
    if (len(L) == 1):
        return L
    return reverseOrder(L[::2]) + reverseOrder(L[1::2])


def reverse_int(n: int, digits: int):
    assert n < 2**digits
    reverse = 0
    for _ in range(digits):
        reverse *= 2
        if n % 2:
            reverse += 1
        n //= 2
    return reverse


def is_odd_child(index: int, height: int):
    return index >= (1 << (height - 1))


def _pair_step(alpha: ExtElement, even_elem: ExtElement, odd_elem: ExtElement) \
        -> ExtElement:
    return (even_elem + odd_elem) + alpha * (even_elem - odd_elem)


class Fri:

    # needs to be a list of length 2^k
    def __init__(self, L: List[ExtElement]):
        """
        Creates a new Fri tree for the given list.
        The list need to be of length which is a power of two.
        """
        n = len(L)
        self.height = math.ceil(math.log2(n))
        assert (n == 2**self.height), f'List\'s length is {len(L)}, and needs to be a power of 2.'
        self._polEval = [L]
        self._mTree = [MerkleTree(L)]
        self._roots = [self._mTree[-1].root]

    def fri_step(self, op: BinaryOp):
        """
        Creates a new Merkle FRI tree of size half the size of the last tree, and return the root
        of the tree.
        """
        assert len(self._polEval[-1]) > 1, \
            f'Last FRI tree already has only 1 element. Cannot create a smaller tree'
        # find a better way. maybe with generator?
        L = self._polEval[-1]
        L = [op(l1, l2) for l1, l2 in zip(L[::2], L[1::2])]
        self._polEval.append(L)
        self._mTree.append(MerkleTree(L))
        self._roots.append(self._mTree[-1].root)
        return self._mTree[-1].root

    def get_num_of_trees(self):
        return len(self._mTree)

    def is_constant(self):
        """
        Checks if the last FRI tree generated has only one element.
        """
        return len(self._polEval[-1]) == 1

    def print_fri(self):
        for L, alpha in zip(self._polEval, self._alphas):
            print(alpha, end=' ')
            print(L)

    def get_merkle_path(self, merkle_index: int, leaf_index: int):
        return list(self._mTree[merkle_index].reveal_path(leaf_index))

    @ staticmethod
    def check_path(
        leaf_index: int, height: int, binary_ops: List[BinaryOp],
        hashGen: List, rootHashes: List[str]) \
            -> bool:
        # Check first validity of the Merkle paths.
        index = leaf_index
        for path, root in zip(hashGen, rootHashes):
            if not MerkleTree.check_path(index, iter(path), root):
                return False
            index //= 2
        # Check the relations between the different trees.
        index = leaf_index
        for i in range(len(hashGen) - 1):
            gen = hashGen[i]
            even_child = getElement(int(gen[0]))  # odd.
            odd_child = getElement(int(gen[1]))   # even
            if index % 2 == 1:  # index is the odd child
                temp = odd_child
                odd_child = even_child
                even_child = temp
            combined = getElement(int(hashGen[i + 1][0]))
            if combined != binary_ops[i](even_child, odd_child):
                return False
            index //= 2
        return True

    def reveal_path(self, leaf_index: int, tree_count: int) -> List[List]:
        index = leaf_index
        paths = []
        power = int(2**self.height)
        for tree in self._mTree[: tree_count]:
            paths.append(list(tree.reveal_path(index)))
            index //= 2
        return paths

    def get_roots(self, tree_count: int):
        return self._roots[: tree_count]
