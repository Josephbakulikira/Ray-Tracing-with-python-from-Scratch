from math import pow , sqrt
from utils.Tuples import Tuples, Point
from utils.shapes import *
from utils.Ray import Ray
import operator
import numpy as np

class Intersection:
    def __init__(self, t, shape):
        self.t = t
        self.shape = shape

    def __repr__(self):
        return f't: {self.t}, objectId: {self.shape.id}'

def intersections(_xs):
    new_list = sorted(_xs, key=operator.attrgetter("t"))
    return new_list

def hit(xs):
    l = [ i.t for i in xs if i.t > 0]
    if len(l) > 0:
        val = min(l)
        for n in xs:
            if n.t == val:
                return n
    return None

def transform(ray, matrix):
    ## alternative way to make it if you decided to use the matrices that we coded
    # origin = multiplyMatrix(matrix, ray.origin.toMatrix()).toTuple()
    # direction = multiplyMatrix(matrix, ray.direction.toMatrix()).toTuple()

    origin = Tuples.toTuple( np.matmul(matrix, Tuples.toMatrix(ray.origin)) )
    direction = Tuples.toTuple(np.matmul(matrix, Tuples.toMatrix(ray.direction)) )
    return Ray(origin, direction)

def intersect(ray, shape):
    local_ray = transform(ray, np.linalg.inv(shape.transform))

    return shape.localIntersect(local_ray)

def normal_at(shape, world_point):
    local_point = Tuples.toTuple(np.matmul(np.linalg.inv(shape.transform), Tuples.toMatrix(world_point)))
    local_normal = shape.local_normal_at(local_point)
    world_normal = Tuples.toTuple(np.matmul(np.linalg.inv(shape.transform).transpose(), Tuples.toMatrix(local_normal)))
    world_normal = Vector3(world_normal.x, world_normal.y, world_normal.z)

    return Vector3.Normalize(world_normal)

def reflect(vec, normal):
    return Tuples.sub(vec, Tuples.multiply( Tuples.multiply(normal , 2) , Tuples.dot(vec, normal)) )
