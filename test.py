from utils.Tuples import *
from utils.Color import Color
from utils.Matrix import Matrix
from utils.shapes import *
from utils.tools import *
from time import perf_counter
from utils.Ray import Ray
from utils.Transform import *
from math import pi,sqrt
from utils.Shader.Light import *
from utils.Shader.Material import *

m = Material()
pos = Point(0, 0, 0)
eyev = Vector3(0, -sqrt(2)/2, -sqrt(2)/2)
normalv = Vector3(0, 0, -1)
light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
result = Lighting(m, light, pos, eyev, normalv)
print(result)
