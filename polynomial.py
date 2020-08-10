
import itertools
import math

from .fourier import FFT, FFT_inv
from .field import FieldElement
from . import field

print("loaded polynomial.py")


def ConvPoly(f):
    def wrapper(self, other):
        if (isinstance(other, int) or isinstance(other, FieldElement)):
            other = Poly([other])
        if (isinstance(other, Poly)):
            return f(self, other)
        return NotImplemented
    return wrapper


def ConvRational(f):
    def wrapper(self, other):
        if (isinstance(other, int) or isinstance(other, FieldElement)):
            other = RationalFunc(Poly([other]), 1)
        if (isinstance(other, Poly)):
            other = RationalFunc(other, 1)
        if (isinstance(other, RationalFunc)):
            return f(self, other)
        return NotImplemented
    return wrapper

# Question: should I make the coefficients fixed or not? Important for implementation of
#          degree and leading coefficient.


class Poly:

    def __init__(self, coef=[]):
        self.coef = [c for c in coef]
        self._remove_zeros()

    def _remove_zeros(self):
        while (len(self.coef) > 0 and self.coef[-1] == 0):
            self.coef.pop()

    def __call__(self, elem):
        sum = FieldElement(0)
        t = FieldElement(1)
        for c in self.coef:
            sum += t * c
            t *= elem
        return sum

    # --------------------- arithmetics -----------------------

    @ConvPoly
    def __eq__(this, other):
        for a, b in itertools.zip_longest(self.coef, other.coef, fillValue='a'):
            if (a != b):
                return False
        return true

    def __req__(this, element):
        return this == element

    @ConvPoly
    def __add__(self, other):
        d = max(len(self.coef), len(other.coef))
        return Poly([c + d for c, d in itertools.zip_longest(self.coef, other.coef, fillvalue=0)])

    def __radd__(self, other):
        return self + other

    @ConvPoly
    def __sub__(self, other):
        d = max(len(self.coef), len(other.coef))
        return Poly([c - d for c, d in itertools.zip_longest(self.coef, other.coef, fillvalue=0)])

    @ConvPoly
    def __rsub__(self, other):
        return other - self  # ConvPoly will turn other to Poly

    @ConvPoly
    def __mul__(self, other):
        # use numpy?
        n = self.deg() + 1
        m = other.deg() + 1
        d = n + m - 1
        return Poly([
            FieldElement(sum([self.getCoef(i - k) * other.getCoef(k) for k in range(m)]))
            for i in range(d)]
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if (isinstance(other, int)):
            other = FieldElement(other)
        if (isinstance(other, FieldElement)):
            return self * other.inv()
        if (isinstance(other, Poly)):
            return RationalFunc(self, other)
        return NotImplemented

    def __pow__(this, power):
        return field.batch_pow(this, [power])[0]

    # return the degree of the polynomial with deg(0)=-1
    # after running the method, len(self.coef)=deg+1
    def deg(self):
        self._remove_zeros()
        return len(self.coef) - 1  # this is not really the degree! just the length of the list

    def getCoef(self, index):
        if (index < 0 or index >= len(self.coef)):
            return 0
        return self.coef[index]

    def leadingCoef(self):
        self.deg()
        return self.coef[-1]

    def __str__(self):
        if (self.isZero()):
            return "0"
        return " + ".join([f'{str(c)}*X^{i}' for i, c in enumerate(self.coef) if not c == 0])

    def isZero(self):
        for c in self.coef:
            if (c != 0):
                return False
        self.coef = []
        return True

    # xi should be of order n>deg

    def fast_eval(self, xi, n, c):
        if (n <= self.deg()):
            raise Error()  # define error
        temp = 1
        L = []
        for alpha in self.coef:
            L.append(alpha * temp)
            temp *= c
        for _ in range(self.deg()-n):
            L.append(0)
        return FFT(L, xi)


class RationalFunc:

    def __init__(self, num=0, denum=1):
        self.num = num
        self.denum = denum

    @ConvRational
    def __eq__(self, other):
        return self.num * other.denum == self.denum * other.num

    def __req__(self, other):
        return self == other

    def __mul__(self, other):
        if (isinstance(other, RationalFunc)):
            return RationalFunc(self.num * other.num, self.denum * other.denum)
        num = self.num * other
        return RationalFunc(num, self.denum)

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if (isinstance(other, RationalFunc)):
            return RationalFunc(self.num * other.denum + self.denum * other.num,
                                self.denum * other.denum)
        num = Poly([1]) * other  # find a better method
        return RationalFunc(self.num + self.denum * num, self.denum)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if (isinstance(other, RationalFunc)):
            return RationalFunc(self.num * other.denum - self.denum * other.num,
                                self.denum * other.denum)
        num = Poly([1]) * other  # find a better method
        return RationalFunc(self.num - self.denum * num, self.denum)

    def __rsub__(self, other):  # other will not be RationalFunc
        pass

    def __truediv__(self, other):
        if (other == 0):
            raise ZeroDivisionError
        if (isinstance(other, int) or isinstance(other, FieldElement)):
            return RationalFunc(self.num / other, self.denum)
        if (isinstance(other, Poly)):
            return RationalFunc(self.num, self.denum * other)
        if (isinstance(other, RationalFunc)):
            return RationFunc(self.num * other.denum, self.denum * other.num)
        return NotImplemented

    def __rtruediv__(self, other):
        if (self == 0):
            raise ZeroDivisionError
        return other * RationalFunc(self.denum, self.num)

    def __str__(self):
        return str(self.num) + " / " + str(self.denum)

    def is_zero(self):
        return self.num == 0

    def div_with_remainder(self):
        num = self.num
        denum = self.denum  # should not be zero!
        q = Poly(0)
        dNum = num.deg()
        dDenum = denum.deg()
        while (dNum >= dDenum):
            temp = (num.leadingCoef() / denum.leadingCoef()) * X**(dNum - dDenum)
            q += temp
            num -= denum * temp
            dNum = num.deg()
        return q, num

    def to_polynomial(self):
        q, r = self.div_with_remainder()
        if (r == 0):
            return q
        return self


X = Poly([0, 1])

# special value can appear at most 1 time in x_values


def single_interpolate(x_values, special):
    special = FieldElement(special)
    # can make it in one loop
    num = math.prod([val - X for val in x_values if val != special])
    denum = FieldElement(math.prod([val - special for val in x_values if val != special]))
    return num / denum


def interpolate_poly(x_values, y_values):
    return sum([single_interpolate(x_values, x) * y for x, y in zip(x_values, y_values)])


# xi should be an element of order len(y_values)
# otherwise... well, let's just not go there
def interpolate_poly_FFT(xi, y_values):
    return Poly(FFT_inv(y_values, xi))
