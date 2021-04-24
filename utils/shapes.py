from utils.Tuples import Point, Vector3, Tuples
from constants import *
from math import sqrt, pow
from utils.tools import *
import numpy as np

class Shape:
    def __init__(self, position=Point.zeros()):
        self.id = id(self)
        self.position = position
        self.material = None
        self.transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.name = "Default"

    def __repr__(self):
        return f'{self.name} ==> id: {self.id} \n position: {self.position}, material: {self.material}, \n transform: {self.transform}'


class Sphere(Shape):
    def __init__(self, position = Point.zeros()):
        super().__init__(position)
        self.material = None

    def localIntersect(self, ray):
        # ray = transform(ray, NumpyMatrixInversion(self.transform))
        sphereToRay = Tuples.sub(ray.origin, self.position)

        a = Tuples.dot(ray.direction, ray.direction)
        b = 2 * Tuples.dot(ray.direction, sphereToRay)
        c = Tuples.dot(sphereToRay, sphereToRay) - 1

        d = pow(b, 2) - 4 * a * c

        if d < 0:
            return []

        t1 = round((-b - sqrt(d) )/ (2 * a), 5)
        t2 = round((-b + sqrt(d) )/ (2 * a), 5)

        return [Intersection(t1, self), Intersection(t2, self)]

    def local_normal_at(self, point):
        return Tuples.sub(point, Point.zeros())

class GlassSphere(Shape):
    def __init__(self, position = Point.zeros()):
        super().__init__(position)
        self.material = Material()
        self.material.transparency = 0.9
        self.material.refractive_index = Glass
        self.material.shininess = 300.0
        self.material.diffuse = 0.1
        self.material.ambient = 0
        self.material.specular = 0.9
        self.material.color = Color.white()
        

    def localIntersect(self, ray):
        # ray = transform(ray, NumpyMatrixInversion(self.transform))
        sphereToRay = Tuples.sub(ray.origin, self.position)

        a = Tuples.dot(ray.direction, ray.direction)
        b = 2 * Tuples.dot(ray.direction, sphereToRay)
        c = Tuples.dot(sphereToRay, sphereToRay) - 1

        d = pow(b, 2) - 4 * a * c

        if d < 0:
            return []

        t1 = round((-b - sqrt(d) )/ (2 * a), 5)
        t2 = round((-b + sqrt(d) )/ (2 * a), 5)

        return [Intersection(t1, self), Intersection(t2, self)]

    def local_normal_at(self, point):
        return Tuples.sub(point, Point.zeros())

class Plane(Shape):
    def __init__(self, position=Point.zeros()):
        super().__init__(position)

    def localIntersect(self, ray):
        if abs(ray.direction.y) < EPSILON:
            return []
        t = round ((-ray.origin.y) / ray.direction.y, 5)
        return [Intersection(t, self)]

    def local_normal_at(self, point):
        return Vector3(0, 1, 0)
