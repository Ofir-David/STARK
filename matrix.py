from .field import FieldElement, ExtElement, getElement

from typing import List, Tuple


class Matrix:

    @staticmethod
    def matrix_identity(n: int):
        elements: List[List[ExtElement]] = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            elements.append(row)  # type : ignore
        return Matrix(elements)

    def __init__(self, elements: List[List[ExtElement]]):
        self.n = len(elements)
        self.elements = []
        for row in elements:
            assert self.n == len(row), f'Each row need to have {self.n} entries'
            self.elements.append([getElement(elem) for elem in row])

    def _valid_key(self, key: Tuple[int, int]):
        return 0 <= key[0] < self.n and 0 <= key[1] < self.n

    def __getitem__(self, key: Tuple[int, int]) -> FieldElement:
        assert self._valid_key(key)
        return self.elements[key[0]][key[1]]

    def __setitem__(self, key: Tuple[int, int], value: ExtElement):
        assert self._valid_key(key)
        self.elements[key[0]][key[1]] = getElement(value)

    def switch_rows(self, row1: int, row2: int):
        temp = self.elements[row1]
        self.elements[row1] = self.elements[row2]
        self.elements[row2] = temp

    def scalar_mult_row(self, row: int, scalar: ExtElement):
        self.elements[row] = [scalar * entry for entry in self.elements[row]]

    def add_row_times_scalar(self, row_from: int, row_to: int, scalar: ExtElement):
        self.elements[row_to] = [scalar * from_elem + to_elem
                                 for from_elem, to_elem
                                 in zip(self.elements[row_from], self.elements[row_to])]

    def _fix_col(self, row: int, col: int, mat: 'Matrix', inv: 'Matrix'):
        mat.switch_rows(row, col)
        inv.switch_rows(row, col)
        elem = mat[col, col]
        elem_inv = elem.inv()
        mat.scalar_mult_row(col, elem_inv)
        inv.scalar_mult_row(col, elem_inv)
        for i in range(self.n):
            if i == col:
                continue
            value = mat[i, col]
            mat.add_row_times_scalar(col, i, 0 - value)
            inv.add_row_times_scalar(col, i, 0 - value)

    def inverse(self):
        temp = Matrix(self.elements)
        inverse_mat = Matrix.matrix_identity(self.n)
        print('\n**************')
        print(temp.elements)
        print(inverse_mat.elements)
        for column in range(self.n):
            # column i:
            for row in range(self.n):
                if temp[row, column] != 0:
                    self._fix_col(row, column, temp, inverse_mat)
                    print('\n**************')
                    print(temp.elements)
                    print(inverse_mat.elements)
                    break
            else:
                raise Exception(f'could not fix column {column}')

        return inverse_mat

    def mult_vector(self, L: List[ExtElement]):
        assert self.n == len(L)
        return [sum(self[i, j] * L[j] for j in range(self.n)) for i in range(self.n)]
