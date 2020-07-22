from field import FieldElement


class Poly:

    def __init__(self):
        self.coef = [0]

    def __call__(self, elem):
        sum = FieldElement(0)
        t = FieldElement(1)
        for c in self.coef:
            sum += t * c
            t *= elem
        return sum

    def __str__(self):
        return "1"


p = Poly()

print(p(3))
