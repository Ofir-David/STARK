import cmath
import random
from .field import FieldElement


# L should be an array of length 2^n


def FFT(L, xi):
    '''
    Perform the fourier transform.
    L should be a list of size 2^n over some field F, and xi should be a 2^n
    root of unity in F
    '''
    if (len(L) == 1):
        return L
    L_even = L[::2]  # jump by two
    L_odd = L[1::2]
    xi2 = xi * xi
    even_res = FFT(L_even, xi2)
    odd_res = FFT(L_odd, xi2)
    res = []
    z = 1
    for le, lo in zip(even_res, odd_res):
        res.append(le + z * lo)
        z *= xi
    for le, lo in zip(even_res, odd_res):
        res.append(le + z * lo)
        z *= xi
    return res


def FFT_inv(L, xi):
    '''
    Perform the inverse fourier transform.
    L should be a list of size 2^n over some field F, and xi should be a 2^n
    root of unity in F
    '''
    if (isinstance(xi, FieldElement)):
        d = FieldElement(len(L)).inv()
    else:
        d = 1.0 / len(L)
    return [d * elem for elem in FFT(L, xi**(-1))]
