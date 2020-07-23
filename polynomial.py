from field import FieldElement
import itertools
import math


def ConvPoly(f):
    def wrapper(self, other):
        if (isinstance(other, int) or isinstance(other, FieldElement)):
            other = Poly([other])
        if (isinstance(other, Poly)):
            return f(self, other)
        return NotImplemented
    return wrapper


class Poly:

    def __init__(self, coef=[0]):
        self.coef = [c for c in coef]

    def __call__(self, elem):
        sum = FieldElement(0)
        t = FieldElement(1)
        for c in self.coef:
            sum += t * c
            t *= elem
        return sum

    # --------------------- arithmetics -----------------------

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
        return NotImplemented

    def __pow__(this, power):
        return pow(this, power)

    def deg(self):
        return len(self.coef) - 1  # this is not really the degree! just the length of the list

    def getCoef(self, index):
        if (index < 0 or index >= len(self.coef)):
            return 0
        return self.coef[index]

    def __str__(self):
        if (self.isZero()):
            return "0"
        '''monoms = []
        if (self.coef[0]!=0):
            monoms.append(str(self.coef[0]))
        if (self.getCoef(1)!=0
        for i, c in enumerate(self.coef):
            if (c==0):
                continue
            if (c==1):
                coefStr = ""
            else:
                coefStr = str(c)
            if (i=0'''
        return " + ".join([f'{str(c)}*X^{i}' for i, c in enumerate(self.coef) if not c == 0])

    def isZero(self):
        for c in self.coef:
            if (c != 0):
                return False
        return True


class RationalFunc:

    def __init__(self, num=0, denum=1):
        self.num = num
        self.denum = denum

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

    def __str__(self):
        return str(self.num) + " / " + str(self.denum)


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
