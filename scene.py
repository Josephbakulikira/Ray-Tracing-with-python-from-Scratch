import pygame
# import multiprocessing as mp
# import concurrent.futures
# import itertools
from time import perf_counter
from pygame.gfxdraw import pixel
import numpy as np
from utils.Tuples import *
from utils.Color import Color
from utils.Matrix import Matrix
from utils.shapes import *
from utils.tools import *
from utils.Ray import Ray
from utils.Transform import *
from utils.Shader.Light import *
from utils.Shader.Material import *
from utils.Camera import *
from utils.World import *
from utils.Shader.Patterns import *
from math import pi, cos, sin

width = 500
height = 500

size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60


Floor = Plane()
Floor.material = Material()
Floor.transform = np.matmul( translation(0, 0, 10), rotation_x(pi/2))
Floor.material.pattern = CheckerPattern(Color(0.15, 0.15, 0.15), Color(0.85,0.85, 0.85))
Floor.material.ambient = 0.8
Floor.material.diffuse = 0.2
Floor.material.specular = 0;

glassSphere = Sphere()
glassSphere.material = Material()
glassSphere.material.diffuse = 0.1
glassSphere.material.shininess = 300.0
glassSphere.material.transparency = 0.9
glassSphere.material.reflective = 0.9
glassSphere.material.refractive_index = 1.52
glassSphere.material.ambient = 0
glassSphere.material.color = Color.white()
glassSphere.material.specular = 0.9

airSphere = Sphere()
airSphere.transform = scaling(0.5, 0.5, 0.5)
airSphere.material = Material()
airSphere.material.color = Color.white()
airSphere.material.diffuse = 0
airSphere.material.shininess = 300.0
airSphere.material.reflective = 0.9
airSphere.material.transparency = 0.9
airSphere.material.ambient = 0
airSphere.material.specular = 0.9
airSphere.material.refractive_index = 1.0000034

world = World()
world.Objects = [Floor, glassSphere, airSphere]
world.light = PointLight(Point(2, 10, -5), Color(0.9, 0.9, 0.9))
cam = Camera(width, height, 0.45)
cam.transform = view_transform(Point(0,0, -5), Point(0, 0, 0), Vector3(0, 1, 0))

def PixelRender(x, y):
    global cam, world
    ray = ray_for_pixel(cam, x, y)
    color = color_at(world, ray, 5)
    pixel(screen, x, y, color.ConvertColor())
    pygame.display.update()

def render(camera, world):
    global width, height, size, screen
    width, height = camera.hSize, camera.vSize
    size = (width, height)
    screen = pygame.display.set_mode(size)

    for x in range(width):
        for y in range(height):
            PixelRender(x, y)

start_time = perf_counter()
render(cam, world)

print(perf_counter() - start_time)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.image.save(screen,"./images/reflectionRefraction.jpg")

pygame.quit()
