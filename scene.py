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
from utils.Shader.Light import *
from utils.Shader.Material import *

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
material = Material(Color(0.95, 0.48, 0.16))
s.material = material
light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))


start = perf_counter()
for y in range(resolution):
    world_y = half - pixel_size * y
    for x in range(resolution):
        world_x = - half + pixel_size * x
        position = Point(world_x, world_y, wall_z)
        r = Ray(r_origin, Vector3.Normalize(Tuples.sub(position , r_origin)))
        xs = intersect(r, s)
        val = hit(xs)
        if val != None:
            point = Ray.position(r, val.t)
            normal = normal_at(val.shape, point)
            eye = Tuples.negateTuple(r.direction)
            color = Lighting(val.shape.material, light, point, eye, normal)
            pixel(screen, x, y, color.ConvertColor())
            # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 1, 1))
            pygame.display.flip()
print(perf_counter() - start)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.image.save(screen,"./images/lightShaderSphere.jpg")

pygame.quit()
