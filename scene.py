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
from utils.Camera import *
from utils.World import *
import numpy as np
from math import sin, cos, pi

width, height = 500, 300

size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

floor = Plane()
floor.transform = scaling(10, 0.01, 10)
floor.material = Material()
floor.material.color = Color(1, 0.9, 0.9)
floor.material.specular = 0

middle = Sphere()
middle.transform = translation(-0.5, 1, 0.5)
middle.material = Material()
middle.material.color = Color(0.81, 0.2, 0.4)
middle.material.diffuse = 0.7
middle.material.specular = 0.3

right = Sphere()
right.transform = np.matmul(translation(1.5, 0.5, -0.5), scaling(0.5, 0.5, 0.5))
right.material = Material()
right.material.color = Color(0.2, 0.51, 0.71)
right.material.diffuse = 0.7
right.material.specular = 0.3

world = World()
world.Objects = [floor, middle, right]
world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
cam = Camera(width, height, pi/3)
cam.transform = view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector3(0, 1, 0))

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

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.image.save(screen, "./images/scene2.jpg")
pygame.quit()
