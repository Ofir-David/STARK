import random
from .field import FieldElement
from .merkle import MerkleTree
from .fri import Fri


def randN():
    return random.randint(0, FieldElement._p)


# find the largest 2-power subgroup of the multiplicative group of the field

gen = FieldElement.generator()
N = FieldElement._p - 1
while (N % 2 == 0):
    N = N // 2
xi = gen**N
n = (FieldElement._p - 1) // N   # this is a power of two


# decide on the second element, and compute the Fibonacci (squared) sequence
def compute_Fib(secondElement=2):
    a_1 = FieldElement(1)
    a_2 = FieldElement(secondElement)

    L = [a_1, a_2]
    for i in range(n - 2):
        L.append(L[-2]**2 + L[-1]**2)
    a_n = FieldElement(L[-1])
    return L

# commitment


friCommit = Fri(compute_Fib())
while (not friCommit.is_constant()):
    friCommit.fri_step(randN())

friCommit.print_fri()
