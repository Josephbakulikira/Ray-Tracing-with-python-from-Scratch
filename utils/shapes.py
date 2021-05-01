from utils.Tuples import Point, Vector3, Tuples
from utils.tools import *
from math import sqrt, pow
import numpy as np
from constants import *

class Shape:
    def __init__(self, position=Point.zeros()):
        self.id = id(self)
        self.position = position
        self.material = None
        self.transform = np.array([ [1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1] ] )
        self.name = "Default"

    def __repr__(self):
        return f'{self.name} ==> id: {self.id} \n position: {self.position}, material: {self.material}, \n transform: {self.transform}'


class Sphere(Shape):
    def __init__(self, position=Point.zeros()):
        super().__init__(position)
        self.material = None

    def GlassSphere(self):
        self.transform = np.identity(4)
        self.material = Material()
        self.material.transparency = 1.0
        self.material.refractive_index = 1.5

    def localIntersect(self, ray):
        sphereToRay = Tuples.sub(ray.origin, self.position)

        a = Tuples.dot(ray.direction, ray.direction)
        b = 2 * Tuples.dot(ray.direction, sphereToRay)
        c = Tuples.dot(sphereToRay, sphereToRay) - 1

        d = pow(b, 2) - 4 * a * c
        #d is the discriminant
        if d < 0:
            return []

        t1 = round( (-b - sqrt(d)) / (2 * a) ,5)
        t2 = round( (-b + sqrt(d)) / (2 * a) ,5)

        return [Intersection(t1, self), Intersection(t2, self)]

    def local_normal_at(self, point):
        return Tuples.sub(point, self.position)

class Plane(Shape):
    def __init__(self, position=Point.zeros()):
        super().__init__(position)
        self.material = None

    def localIntersect(self, ray):
        if abs(ray.direction.y) < EPSILON:
            return []
        t = round ((-ray.origin.y) / ray.direction.y, 5)
        return [Intersection(t, self)]

    def local_normal_at(self, point):
        return Vector3(0, 1, 0)
