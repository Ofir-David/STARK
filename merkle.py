import hashlib
from field import FieldElement

sha = hashlib.sha256()


def hash(s):
    return hashlib.sha256(s.encode()).hexdigest()


class MerkleTree:

    def __init__(self, elem):
        if (isinstance(elem, int) or isinstance(elem, FieldElement)):
            elem = [elem]
        if (isinstance(elem, list)):
            n = len(elem)
            if (n > 1):
                self.left = MerkleTree(elem[:n // 2])
                self.right = MerkleTree(elem[n // 2:])
                self.root = hash(self.left.root + self.right.root)
            else:
                self.data = elem
                self.root = hash(str(FieldElement(elem)))  # fix?
        return None


m = MerkleTree(FieldElement(5))
print(m.root)
m = MerkleTree([FieldElement(5), 2, 3])
print(m.root)
