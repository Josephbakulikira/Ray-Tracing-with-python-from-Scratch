from utils.Ray import *
from utils.Tuples import *
from math import pi, cos, sin, tan

class Camera:
    def __init__(self, hsize, vsize, fieldOfView):
        self.hSize = hsize
        self.vSize = vsize
        self.fieldOfView = fieldOfView
        self.transform = np.identity(4)
        self.halfView = round(tan(fieldOfView / 2), 5)
        self.aspect = round(hsize/ vsize, 5)
        self.halfWidth = 0
        self.halfHeight = 0

        if self.aspect >= 1:
            self.halfWidth = self.halfView
            self.halfHeight = self.halfView / self.aspect
        else :
            self.halfWidth = self.halfView * self.aspect
            self.halfHeight = self.halfView
        self.pixelSize = round( (self.halfWidth * 2) / self.hSize, 5)

    def Update(self):
        self.halfView = round(tan(self.fieldOfView / 2), 5)
        self.aspect = round(self.hSize/ self.vSize, 5)
        if aspect >= 1:
            self.halfWidth = self.halfView
            self.halfHeight = self.halfView * self.aspect
        else :
            self.halfWidth = self.halfView * self.aspect
            self.halfHeight = self.halfView
        self.pixelSize = (self.halfWidth * 2) / self.hSize

def ray_for_pixel(cam, px, py):
    x_offset = (px + 0.5) * cam.pixelSize
    y_offset = (py + 0.5) * cam.pixelSize
    world_x = round(cam.halfWidth  - x_offset, 5)
    world_y = round(cam.halfHeight  - y_offset, 5)

    # pixel = multiplyMatrix(MatrixInversion(cam.transform), Point(world_x, world_y, -1).toMatrix()).toTuple()
    # origin = multiplyMatrix(MatrixInversion(cam.transform), Point(0, 0, 0).toMatrix()).toTuple()

    pixel = Tuples.toTuple(np.matmul(np.linalg.inv(cam.transform), Tuples.toMatrix(Point(world_x, world_y, -1))))
    origin = Tuples.toTuple(np.matmul(np.linalg.inv(cam.transform), Tuples.toMatrix(Point(0, 0, 0)) ))

    direction = Vector3.Normalize(Tuples.sub(pixel, origin))
    return Ray(origin, direction)
