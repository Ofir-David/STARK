import math
from .merkle import MerkleTree
from .field import FieldElement


def reverseOrder(L):
    if (len(L) == 1):
        return L
    return reverseOrder(L[::2]) + reverseOrder(L[1::2])


class Fri:

    # needs to be a list of length 2^n
    def __init__(self, L):
        n = len(L)
        if (n != 2**math.ceil(math.log2(n))):
            return  # TO DO: produce some error
        L = reverseOrder(L)
        self._polEval = [L]
        self._mTree = [MerkleTree(L)]
        self._alphas = [FieldElement(0)]
        self._roots = [self._mTree[-1].root]

    def fri_step(self, alpha):
        if (isinstance(alpha, int)):
            alpha = FieldElement(alpha)
        if (not isinstance(alpha, FieldElement)):
            return False  # TO DO : produce some error
        if (len(self._polEval[-1]) == 1):
            return False  # TO DO : return message?
        self._alphas.append(alpha)
        # find a better way. maybe with generator?
        L = self._polEval[-1]
        L = [l1 + alpha * l2 for l1, l2 in zip(L[::2], L[1::2])]
        self._polEval.append(L)
        self._mTree.append(MerkleTree(L))
        self._roots.append(self._mTree[-1].root)
        return self._mTree[-1].root

    def is_constant(self):
        return len(self._polEval[-1]) == 1

    def print_fri(self):
        for L, alpha in zip(self._polEval, self._alphas):
            print(alpha, end=' ')
            print(L)
