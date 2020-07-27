import pytest


def test_test():
    assert 1 == 1


'''import random
import operator

from .. import field
# from ..field import field.FieldElement


# python -m pytest tests/test_field.py.   NEVER MIND! now it works ok!

print("loaded test_file")


def randN():
    return random.randint(-field.FieldElement._p * 2, field.FieldElement._p * 2)


def single_test_eq(n):
    ne = field.FieldElement(n)
    nne = field.FieldElement(n)
    assert ne == nne
    assert ne == n
    assert n == ne


def test_eq():
    for i in range(10):
        n = randN()
        single_test_eq(n)
        assert field.FieldElement(n) != f'{n}'
'''

'''

def bin_test(f, n, m, res):
    ne = field.FieldElement(n)
    me = field.FieldElement(m)
    rese = field.FieldElement(res)
    assert rese == res
    assert f(ne, me) == rese
    assert f(n, me) == rese
    assert f(ne, m) == rese


def test_operations():
    for i in range(10):
        n = randN()
        m = randN()
        # print(f'{n=}, {m=}')
        bin_test(operator.add, n, m, n + m)
        bin_test(operator.sub, n, m, n - m)
        bin_test(operator.mul, n, m, n * m)
        if ((m % field.FieldElement._p) != 0):
            bin_test(operator.truediv, n * m, m, n)
        else:
            with pytest.raises(ZeroDivisionError):
                bin_test(operator.truediv, n, m, 0)


def gcd_test_single(n, m):
    (d, a, b) = field.gcd(n, m)
    print(f'{n=}, {m=}')
    print(f'{a=}, {b=}')
    print(f'{d=}')
    assert d == a * n + b * m
    n = n // d
    m = m // d
    (d, a, b) = field.gcd(n, m)
    assert d == a * n + b * m
    assert d * d == 1


def test_gcd():
    for i in range(10):
        n = randN()
        m = randN()
        gcd_test_single(n, m)


def single_power_test(n, power):
    print(f'{n=}, {power=}')
    ne = field.FieldElement(n)
    if (ne == 0):
        assert ne**power == 0
        return
    if (power < 0):
        me = ne.inv()
        assert ne * me == 1
        assert me * n == 1
        ne = me
        power = -power
    assert ne**power == ne.n**power


def test_power():
    for i in range(10):
        n = randN()
        m = randN()
        single_power_test(n, m)


def single_test_batch_inverse(L):
    res = field.batch_inv(L)
    for r, ll in zip(res, L):
        assert r * ll == 1


def test_batch_inverse():
    for i in range(10):
        L = [randN() for _ in range(20)]
        L = [ll for ll in L if (ll % field.FieldElement._p) != 0]
        single_test_batch_inverse(L)
'''
