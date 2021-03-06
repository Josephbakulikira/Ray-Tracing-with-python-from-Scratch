from utils.Tuples import *
from utils.Color import Color
from utils.tools import *
from utils.Shader.Pattern import *
from math import pow

class Light:
    def __init__(self, position, intensity):
        self.id = id(self)
        self.position = position
        self.intensity = intensity
        self.name = "DefaultLight"

    def __repr__(self):
        return f'{self.name}, id: {self.id}, intensity: {self.intensity}, \n position: {self.position}'

class PointLight(Light):
    def __init__(self, position=Point.zeros(), intensity=Color.white()):
        super().__init__(position, intensity)


def Lighting(material, obj, light, point, eyev, normalv, inShadow=None):

    color = Color()
    if material.pattern != None:
        color = pattern_at_object(material.pattern, obj, point)
    else:
        color = material.color

    effective_color = Color.multiply(color, light.intensity)
    lightv = Vector3.Normalize(Tuples.sub(light.position, point))
    ambient = Color.multiply(effective_color, material.ambient)
    light_dot_normal = Tuples.dot(lightv, normalv)

    if light_dot_normal < 0 or inShadow==True:
        diffuse = Color()
        specular = Color()

    else:
        diffuse = Color.multiply(effective_color, material.diffuse * light_dot_normal)
        reflectv = Tuples.reflect(Tuples.NegateTuple(lightv), normalv)
        reflect_dot_eye = Tuples.dot(reflectv, eyev)

        if reflect_dot_eye <= 0:
            specular = Color()
        else:
            factor = pow(reflect_dot_eye , material.shininess)
            specular = Color.multiply(light.intensity, material.specular * factor)

    return Color.add(Color.add(ambient, diffuse), specular)
