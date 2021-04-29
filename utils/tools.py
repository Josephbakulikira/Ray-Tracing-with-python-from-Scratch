from math import pow, sqrt
from utils.Tuples import Tuples, Point, Vector3
from utils.shapes import *
from utils.Transform import *
from utils.Color import *
from utils.Ray import Ray
from utils.Computation import *
from utils.Shader.Light import *
from utils.Shader.Material import *
import numpy as np
import operator

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
    l = [i.t for i in xs if i.t > 0]
    if len(l) > 0:
        val = min(l)
        for n in xs:
            if n.t == val:
                return n
    return None

def transform(ray, matrix):
    origin = Tuples.toTuple(np.matmul(matrix, Tuples.toMatrix(ray.origin)))
    direction = Tuples.toTuple(np.matmul(matrix, Tuples.toMatrix(ray.direction)))
    return Ray(origin, direction)

def intersect(ray, shape):
    local_ray = transform(ray, np.linalg.inv(shape.transform))
    return shape.localIntersect(local_ray)

def normal_at(shape, world_point):
    local_point = Tuples.toTuple(np.matmul(np.linalg.inv(shape.transform), Tuples.toMatrix(world_point) ))
    local_normal = shape.local_normal_at(local_point)
    world_normal = Tuples.toTuple(np.matmul(np.linalg.inv(shape.transform).transpose(), Tuples.toMatrix(local_normal)))
    world_normal = Vector3(world_normal.x, world_normal.y, world_normal.z)

    return Vector3.Normalize(world_normal)

def view_transform(frm, to, up):
    forward = Vector3.Normalize(Tuples.sub(to, frm))
    upn = Vector3.Normalize(up)
    left = Tuples.cross(forward, upn)
    true_up = Tuples.cross(left, forward)

    orientation = np.array([ [left.x, left.y, left.z, 0],
                             [true_up.x, true_up.y, true_up.z, 0],
                             [-forward.x, -forward.y, -forward.z, 0],
                             [0, 0, 0, 1] ])

    return np.matmul(orientation, translation(-frm.x, -frm.y, -frm.z))

def intersect_world(world, ray):
    _intersections = []
    for ob in world.Objects:
        xs = intersect(ray, ob)
        for n in xs:
            _intersections.append(n)

    return _intersections

def color_at(w, r, remaining=0):
    i = intersect_world(w, r)
    if len(i) > 0:
        if(len(i)) == 1:
            if i[0].t > 0:
                comps = prepare_computations(i[0], r, i)
                return shade_hit(w, comps)
            else:
                return Color()
        h= hit(i)
        if h != None:
            comps = prepare_computations(h, r, i)
            return shade_hit(w, comps)
        else:
            return Color()

    else:
        return Color(0, 0, 0)

def prepare_computations(i, ray, new_xs=None):
    _point = Ray.position(ray, i.t)
    comps = Computations(i.t, i.shape, Ray.position(ray, i.t), Tuples.NegateTuple(ray.direction), normal_at(i.shape, _point))
    if Tuples.dot(comps.normal_vector, comps.eye_vector) < 0:
        comps.inside = True
        comps.normal_vector.negate()
    else:
        comps.inside = False


    comps.over_point = Tuples.add(comps.point, Tuples.multiply(comps.normal_vector, EPSILON))
    return comps

def shade_hit(world, comps):
    shadowed = is_shadowed(world, comps.over_point)
    return Lighting(comps.shape.material, world.light, comps.over_point, comps.eye_vector, comps.normal_vector, shadowed)

def is_shadowed(world, point):
    v = Tuples.sub(world.light.position, point)
    distance = Vector3.GetMagnitude(v)
    direction = Vector3.Normalize(v)
    r = Ray(point, direction)
    _intersections = intersect_world(world, r)
    h = hit(_intersections)
    if h != None and h.t < distance:
        return True
    else:
        return False
