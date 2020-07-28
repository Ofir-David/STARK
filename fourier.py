import cmath
import random

# L should be an array of length 2^n


def FFT(L, xi):
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
