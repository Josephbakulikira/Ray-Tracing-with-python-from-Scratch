from utils.Tuples import Tuples
class Ray:
    def __init__(self, origin , direction ):
        self.origin = origin
        self.direction = direction

    def position(ray, t):
        return Tuples.add(ray.origin, Tuples.multiply(ray.direction, t))

    def __repr__(self):
        return f"origin -->{self.origin} \n, direction: {self.direction}"
