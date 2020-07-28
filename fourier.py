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


def test_FFT_addition(n):
    N = 2**n
    xi = cmath.exp(2 * cmath.pi * 1j / N)
    L1 = random.sample(range(-3 * N, 3 * N), N)
    L2 = random.sample(range(- 3 * N, 3 * N), N)
    L = [l1 + l2 for l1, l2 in zip(L1, L2)]
    res1 = FFT(L1, xi)
    res2 = FFT(L2, xi)
    res = FFT(L, xi)
    res_add = [r1 + r2 for r1, r2 in zip(res1, res2)]
    for a, b in zip(res, res_add):
        assert abs(a - b) < error
    # print(res)
    # print(res_add)


error = 1e-10


def test_FFT_basis(n):
    N = 2**n
    xi = cmath.exp(2 * cmath.pi * 1j / N)
    w = 1
    for i in range(N):
        L = [0] * N
        L[i] = 1
        res = FFT(L, xi)
        z = 1
        for j in range(N):
            diff = z - res[j]
            assert abs(diff) < error
            z *= w
        w *= xi


def single_test_FFT(n):
    xi = cmath.exp(2 * cmath.pi * 1j / n)
    L = random.sample(range(-100, 100), 2**n)
    print(L)
    print(FFT(L, xi))


test_FFT_addition(10)
