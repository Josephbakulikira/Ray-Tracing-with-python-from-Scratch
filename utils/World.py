from utils.Shader.Light import *
from utils.Shader.Material import *
from utils.Tuples import *
from utils.shapes import *
from utils.Transform import *
from utils.tools import *

class World:
    def __init__(self):
        self.light = PointLight(Point(-10, 10, -10), Color.white())
        self.Objects = []

    def DefaultWorld(self):
        sphere1 = Sphere()
        self.Objects = []
        sphere1.material = Material(Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2)
        self.Objects.append(sphere1)
        sphere2 = Sphere()
        sphere2.transform = scaling(0.5, 0.5, 0.5)
        sphere2.material = Material(Color(0.3, 4.0, 0.8), 0.1, 0.7, 0.2)
        self.Objects.append(sphere2)
