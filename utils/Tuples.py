import numpy as np
from math import sqrt, pow

class Tuples:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(a, b):
        if a.w + b.w == 0:
            return Vector3(a.x + b.x, a.y + b.y , a.z + b.z)
        return Point(a.x + b.x, a.y + b.y , a.z + b.z)

    def sub(a, b):
        if a.w - b.w == 0:
            return Vector3(a.x - b.x, a.y - b.y , a.z - b.z)
        return Point(a.x - b.x, a.y - b.y , a.z - b.z)

    def multiply(tuple, s):

        if tuple.w == 0:
            return Vector3(tuple.x * s, tuple.y * s, tuple.z * s)
        return Point(tuple.x * s, tuple.y * s, tuple.z * s)

    def divide(tuple, d):
        if tuple.w == 0:
            return Vector3(tuple.x / d, tuple.y / d, tuple.z / d)
        return Point(tuple.x / d, tuple.y * s, tuple.z / d)

    def reflect(vec, normal):
        return Tuples.sub(vec, Tuples.multiply(Tuples.multiply(normal, 2), Tuples.dot(vec, normal)))

    def NegateTuple(tuple):
        if tuple.w == 0:
            return Vector3(tuple.x * -1, tuple.y * -1, tuple.z * -1)
        return Point(tuple.x * -1, tuple.y * -1, tuple.z * -1)

    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    def cross(a, b):
        return Vector3((a.y * b.z) - (a.z * b.y),
                       (a.z * b.x) - (a.x * b.z),
                       (a.x * b.y) - (a.y * b.x))

    def toTuple(matrix):
        if matrix[3][0] == 0:
            return Vector3(matrix[0][0], matrix[1][0], matrix[2][0])
        return Point(matrix[0][0], matrix[1][0], matrix[2][0])

    def toMatrix(tuple):
        return np.array([ [tuple.x], [tuple.y], [tuple.z], [tuple.w] ])


class Vector3(Tuples):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.w = 0

    def zeros():
        return Vector3(0, 0, 0)

    def units():
        return Vector3(1, 1, 1)

    def GetMagnitude(v):
        return sqrt(pow(v.x, 2) + pow(v.y, 2) + pow(v.z, 2) + pow(v.w, 2))

    def Normalize(v):
        mag = sqrt(pow(v.x, 2) + pow(v.y, 2) + pow(v.z, 2) + pow(v.w, 2))

        try:
            return Vector3(v.x/mag, v.y/mag, v.z/mag)
        except ZeroDivisionError:
            return Vector3(0, 0, 0)

    def __repr__(self):
        return f'Vector3 --> ( x: {self.x}, y: {self.y}, z: {self.z})'


class Point(Tuples):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.w = 1

    def zeros():
        return Point(0, 0, 0)

    def units():
        return Point(1, 1, 1)

    def __repr__(self):
        return f'Point --> ( x: {self.x}, y: {self.y}, z: {self.z})'
