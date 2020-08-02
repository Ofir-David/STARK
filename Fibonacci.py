from .field import FieldElement
from .merkle import MerkleTree

gen = FieldElement.generator()
N = FieldElement._p - 1
while (N % 2 == 0):
    N = N // 2
xi = gen**N
n = FieldElement._p // N   # this is a power of two

# compute Fibonacci

a_1 = FieldElement(1)
a_2 = FieldElement(2)

L = [a_1, a_2]
for i in range(N - 2):
    L.append(L[-2]**2 + L[-1]**2)
a_N = FieldElement(L[-1])

# commitment


def reverseOrder(L):
    if (len(L) == 1):
        return L
    return reverseOrder(L[::2]) + reverseOrder(L[1::2])


def randN():
    return random.randint(0, field.FieldElement._p)


polEval = [L]
mTree = [MerkleTree(L)]
roots = [mTree[0].root]
alphas = []

while (len(L) > 1):
    alpha = randN()
    alpha.append(alpha)
    # find a better way. maybe with generator?
    L = [l1 + alpha * l2 for l1, l2 in zip(L[::2], L[1::2])]
    polEval.append(L)
    mTree.append(MerkleTree(L))
    roots.append(mTree[-1].root)
