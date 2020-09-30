from math import sqrt


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def distance_squared(self, point):
        return (point.x - self.x) ** 2 + (point.y - self.y) ** 2

    def dot_product(self, point):
        return self.x * point.x + self.y + point.y

    def orthogonal(self):
        return Point2D(-self.y, self.x)

    def subtraction(self, point):
        return Point2D(self.x - point.x, self.y - point.y)

    def sum(self, point):
        return Point2D(self.x + point.x, self.y + point.y)
