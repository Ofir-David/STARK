import random
import math
from .field import FieldElement
from .protocol_data import ProtocolData
from .merkle import MerkleTree
from .fri import Fri, reverseOrder, reverse_int
from .polynomial import Poly, interpolate_poly_FFT
from . import polynomial
from .hash_chain import HashChainWriter, HashChainReader
from typing import List, Tuple, Dict, Any

from .prover import create_proof
from .verifier import verify


def randN(randomizer: random.Random):
    return randomizer.randrange(FieldElement._p)


# find the largest 2-power subgroup of the multiplicative group of the field

P = 3 * 2**30 + 1


# def is_generator(n: int) -> bool:
#     m = n
#     for i in range(29):
#         # m = n^(2^i)
#         m = (m * m) % P
#         # m = n^(2^(i+1))
#     # n^(2^29)
#     n0_30 = m * m % P  # n
#     n1_29 = n * n * n * m % P
#     return n0_30 != 1 and n1_29 != 1


# for i in [2, 3, 5, 7]:
#     print(i, is_generator(i))
# assert False

# inv = FieldElement.generatorInv()
# print(inv)
# print(f'{inv*FieldElement.generator()} == 1 ?')
# assert False

pro_data = ProtocolData()

print('========================================== START ==========================================')
print(f'Creating and verifying proof for Fibonacci starting at 1,2 with '
      f'{pro_data.fib_sequence_length} elements')
print(f'Our field has {FieldElement._p} elements with generator {pro_data.gen}')
print(f'The element {pro_data.xi} has multiplicative order {pro_data.xi_order}')

assert verify(pro_data, create_proof(pro_data, 3, 11))

print('========================================= FINISH =========================================')
