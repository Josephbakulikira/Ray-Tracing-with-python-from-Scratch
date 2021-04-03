class Color:
    def __init__(self, red = 0, green = 0 , blue = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def white():
        return Color(1, 1, 1)

    def multiply(a, b):
        if type(b) == Color:
            #known as the hadamart product
            return Color(a.red * b.red, a.green * b.green, a.blue * b.blue)
        return Color(a.red * b, a.green * b, a.blue * b)

    def add(a, b):
        return Color(a.red + b.red, a.green + b.green, a.blue + b.blue)

    def sub(a, b):
        return Color(a.red - b.red, a.green - b.green, a.blue - b.blue)

    def ConvertColor(self):
        r, g, b = 0, 0, 0
        if self.red * 255 > 255:
            r = 255
        else:
            r = self.red * 255
        if self.green * 255 > 255:
            g = 255
        else:
            g = self.green * 255
        if self.b * 255 > 255:
            b = 255
        else:
            b = self.blue * 255
        return (r, g, b)

    def __repr__(self):
        return f'color --> r: {self.red}, g: {self.green}, b: {self.blue}'
