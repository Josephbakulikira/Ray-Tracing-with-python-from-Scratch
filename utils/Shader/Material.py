from utils.Color import Color

class Material:
    def __init__(self, color= Color(1,1,1), ambient=0.1, diffuse=0.9, specular=0.9):
        self.id = id(self)
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = 200.0
        self.reflective = 0.0
        self.refractive_index = 1.0
        self.transparency = 0
        self.pattern = None
        self.name = "DefaultMaterial"

    def __repr__(self):
        return f'{self.name}, {self.color} \n, {self.id}'
