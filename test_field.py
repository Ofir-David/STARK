import pytest
from field import FieldElement
import random
import operator


# python -m pytest test_field.py

def randN():
    return random.randint(-FieldElement._p * 2, FieldElement._p * 2)


def test_eq():
    def single_test_eq(n):
        ne = FieldElement(n)
        nne = FieldElement(n)
        assert ne == nne
        assert ne == n
        assert n == ne
    for i in range(10):
        single_test_eq(randN())


def bin_test(f, n, m, res):
    ne = FieldElement(n)
    me = FieldElement(m)
    rese = FieldElement(res)
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
        if ((m % FieldElement._p) != 0):
            bin_test(operator.truediv, n * m, m, n)
