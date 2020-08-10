import random
from .field import FieldElement
from .merkle import MerkleTree
from .fri import Fri
from .polynomial import Poly, interpolate_poly_FFT
from . import polynomial


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

# represent data using a polynomial pol(xi^i)=fib[i]


pol = interpolate_poly_FFT(xi, compute_Fib())  # has degree <=n-1


# condition on the polynomial

'''
pol(xi**(k+2)) = pol(xi**k)**2 + pol(xi**(k+1))**2 for k=0,...,n-3   (deg<=2n)
   equi
f_0(x) = pol(x*(xi**2)) - pol(x)**2 + pol(x*xi)**2 == 0 for x=xi**k , k=0,...,n-3
   equi

h_0 = f_0(x) * (x-xi**(n-2))*(x-xi**(n-1)) / (x**n-1) is a polynomial of degree <= 2n - (n-2) = n + 2

h_1 = (pol(x)-1)/(x-xi) poly of degree <= n-1
h_2 = (pol(x)-pol(xi**(n-1)) )/(x-xi**(n-1)) poly of degree <= n-1

convinve verifier that this is a polynomial of degree <= 2n
(h_0 + x^3 h_1 + x^3 h_2 ) x^(n-2) + h_0 + h_1 + h_2

'''

X = polynomial.X

f_0 = (pol(X * xi * xi) - (pol**2 + pol(X * xi)**2))            # f_0(x)=0 for x=xi**k, k=0,...,n-3
# deg(f_0) <= 2(n-1)
h_0 = f_0 * (X - xi**(n - 2)) * (X - xi**(n - 1)) / (X**n - 1)  # deg(h_0) <= n
h_1 = (pol - 1) / (X - 1)                                       # deg(h_1) <= n-2
h_2 = (pol - pol(xi**(n - 1))) / (X - xi**(n - 1))              # deg(h_2) <= n-2


# using randomness (from the verifier - add later) combine the polynomials

H = randN() * h_0 + randN() * h_1 + randN() * h_2 + X * X * (randN() * h_1 + randN() * h_2)


# using randomness (from the verifier - add later) create the fri forest for f and H

friCommit = Fri(compute_Fib())
while (not friCommit.is_constant()):
    friCommit.fri_step(randN())

friCommit.print_fri()
