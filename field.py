import math

print("loaded file field.py")


def _innerGcd(n, m):  # n>m>0
    """
    returns a triple (d,a,b) such that d=a*n+b*m under the assumption that n>m>0.
    In particular d=gcd(n,m)
    """
    q = n // m
    r = n - q * m
    if (r == 0):
        return (m, 0, 1)
    else:
        res = _innerGcd(m, r)
        return (res[0], res[2], res[1] - q * res[2])


def gcd(n, m):
    """
    returns a triple (d,a,b) such that d=a*n+b*m. In particular d=gcd(n,m).
    If both n=m=0, then returns (0,1,0), so that 0=gcd(0,0)
    """
    if (m == 0):
        return (n, 1, 0)
    if (n == 0):
        return (m, 0, 1)
    signN = 1 if n > 0 else -1
    signM = 1 if m > 0 else -1
    n *= signN
    m *= signM
    if (n < m):
        res = _innerGcd(m, n)
        return (res[0], res[2] * signN, res[1] * signM)
    else:
        res = _innerGcd(n, m)
        return (res[0], res[1] * signN, res[2] * signM)


def getValue(element):
    # returns the integer value of a field element in the range [0,_p), or the element itself
    # if it is an integer. Otherwise returns 1 (should change to NotImplemented?)
    if (isinstance(element, FieldElement)):
        return element.n
    if (isinstance(element, int)):
        return element
    return NotImplemented


def Convert(f):
    def wrapper(self, element):
        value = getValue(element)
        if (value == NotImplemented):
            return NotImplemented
        return f(self, value)

    return wrapper


class FieldElement:

    _p = 17  # (3 * 2 ** 30+1)

    @staticmethod
    def generator():
        return FieldElement(3)

    def generatorInv():
        return FieldElement(6)

    def __init__(this, n):
        # should change the n variable into property so it will always be mod _p
        this.n = getValue(n) % FieldElement._p  # might be negative, so
        # For some reason, in java you could get negative numbers...
        # if (this.n < 0):
        #    this.n += FieldElement._p

    # The @element parameter in the following can be either FieldElement or integer
    # Any other type will return NotImplemented, so it can try to use the same operator on
    # the element parameter (e.g. element.__add__(self) )
    @Convert
    def __eq__(this, element):
        return this.n == element % FieldElement._p

    def __req__(this, element):
        return this == element

    # ----------------------- arithmetics -------------------------

    @Convert
    def __add__(this, element):
        return FieldElement(this.n + element)

    @Convert
    def __radd__(this, element):
        return FieldElement(this.n + element)

    @Convert
    def __sub__(this, element):
        return FieldElement(this.n - element)

    @Convert
    def __rsub__(this, element):
        return FieldElement(element - this.n)

    @Convert
    def __mul__(this, element):
        return FieldElement(this.n * element)

    @Convert
    def __rmul__(this, element):
        return FieldElement(this.n * element)

    @Convert
    def __truediv__(this, element):
        return this * FieldElement(element).inv()

    @Convert
    def __rtruediv__(this, element):
        return element * this.inv()

    def __pow__(this, power):
        if (this == 0):
            return this
        # if batch_pow doesn't do any multiplication, it will just return 1 as a number
        if (power == 0):
            return FieldElement(1)
        if (power > 0):
            base = this
        else:
            base = this.inv()
            power = -power
        return batch_pow(base, [power])[0]
        # return FieldElement(pow(this.n, power, this._p))

    def __abs__(this):
        return this

    # ------------------------------------------------------------------

    def __str__(this):
        return str(this.n)

    def __repr__(this):
        return str(this)

    def inv(this):
        if (this.n == 0):
            raise ZeroDivisionError
        _, m, _ = gcd(this.n, this._p)
        return FieldElement(m)


def batch_pow(x, L):
    max_power = max(L)
    results = [1 for _ in L]
    if (max_power == 0):
        return res
    n_bits = int(math.log2(max_power)) + 1
    for i in range(n_bits):
        mask = 1 << i
        for j in range(len(L)):
            if (L[j] & mask):
                results[j] *= x
        x *= x
    return results


def batch_inv(L):
    mults = [FieldElement(1)]
    for elem in L:
        mults.append(mults[-1] * elem)
    inverse = mults[-1].inv()
    res = [0 for _ in L]
    for i in range(len(L)):
        res[- 1 - i] = mults[-2 - i] * inverse
        inverse *= L[-1 - i]
    return res
