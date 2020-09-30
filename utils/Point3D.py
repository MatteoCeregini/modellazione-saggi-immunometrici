from math import sqrt


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, point):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    def distance_squared(self, point):
        return (point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2

    def subtraction(self, point):
        return Point3D(self.x - point.x, self.y - point.y, self.z - point.z)

    def sum(self, point):
        return Point3D(self.x + point.x, self.y + point.y, self.z + point.z)