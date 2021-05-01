from utils.Color import *
from math import floor, sqrt, pow
from utils.Tuples import *

import numpy as np

identity = np.identity(4)
class Pattern:
    def __init__(self, primary, secondary, transform_matrix):
        self.primary = primary
        self.secondary = secondary
        self.transform = transform_matrix

class StripePattern(Pattern):
    def __init__(self, primary=Color.white(), secondary=Color(), transform_matrix=identity):
        super().__init__(primary, secondary, transform_matrix)

    def pattern_at(self, pattern, point):
        if floor(point.x) % 2 == 0:
            return pattern.primary
        else:
            return pattern.secondary

class TestPattern(Pattern):
    def __init__(self, primary=Color.white(), secondary=Color(), transform_matrix=identity):
        super().__init__(primary, secondary, transform_matrix)

    def pattern_at(self, pattern, point):
        return Color(point.x, point.y, point.z)

class GradientPattern(Pattern):
    def __init__(self, primary=Color.white(), secondary=Color(), transform_matrix=identity):
        super().__init__(primary, secondary, transform_matrix)

    def pattern_at(self, pattern, point):
        dist = Color.sub(pattern.secondary, pattern.primary)
        fraction = point.x - floor(point.x)
        return  Color.add(pattern.primary, Color.multiply(dist, fraction))

class CheckerPattern(Pattern):
    def __init__(self, primary=Color.white(), secondary=Color(), transform_matrix=identity):
        super().__init__(primary, secondary, transform_matrix)

    def pattern_at(self, pattern, point):
        if (floor(point.x) + floor(point.y) + floor(point.z)) % 2 == 0:
            return pattern.primary
        else:
            return pattern.secondary

class RingPattern(Pattern):
    def __init__(self, primary=Color.white(), secondary=Color(), transform_matrix=identity):
        super().__init__(primary, secondary, transform_matrix)

    def pattern_at(self, pattern, point):
        if floor(sqrt(pow(point.x, 2) + pow(point.z, 2))) % 2 == 0:
            return pattern.primary
        else:
            return pattern.secondary

class BlendedPattern:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.transform = identity

    def pattern_at(self, pattern, point):
        c1 = pattern.a.pattern_at(pattern.a, point)
        c2 = pattern.b.pattern_at(pattern.b, point)

        c3 = Color.add(c1, c2)
        return Color(c3.r/2, c3.g/2, c3.b/2)

def pattern_at_object(pattern, object, point):
    object_point = Tuples.toTuple( np.matmul(np.linalg.inv(object.transform), Tuples.toMatrix(point)) )
    pattern_point = Tuples.toTuple(np.matmul(np.linalg.inv(pattern.transform), Tuples.toMatrix(object_point)) )

    return pattern.pattern_at(pattern, pattern_point)
