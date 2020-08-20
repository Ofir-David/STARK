

import random
import sympy

ALPHA = 1
BETA = 1
FIELD_PRIME = 97


def is_quad_residue(n, p):
    """
    Returns True if n is a quadratic residue mod p.
    """
    return sympy.is_quad_residue(n, p)


def sqrt_mod(n, p):
    """
    Finds the minimum positive integer m such that (m*m) % p == n
    """
    return min(sympy.sqrt_mod(n, p, all_roots=True))


def igcdex(a, b):
    """Returns x, y, g such that g = x*a + y*b = gcd(a, b).

       >>> from sympy.core.numbers import igcdex
       >>> igcdex(2, 3)
       (-1, 1, 1)
       >>> igcdex(10, 12)
       (-1, 1, 2)

       >>> x, y, g = igcdex(100, 2004)
       >>> x, y, g
       (-20, 1, 4)
       >>> x*100 + y*2004
       4

    """
    if (not a) and (not b):
        return (0, 1, 0)

    if not a:
        return (0, b//abs(b), abs(b))
    if not b:
        return (a//abs(a), 0, abs(a))

    if a < 0:
        a, x_sign = -a, -1
    else:
        x_sign = 1

    if b < 0:
        b, y_sign = -b, -1
    else:
        y_sign = 1

    x, y, r, s = 1, 0, 0, 1

    while b:
        (c, q) = (a % b, a // b)
        (a, b, r, s, x, y) = (b, c, x - q*r, y - q*s, r, s)

    return (x * x_sign, y * y_sign, a)


def div_mod(n, m, p):
    """
    Finds a nonnegative integer 0 <= x < p such that (m * x) % p == n
    """
    a, b, c = igcdex(m, p)
    assert c == 1
    return (n * a) % p


class InvalidECPoint(Exception):
    def __init__(self):
        super().__init__('Not a point on the elliptic curve.')


def is_on_curve(x: int, y: int):
    return 0 == (x * (x * x + ALPHA) + BETA - y * y) % FIELD_PRIME


def binaryEC(f):
    def wrapper(self, other):
        if (isinstance(other, ECPoint)):
            return f(self, other)
        raise InvalidECPoint()
    return wrapper


class ECPoint:
    """
    A point on the elliptic curve y^2 = x^3 + ALPHA*x +BETA
    """

    @staticmethod
    def random():
        for i in range(20):
            x = random.randint(0, FIELD_PRIME)
            if (x == FIELD_PRIME):
                return ECPoint.get_zero()

            y_squared = (x * x * x + ALPHA * x + BETA) % FIELD_PRIME
            if is_quad_residue(y_squared, FIELD_PRIME):
                y = sqrt_mod(y_squared, FIELD_PRIME)
                if (random.randint(0, 1)):
                    y = -y
                return ECPoint(x, y)
        return ECPoint.get_zero()

    @staticmethod
    def get_zero():
        p = ECPoint.__new__(ECPoint)
        p._x = 0
        p._y = 1
        p._z = 0
        return p

    def is_zero(self):
        return self._z == 0

    def __str__(self):
        if (self.is_zero()):
            return '0'
        return f'({self._x},{self._y})'

    def __init__(self, x: int, y: int):
        if (not is_on_curve(x, y)):
            raise InvalidECPoint()
        self._x = x % FIELD_PRIME
        self._y = y % FIELD_PRIME
        self._z = 1

    @binaryEC
    def __eq__(self, other):
        if (self.is_zero()):
            return other.is_zero()
        if (other.is_zero()):
            return False
        return (self._x == other._x and self._y == other._y)

    def __neg__(self):
        if (self.is_zero()):
            return self
        return ECPoint(self._x, -self._y)

    def double(self):
        if (self.is_zero()):
            return self
        m = div_mod(3 * self._x * self._x + ALPHA, 2 * self._y, FIELD_PRIME)
        x = m * m - self._x - other._x
        y = m * (self._x - x) - self._y
        return ECPoint(x, y)

    @binaryEC
    def __add__(self, other):
        if (self.is_zero()):
            return other
        if (other.is_zero()):
            return self
        if (self._x != other._x):
            m = div_mod(other._y - self._y, other._x - self._x, FIELD_PRIME)
            x = m * m - self._x - other._x
            y = m * (self._x - x) - self._y
            return ECPoint(x, y)
        if (self._y != other._y or self._y == 0):
            return ECPoint.get_zero()
        m = div_mod(3 * self._x * self._x + ALPHA, 2 * self._y, FIELD_PRIME)
        x = m * m - self._x - other._x
        y = m * (self._x - x) - self._y
        return ECPoint(x, y)

    def __radd__(self, other):
        return self + other

    @binaryEC
    def __sub__(self, other):
        return self + (-other)

    def _rmult(self, m):
        """
        Multiplies this point by m under the assumption that it is a positive integer.
        Runs in O(log(m)) steps of ECPoint.double and ECpoint.__add__
        """
        if (m == 1):
            return self
        temp = (m // 2) * self.double()
        if (m % 2 == 0):
            return temp
        return self + temp

    def __rmult__(self, m):
        if (not isinstance(m, int)):
            raise Exception()
        if (m == 0):
            return ECPoint.get_zero()
        if (m < 0):
            return -self._rmult(-m)
        return self._rmult(m)
