import random

from ..field import FieldElement
from ..polynomial import Poly, RationalFunc
from .. import polynomial


def randN():
    return random.randint(-FieldElement._p * 2, FieldElement._p * 2)


def _test_interpolate_with_values(x_values, special, y_values):
    p = polynomial.single_interpolate(x_values, special)
    special = FieldElement(special)
    for val in x_values:
        if (val != special):
            assert p(val) == 0
    assert p(special) == 1

    q = 0
    for x, y in zip(x_values, y_values):
        p = polynomial.single_interpolate(x_values, x) * y
        # print(x, p)
        q += p
        for t in x_values:
            if (t == x):
                assert p(t) == y
            else:
                assert p(t) == 0

    p = polynomial.interpolate_poly(x_values, y_values)
    for x, y in zip(x_values, y_values):
        assert p(x) == y


def test_interpolate():

    for i in range(10):
        d = 10
        x_values = list(set([randN() % FieldElement._p for i in range(d)]))
        special = randN()
        y_values = [randN() for x in x_values]
        '''x_values = [0, 2, 4, 6, 10]
        y_values = [-10, 20, -14, 16, -4]
        special = -1'''
        '''print(str(x_values))
        print(str(y_values))
        print(special)'''

        _test_interpolate_with_values(x_values, special, y_values)


# test_interpolate()
