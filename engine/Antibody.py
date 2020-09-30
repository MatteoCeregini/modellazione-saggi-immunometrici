import math

from sat_collision_detection.ConvexPolygon2DSAT import ConvexPolygon2DSAT
from utils.Point2D import Point2D


class Antibody:
    def __init__(self, orientation, center_point, a, b, c, theta):
        self.orientation = orientation
        if self.orientation == 1:  # End on fab-up
            self.empty_antigen_binding_sites = 2
        elif self.orientation == 2:  # End on fab-down
            self.empty_antigen_binding_sites = 0
        elif self.orientation == 3:  # Side on
            self.empty_antigen_binding_sites = 1
        else:  # Flat on
            self.empty_antigen_binding_sites = 0
        self.center_point = center_point
        self.center_point_2d = Point2D(self.center_point.x, self.center_point.z)
        self.a = a
        self.b = b
        self.c = c
        self.theta = theta
        self.vertices_3d = None
        self.box = ConvexPolygon2DSAT(self.get_vertices_ellipse())

    def get_vertices_ellipse(self):
        step = 15
        vertices = []
        for alpha in range(0, 361, step):
            x = self.a * math.cos(alpha) * math.cos(self.theta) - self.b * math.sin(alpha) * math.sin(
                self.theta) + self.center_point_2d.x
            y = self.a * math.cos(alpha) * math.sin(self.theta) + self.b * math.sin(alpha) * math.cos(
                self.theta) + self.center_point_2d.y
            vertices.append(Point2D(x, y))
        return vertices
