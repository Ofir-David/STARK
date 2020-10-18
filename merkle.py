import hashlib
import math
import colorama
from .field import FieldElement, ExtElement

from typing import List

sha = hashlib.sha256()


def hash(s) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


class MerkleTree:

    @staticmethod
    def hashElem(elem: ExtElement) -> str:
        if isinstance(elem, int):
            return str(FieldElement(elem))
        if isinstance(elem, FieldElement):
            return str(elem)

    @ staticmethod
    def check_path(leafIndex: int, hashGen, rootHash: str):
        lastHash = next(hashGen)
        for nodeHash in hashGen:
            if (leafIndex % 2 == 0):  # left child
                lastHash = hash(lastHash + nodeHash)
            else:
                lastHash = hash(nodeHash + lastHash)
            leafIndex = leafIndex // 2
            # print(lastHash + "(" + nodeHash + ")" + '\n')
        if (lastHash == rootHash):
            return True
        else:
            return False

    def printAll(self, tabs: int = 0):
        print("\t" * tabs + self.root)
        if (self.numLeaves > 1):
            self.left.printAll(tabs + 1)
            self.right.printAll(tabs + 1)

    def __init__(self, elem: List):
        if not isinstance(elem, list):
            elem = [elem]
        n = len(elem)
        self.numLeaves = 2**math.ceil(math.log2(n))
        elem = elem + [0] * (self.numLeaves - n)
        n = self.numLeaves
        if (n > 1):
            self.left = MerkleTree(elem[:n // 2])
            self.right = MerkleTree(elem[n // 2:])
            self.root: str = hash(self.left.root + self.right.root)
        else:
            self.data = elem[0]
            self.root = str(self.data)

    def reveal_path(self, leafIndex: int):
        if (self.numLeaves == 1):
            yield self.root
            return
        if (leafIndex < self.numLeaves // 2):
            child = self.left.reveal_path(leafIndex)
            yield from child
            # print(self.root + "("+self.right.root+")")
            yield self.right.root
        else:
            child = self.right.reveal_path(leafIndex - self.numLeaves // 2)
            yield from child
            # print(self.root+"("+self.left.root+")")
            yield self.left.root
