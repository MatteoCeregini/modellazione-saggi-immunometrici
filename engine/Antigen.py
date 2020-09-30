import math

from sat_collision_detection.ConvexPolygon2DSAT import ConvexPolygon2DSAT
from utils.Point2D import Point2D


class Antigen:
    def __init__(self, center_point, radius):
        self.center_point = center_point
        self.center_point_2d = Point2D(self.center_point.x, self.center_point.z)
        self.radius = radius
        self.box = ConvexPolygon2DSAT(self.get_vertices_circle())

    def overlaps_with_antigen(self, antigen):
        return self.center_point.distance_squared(antigen.center_point) <= (self.radius + antigen.radius) ** 2

    def contains(self, point):
        return (point.x - self.center_point.x) ** 2 + (point.y - self.center_point.y) ** 2 + (point.z - self.center_point.z) ** 2 <= self.radius ** 2

    def get_vertices_circle(self):
        step = 15
        vertices = []
        for alpha in range(0, 361, step):
            x = self.radius * math.cos(alpha) + self.center_point_2d.x
            y = self.radius * math.sin(alpha) + self.center_point_2d.y
            vertices.append(Point2D(x, y))
        return vertices
