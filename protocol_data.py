from .field import FieldElement, ExtElement
from .polynomial import Poly, interpolate_poly_FFT
import math

from typing import List


class ProtocolData:

    @staticmethod
    def two_power(N: int):
        """
        Returns 2^k, m such that m is odd and N= 2^k * m.
        """
        M = 1
        while (N % 2 == 0):
            N = N // 2
            M *= 2
        return M, N

    def __init__(self):
        self.gen = FieldElement.generator()
        N = FieldElement._p - 1
        self.N_two_power, self.N_odd = ProtocolData.two_power(N)
        self.gen_2_pow = self.gen**self.N_odd        # xi has order N_two_power
        self.n = self.N_two_power             # this is a power of two, which is the order of xi
        self.pow = int(math.log2(self.N_two_power))
        self.fib_pow = self.pow - 2

        poww = self.N_two_power >> 13
        if poww >= 1:
            self.xi = self.gen_2_pow ** poww
            self.xi_order = 1 << 13
        else:
            self.xi = self.gen_2_pow
            self.xi_order = self.N_two_power

        self.fib_sequence_length = 32
        self.composition_trace = (1 << self.fib_pow)
        self.H_trace_length = self.N_two_power - 1
        self.coset = self.gen

    def get_polynomials(self):

        def boundary_1(
            fib_trace: List[FieldElement], pol_trace: List[FieldElement],
            xi: FieldElement, xi_power: int, x: FieldElement) \
                -> FieldElement:
            return (pol_trace[xi_power] - fib_trace[0]) // (x - 1)

        def boundary_2(
            fib_trace: List[FieldElement], pol_trace: List[FieldElement],
            xi: FieldElement, xi_power: int, x: FieldElement) \
                -> FieldElement:
            return (pol_trace[xi_power] - fib_trace[-1]) // (x - xi**(len(fib_trace) - 1))

        def fibonacci_condition(
                fib_trace: List[FieldElement], pol_trace: List[FieldElement],
                xi: FieldElement, xi_power: int, x: FieldElement):
            seq_len = len(fib_trace)
            # f_0(x)=0 for x=xi**k, k=0,...,seq_len-3,  deg(f_0) <= 2*(seq_len-1)
            f_0 = (pol_trace[xi_power + 2] -
                   ((pol_trace[xi_power]**2) + (pol_trace[xi_power + 1]**2)))       #
            # complete it to have 0 on xi**k for k<= power of two
            deg = int(2**math.ceil(math.log2(seq_len - 2)))
            f_temp = f_0
            root = xi**(seq_len - 2)
            for k in range(seq_len - 2, deg):
                f_temp *= (pol_trace[xi_power] - root)
                root *= xi

            return [boundary_1, boundary_2]

    def get_pol_trace(self, pol: Poly) -> List[ExtElement]:
        return pol.fast_eval(self.xi, self.xi_order, self.coset)

    # def __init__(self):
    #     self.gen = FieldElement.generator()
    #     N = FieldElement._p - 1
    #     self.N_two_power, self.N_odd = ProtocolData.two_power(N)
    #     self.xi = self.gen**self.N_odd        # xi has order N_two_power
    #     self.n = self.N_two_power             # this is a power of two, which is the order of xi
    #     self.pow = int(math.log2(self.N_two_power))
    #     self.fib_pow = self.pow - 2

    #     self.fib_sequence_length = (1 << self.fib_pow) - 1
    #     self.composition_trace = (1 << self.fib_pow)
    #     self.H_trace_length = self.N_two_power - 1
