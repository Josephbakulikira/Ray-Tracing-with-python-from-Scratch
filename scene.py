import pygame
from time import perf_counter
from pygame.gfxdraw import pixel

from utils.Tuples import *
from utils.Color import *
from utils.shapes import *
from utils.Ray import Ray
from utils.tools import *
from utils.Transform import *
from utils.Shader.Light import *
from utils.Shader.Material import *
from utils.Shader.Pattern import *
from utils.Camera import *
from utils.World import *
from utils.Shader.Pattern import *
from constants import *
import numpy as np
from math import sin, cos, pi

width, height = 1920, 1080

size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

Floor = Plane()
Floor.material = Material()
Floor.material.pattern = CheckerPattern()
Floor.material.reflection = 0.4
Floor.material.ambient = 0.8
Floor.material.diffuse = 0.2
Floor.material.specular = 0.2;

_sphere = Sphere()
_sphere.transform = translation(0, 1, -0.5)
_sphere.material = Material()
_sphere.material.diffuse = 0.1
_sphere.material.shininess = 200.0
_sphere.material.transparency = 0
_sphere.material.reflective = 0.6
_sphere.material.refractive_index = 1.52
_sphere.material.ambient = 0.6
_sphere.material.color = Color(1, 0, 0)
_sphere.material.specular = 0.6

_sphere2 = Sphere()
_sphere2.transform = np.matmul(translation(1.7, 0.7, -0.9), scaling(0.7, 0.7, 0.7) )
_sphere2.material = Material()
_sphere2.material.diffuse = 0.4
_sphere2.material.shininess = 200.0
_sphere2.material.transparency = 0
_sphere2.material.reflective = 0.2
_sphere2.material.refractive_index = 1.52
_sphere2.material.ambient = 0.8
_sphere2.material.color = Color(0.1, 0.3, 1)
_sphere2.material.specular = 0.8
# glassSphere.transform = scaling(0.5, 0.5, 0.5)

# airSphere = Sphere()
# airSphere.transform = scaling(0.5, 0.5, 0.5)
# airSphere.material = Material()
# airSphere.material.color = Color.white()
# airSphere.material.diffuse = 0
# airSphere.material.shininess = 300.0
# airSphere.material.reflective = 0.9
# airSphere.material.transparency = 0.9
# airSphere.material.ambient = 0
# airSphere.material.specular = 0.9
# airSphere.material.refractive_index = 1.0000034


world = World()
world.Objects = [Floor, _sphere, _sphere2]
world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
cam = Camera(width, height, pi/3)
cam.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector3(0, 1, 0))

# cam.transform = view_transform(Point(0,0, -5), Point(0, 0, 0), Vector3(0, 1, 0))

def PixelRender(x, y):
    global cam, world
    ray = ray_for_pixel(cam, x, y)
    color = color_at(world, ray)
    pixel(screen, x, y, color.ConvertColor())
    pygame.display.flip()

def render(camera, world):
    global width, height, size, screen
    width, height = camera.hSize, camera.vSize
    size = (width, height)
    screen = pygame.display.set_mode(size)

    for x in range(width):
        for y in range(height):
            PixelRender(x, y)

render(cam, world)
#
# w = World()
# r = Ray(Point(0,0 , -3), Vector3(0, -(sqrt(2))/2 , sqrt(2)/2))
# floor = Plane()
# floor.transform = translation(0, -1, 0)
# floor.material = Material()
# floor.material.reflective = 0.5
# floor.material.transparency = 0.5
# floor.material.refractive_index = 1.5
#
# w.Objects.append(floor)
# ball = Sphere()
# ball.material = Material()
# ball.material.color = Color(1, 0, 0)
# ball.material.ambient = 0.5
# ball.transform = translation(0, -3.5, -0.5)
# w.Objects.append(ball)
# xs = intersections([Intersection(sqrt(2), floor)])
# comps = prepare_computations(xs[0], r, xs)
# c = shade_hit(w, comps, 5)
# print(c)

# r = Ray( Point(0, 1, -1), Vector3(0, -(sqrt(2))/2 , sqrt(2)/2) )

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
pygame.image.save(screen, "./images/sceneReflection.jpg")
pygame.quit()
