def gcd(n, m):
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
        return (res[0], res[2] * signM, res[1] * signN)
    else:
        res = innerGcd(n, m)
        return (res[0], res[1] * signN, res[2] * signM)


def innerGcd(n, m):  # n>m>0
    q = n // m
    r = n - q * m
    if (r == 0):
        return (m, 0, 1)
    else:
        res = innerGcd(m, r)
        return (res[0], res[2], res[1]-q*res[2])


def checkGcd(n, m):
    res = gcd(n, m)
    print(f'the gcd of {n} and {m} is {res[0]}={n}*{res[1]}+{m}*{res[2]}')


class FieldElement:

    _p = 11  # (3 * 2 ** 30+1)

    def __init__(this, n):
        this.n = n % FieldElement._p  # might be negative, so
        if (this.n < 0):
            this.n += FieldElement._p

    def __add__(this, element):
        return FieldElement(this.n+element.n)

    def __sub__(this, element):
        return FieldElement(this.n-element.n)

    def __mul__(this, element):
        return FieldElement(this.n*element.n)

    def __truediv__(this, element):
        if (element.n == 0):
            return FieldElement(0)
        return FieldElement(this.n/element.n)

    def __pow__(this, power):
        pass

    def __str__(this):
        return str(this.n)

    def inv(this):
        if (this.n == 0):
            return 0  # raise sum error
        _, m, _ = gcd(this.n, this._p)
        return FieldElement(m)


e = FieldElement(4) * FieldElement(8)
print(e)
# print(e**3)
checkGcd(66, 1017)
print(e.inv())
