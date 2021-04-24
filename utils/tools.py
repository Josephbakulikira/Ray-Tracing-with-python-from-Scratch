from math import pow , sqrt, sin, cos
from utils.Tuples import Tuples, Point
from utils.shapes import *
from utils.Ray import Ray
from utils.World import *
from utils.Computation import *
from utils.Transform import *
from constants import *
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

def color_at(w, r, remaining):
    i = intersect_world(w, r)
    if len(i) > 0:
        if(len(i)) == 1:
            if i[0].t > 0:
                comps = prepare_computations(i[0], r, i)
                return shade_hit(w, comps, remaining)
            else:
                return Color()
        # print([ire.t for ire in i])
        h = hit(i)
        if h != None:
            comps = prepare_computations(h, r, i)
            return shade_hit(w, comps, remaining)
        else:
            return Color()
    else:
        return Color(0, 0, 0)

def prepare_computations(i, ray, new_xs=None):
    _point = Ray.position(ray, i.t)
    comps = Computations(i.t, i.shape, Ray.position(ray, i.t), Tuples.negateTuple(ray.direction), normal_at(i.shape, _point))
    # comps.point = Ray.position(ray, comps.t)
    if Tuples.dot(comps.normal_vector, comps.eye_vector) < 0:
        comps.inside = True
        comps.normal_vector.negate()
    else:
        comps.inside = False
    comps.reflect_vector = Tuples.reflect(ray.direction, comps.normal_vector)

    if new_xs != None:
        containers = []
        for index in range(len(new_xs)):
            # print(hit(xs))
            if  new_xs[index] == i:
                if len(containers) == 0:
                    comps.n1 = Vacuum
                else:
                    comps.n1 = containers[-1].material.refractive_index

            if new_xs[index].shape in containers:
                # print(xs[index].object.id)
                containers.remove(new_xs[index].shape)
            else:
                containers.append(new_xs[index].shape)

            if new_xs[index] == i:
                if len(containers) == 0:
                    comps.n2 = Vacuum
                else:
                    comps.n2 = containers[-1].material.refractive_index

                break

    comps.over_point = Tuples.add(comps.point, Tuples.multiply(comps.normal_vector, EPSILON))
    comps.under_point = Tuples.sub(comps.point, Tuples.multiply(comps.normal_vector, EPSILON))
    return comps

def shade_hit(world, comps, remaining):
    shadowed = is_shadowed(world, comps.over_point)
    surface = Lighting(comps.shape.material,comps.shape, world.light, comps.over_point, comps.eye_vector, comps.normal_vector, shadowed)
    reflected = ReflectedColor(world, comps, remaining)
    refracted = RefractedColor(world, comps, remaining)
    material = comps.shape.material
    if material.reflective > 0 and material.transparency > 0:
        reflectance = schlick(comps)
        return Color.add( Color.add(surface, Color.multiply(reflected, reflectance)), Color.multiply(refracted, (1-reflectance)) )
    else:
        return Color.add(surface, Color.add(reflected, refracted))

def is_shadowed(world, point):
    v = Tuples.sub(world.light.position, point)
    distance = Vector3.GetMagnitude(v)
    direction = Vector3.Normalize(v)
    r = Ray(point, direction)
    _intesections = intersect_world(world, r)

    h = hit(_intesections)
    if h != None and h.t < distance:
        return True
    else:
        return False

def ReflectedColor(world, comps, remaining):
    if remaining <= 0:
        return Color()
    if comps.shape.material.reflective == 0:
        return Color()
    reflect_ray = Ray(comps.over_point, comps.reflect_vector)
    color = color_at(world, reflect_ray, remaining - 1)
    return Color.multiply(color, comps.shape.material.reflective)

def RefractedColor(world, comps, remaining):
    if remaining <= 0 or comps.shape.material.transparency == 0:
        return Color()

    n_ratio = comps.n1 / comps.n2
    cos_i = Tuples.dot(comps.eye_vector, comps.normal_vector)
    sin2_t = round( n_ratio * n_ratio * (1 - (cos_i * cos_i) ),5)

    if sin2_t > 1:
        return Color()

    cos_t = round(sqrt(1.0 - sin2_t), 5)
    _direction = Tuples.sub(Tuples.multiply(comps.normal_vector,  (n_ratio * cos_i) - cos_t ) , Tuples.multiply(comps.eye_vector, n_ratio))

    refract_ray = Ray(comps.under_point, _direction)
    # print(comps.shape.material.transparency)
    new_color = color_at(world, refract_ray, remaining - 1)
    return Color.multiply(new_color, comps.shape.material.transparency)

def schlick(comps):
    # cosine of the angle between the eye vector and the normal vector
    angle_cos = Tuples.dot(comps.eye_vector, comps.normal_vector)
    
    # total internal reflection occur only if n1 > n2
    if comps.n1 > comps.n2:

        n = round(comps.n1 / comps.n2, 5)
        sin2_t = ( n * n ) * (1 - (angle_cos * angle_cos) )
        if sin2_t > 1.0:
            return 1.0

        cos_t = sqrt(1.0 - sin2_t)
        # angle_cos = cos_t

    r0 = pow(round( ((comps.n1 - comps.n2) / (comps.n1 + comps.n2)), 5),2)
    return  round(r0 + ( 1 - r0) * pow(( 1 - angle_cos), 5), 5)
