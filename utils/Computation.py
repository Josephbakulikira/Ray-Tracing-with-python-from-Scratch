from utils.Tuples import *
from utils.Ray import *
from constants import *

class Computations:
    def __init__(self, t, shape, point, eyev, normalv):
        self.t = t
        self.shape = shape
        self.point = point
        self.eye_vector = eyev
        self.normal_vector = normalv
        self.inside = False
        self.over_point = Point.zeros()
        self.under_point = Point.zeros()
        self.reflect_vector = Vector3.zeros()

    def update(self):
        self.over_point = Point.add(self.point, point.multiply(self.normal_vector, EPSILON))
