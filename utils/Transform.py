import numpy as np
from math import sqrt, pow, pi, cos, sin, floor

def convertToRadian(degree):
    return (degree * pi/ 180)

def translation(x, y, z):
    return np.array([[1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])

def scaling(x, y, z):
    return np.array([[x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]])

def rotation_x(rad):
    return np.array([[1, 0, 0, 0],
             [0, cos(rad), -sin(rad), 0],
             [0, sin(rad), cos(rad), 0],
             [0, 0, 0, 1]])

def rotation_y(rad):
    return np.array([[cos(rad), 0, sin(rad), 0],
             [0, 1, 0, 0],
             [-sin(rad), 0, cos(rad), 0],
             [0, 0, 0, 1]])

def rotation_z(rad):
    return np.array([[cos(rad), -sin(rad), 0, 0],
             [sin(rad), cos(rad), 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]])

def Shearing(xy, xz, yx, yz, zx, zy):
    return np.array([[1, xy, xz, 0],
             [yx, 1, yz, 0],
             [zx, zy, 1, 0],
             [0, 0, 0, 1]])
