import numpy as np
from math import sqrt, pow, pi, cos, sin, floor
from copy import deepcopy

#this file will not be used at all, it's just for some
#explanation of how the matrices mathematics works behind the scenes
# we will not use this simply for some performance purposes

class Matrix:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.val = np.zeros((r, c))

    def updateInfo(self):
        self.row = len(self.val)
        self.col = len(self.val[0])

    def identityMatrix(matrix):
        r = matrix.col
        m = Matrix(r, r)
        y = 0
        for x in range(r):
            m.val[x][y] = 1
            y += 1
        return m

    def transpose(self):
        temp = [[0 for i in range(self.col)] for j in range(self.row)]
        for x in range(self.row):
            for y in range(self.col):
                temp[x][y] = self.val[y][x]

        self.val = temp

    def multiply(m1, m2):
        m = Matrix(m1.row, m2.col)

        if m1.col != m2.row:
            print("we can't multiply this two matrices")
            return None

        for x in range(m1.row):
            for y in range(m2.col):
                sum = 0
                for z in range(m1.col):
                    sum += m1.val[x][z] * m2.val[z][y]
                m.val[x][y] = round(sum, 5)

        return m

    def TransposeMatrix(m):
        m1 = Matrix(m.row, m.col)
        for x in range(m.row):
            for y in range(m.col):
                m1.val[x][y] = m.val[y][x]

        return m1

    def Determinant2x2(matrix):
        return matrix.val[0][0] * matrix.val[1][1] - matrix.val[0][1] * matrix.val[1][0]

    def submatrix(matrix, row, column):
        temp = deepcopy(matrix)
        temp.val = np.delete(temp.val, row, 0)
        temp.val = np.delete(temp.val, column, 1)
        temp.updateInfo()
        return temp

    def Minor3x3(matrix, row, column):
        s = Matrix.submatrix(matrix, row, column)
        if len(s.val) > 2:
            return Matrix.Determinant(s)
        else:
            return Matrix.Determinant2x2(s)

    def Cofactor3x3(matrix, row, column):
        minor = Matrix.Minor3x3(matrix, row, column)
        if (row + column) % 2 == 0:
            return minor
        else:
            return -minor

    def Determinant(matrix):
        if matrix.row == 2:
            return Matrix.Determinant2x2(matrix.val)
        else:
            d = 0
            for j in range(len(matrix.val[0])):
                c = Matrix.Cofactor3x3(matrix, 0, j)
                d += c * matrix.val[0][j]
            return d

    def MatrixInversion(matrix):
        d = Matrix.Determinant(matrix)
        if d == 0:
            print("this matrix is not invertible")
            return None

        new = Matrix(matrix.row, matrix.col)
        for x in range(matrix.row):
            for y in range(matrix.col):
                new.val[x][y] = round(Matrix.Cofactor3x3(matrix, x, y)/ d, 6)
        new.transpose()
        return new

    def __repr__(self):
        return f'{self.val}'
