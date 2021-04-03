from utils.Tuples import *
from utils.Color import Color
from utils.Matrix import Matrix
from utils.shapes import *
from utils.tools import *
from time import perf_counter
from utils.Ray import Ray
from utils.Transform import *

r = Ray(Point(1, 2, 3), Vector3(0, 1, 0))
m = scaling(2, 3, 4)
r2 = transform(r, m)
print(r2)
# print(perf_counter() - start)
