import pygame
from time import perf_counter
from pygame.gfxdraw import pixel

from utils.Tuples import *
from utils.Color import Color
from utils.Matrix import Matrix
from utils.shapes import *
from utils.tools import *
from time import perf_counter
from utils.Ray import Ray
from utils.Transform import *

width = 500
height = 500

size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

r_origin = Point(0, 0, -5)
wall_z = 10
wall_size = 7.0
resolution = 500
pixel_size = wall_size/ resolution
half = wall_size / 2
s = Sphere()
color = Color(1, 0, 0)

start = perf_counter()
for y in range(resolution):
    world_y = half - pixel_size * y
    for x in range(resolution):
        world_x = - half + pixel_size * x
        position = Point(world_x, world_y, wall_z)
        r = Ray(r_origin, Vector3.Normalize(Tuples.sub(position , r_origin)))
        xs = intersect(r, s)

        if hit(xs) != None:
            pixel(screen, x, y, (255, 0, 0))

pygame.display.flip()
print(perf_counter() - start)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.image.save(screen,"./images/simpleSphere.jpg")

pygame.quit()
