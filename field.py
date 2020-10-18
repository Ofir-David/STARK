import math
from .math_utils import gcd
from typing import Union, List

print("loaded file field.py")

ExtElement = Union['FieldElement', int]


def getValue(element: ExtElement) -> int:
    # returns the integer value of a field element in the range [0,_p), or the element itself
    # if it is an integer. Otherwise returns 1 (should change to NotImplemented?)
    if (isinstance(element, FieldElement)):
        return element.n
    if (isinstance(element, int)):
        return element
    return NotImplemented


def getElement(element: ExtElement):
    if (isinstance(element, FieldElement)):
        return element
    if (isinstance(element, int)):
        return FieldElement(element)


def Convert(f):
    def wrapper(self, element: ExtElement):
        value = getValue(element)
        if (value == NotImplemented):
            return NotImplemented
        return f(self, value)

    return wrapper


class FieldElement:

    _p = 3 * (2**30) + 1  # 17
    _inv_gen = None

    @staticmethod
    def generator():
        return FieldElement(3)

    @staticmethod
    def generatorInv():
        if FieldElement._inv_gen is None:
            FieldElement._inv_gen = FieldElement.generator().inv().n
        return FieldElement(FieldElement._inv_gen)

    def __init__(this, n: int):
        # should change the n variable into property so it will always be mod _p
        this.n = getValue(n) % FieldElement._p  # might be negative, so
        # For some reason, in java you could get negative numbers...
        # if (this.n < 0):
        #    this.n += FieldElement._p

    # The @element parameter in the following can be either FieldElement or integer
    # Any other type will return NotImplemented, so it can try to use the same operator on
    # the element parameter (e.g. element.__add__(self) )
    @Convert
    def __eq__(this, element):
        return this.n == element % FieldElement._p

    def __req__(this, element):
        return this == element

    # ----------------------- arithmetics -------------------------

    @Convert
    def __add__(this, element):
        return FieldElement(this.n + element)

    @Convert
    def __radd__(this, element):
        return FieldElement(this.n + element)

    @Convert
    def __sub__(this, element):
        return FieldElement(this.n - element)

    @Convert
    def __rsub__(this, element):
        return FieldElement(element - this.n)

    @Convert
    def __mul__(this, element):
        return FieldElement(this.n * element)

    @Convert
    def __rmul__(this, element):
        return FieldElement(this.n * element)

    @Convert
    def __truediv__(this, element):
        return this * FieldElement(element).inv()

    @Convert
    def __rtruediv__(this, element):
        return element * this.inv()

    def __pow__(this, power: int):
        if (this == 0):
            return this
        # if batch_pow doesn't do any multiplication, it will just return 1 as a number
        if (power == 0):
            return FieldElement(1)
        if (power > 0):
            base = this
        else:
            base = this.inv()
            power = -power
        return batch_pow(base, [power])[0]
        # return FieldElement(pow(this.n, power, this._p))

    def __abs__(this):
        return this

    # -------------------- extra arithmetics -----------------------

    def inv(this):
        if (this.n == 0):
            raise ZeroDivisionError
        _, m, _ = gcd(this.n, this._p)
        return FieldElement(m)

    # ------------------------------------------------------------------

    def __str__(this):
        return str(this.n)

    def __repr__(this):
        return str(this)


def batch_pow(x, L: List[int]):
    """
    Compute simultanously several powers of the same number x.
    """
    max_power = max(L)
    results = [1 for _ in L]
    if (max_power == 0):
        return results
    n_bits = int(math.log2(max_power)) + 1
    for i in range(n_bits):
        mask = 1 << i
        for j in range(len(L)):
            if (L[j] & mask):
                results[j] *= x
        x *= x
    return results


def batch_inv(L: List[ExtElement]):
    """
    Returns a list of inverses of the given elements.
    """
    # If L=[a_1, ..., a_n], create the list [1,a_1,a_1*a_2,..., a_1*a_2*...*a_n]
    mults = [FieldElement(1)]
    for elem in L:
        mults.append(mults[-1] * elem)
    # If P_i = a_1*...*a_i (with P_0=1), then given 1/P_n we can find (using multiplication):
    #   (1) 1/(a_n) = P_(n-1)* 1/P_n, and
    #   (2) 1/P_(n-1) = a_n* 1/P_n
    # Now use induction.
    inverse = mults[-1].inv()
    res = [0 for _ in L]
    for i in reversed(range(len(L))):
        res[i] = mults[i - 1] * inverse
        inverse *= L[i]
    return res
