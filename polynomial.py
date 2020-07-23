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

    @ConvPoly
    def __mul__(self, other):
        '''# creates a new list. Can I just update the original?
        if (isinstance(other, int) or isinstance(other, FieldElement)):
            self.coef = [c*other for c in self.coef]
        if (not isinstance(other, Poly)):
            return NotImplemented'''
        # use numpy?
        n = self.deg() + 1
        m = other.deg() + 1
        d = n + m - 1
        return Poly([
            sum([self.getCoef(i - k) * other.getCoef(k) for k in range(m)])
            for i in range(d)]
        )

    def __rmul__(self, other):
        return self * other

    @ConvPoly
    def __add__(self, other):
        d = 1 + max(self.deg(), other.deg())
        return Poly([c + d for c, d in itertools.zip_longest(self.coef, other.coef, fillvalue=0)])

    def __radd__(self, other):
        return self + other

    @ConvPoly
    def __sub__(self, other):
        d = 1 + max(self.deg(), other.deg())
        return Poly([c - d for c, d in itertools.zip_longest(self.coef, other.coef, fillvalue=0)])

    @ConvPoly
    def __rsub__(self, other):
        return other - self  # ConvPoly will turn other to Poly

    def __truediv__(self, other):
        if (isinstance(other, int)):
            other = FieldElement(other)
        if (isinstance(other, FieldElement)):
            return self * other.inv()
        return NotImplemented

    def deg(self):
        return len(self.coef) - 1

    def getCoef(self, index):
        if (index < 0 or index >= len(self.coef)):
            return 0
        return self.coef[index]

    def __str__(self):
        return " + ".join([f'{str(c)}*X^{i}' for i, c in enumerate(self.coef) if not c == 0])


X = Poly([0, 1])


def single_interpolate(x_values, special):
    num = math.prod([val - X for val in x_values if val != special])
    denum = FieldElement(math.prod([val - special for val in x_values if val != special]))
    return num / denum


def interpolate_poly(x_values, y_values):
    return sum([single_interpolate(x_values, val) * y for val, y in zip(x_values, y_values)])


p = Poly()
q = Poly()
p.coef = [1, 1, 1]
q.coef = [1, 1]
h = p - q
print(h)
print(h(3))
print(p(q))

f = single_interpolate([1, 2, 3, 4], 0)
print(f)
print(f(1))
print(f(2))
print(f(3))
print(f(4))

print("---------------")
g = interpolate_poly([1, 2, 3, 4], [5, 9, 7, 8])
print(g)
print(g(1))
print(g(2))
print(g(3))
print(g(4))
