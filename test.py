from utils.Tuples import *
from utils.Color import Color
from utils.Matrix import *
from utils.shapes import *
from utils.tools import *
import numpy as np
from time import perf_counter
from utils.Ray import Ray

r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
s = Sphere()
i1 = Intersection(2, s)
i2 = Intersection(5, s)
i3 = Intersection(8, s)
i4 = Intersection(-8, s)
i5 = Intersection(-2, s)

xs = intersections([i1, i2, i3, i4, i5])
xs = hit(xs)
print(xs)
# print(perf_counter() - start)
