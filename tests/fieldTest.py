import pytest
from field import FieldElement


def test_eq(n):
    ne = FieldElement(n)
    nne = FieldElement(n)
    assert ne == nne
    assert ne == n
    assert n == ne


'''
def test_add(n,m):
    k = (n+m)%FieldElement._p
    if (k<0):
        k+=FieldElement._p
    ne = FieldElement(n)
    me = FieldElement(m)
    assert 1=1'''
