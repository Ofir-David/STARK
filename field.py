print("loaded file field.py")


def innerGcd(n, m):  # n>m>0
    # returns an integer triple (d,a,b) such that d=a*n+b*m, under the assumption that
    # n>m>0
    q = n // m
    r = n - q * m
    if (r == 0):
        return (m, 0, 1)
    else:
        res = innerGcd(m, r)
        return (res[0], res[2], res[1] - q * res[2])


def gcd(n, m):
    # returns an integer triple (d,a,b) such that d=a*n+b*m
    if (m == 0):
        return (n, 1, 0)
    if (n == 0):
        return (m, 0, 1)
    signN = 1 if n > 0 else -1
    signM = 1 if m > 0 else -1
    n *= signN
    m *= signM
    if (n < m):
        res = innerGcd(m, n)
        return (res[0], res[2] * signN, res[1] * signM)
    else:
        res = innerGcd(n, m)
        return (res[0], res[1] * signN, res[2] * signM)


def checkGcd(n, m):
    res = gcd(n, m)
    print(f'the gcd of {n} and {m} is {res[0]}={n}*{res[1]}+{m}*{res[2]}')


def Convert(f):
    def wrapper(self, element):
        if (isinstance(element, int)):
            return f(self, element)
        if (isinstance(element, FieldElement)):
            return f(self, element.n)
        return NotImplemented

    return wrapper


def getValue(element):
    # returns the integer value of a field element in the range [0,_p), or the element itself
    # if it is an integer. Otherwise returns 1 (should change to NotImplemented?)
    if (isinstance(element, FieldElement)):
        return element.n
    if (isinstance(element, int)):
        return element
    return 1


class FieldElement:

    _p = 11  # (3 * 2 ** 30+1)

    @staticmethod
    def generator():
        return 2

    def __init__(this, n):
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
        return FieldElement(pow(this.n, power, this._p))

    # ------------------------------------------------------------------

    def __str__(this):
        return str(this.n)

    def __repr__(this):
        return str(this)

    def inv(this):
        if (this.n == 0):
            return 0  # raise sum error
        _, m, _ = gcd(this.n, this._p)
        return FieldElement(m)
