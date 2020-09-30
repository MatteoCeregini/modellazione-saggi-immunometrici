from engine.Antibody import Antibody
from quadtree.Circle import Circle
from quadtree.Rectangle import Rectangle

from utils.Point2D import Point2D
from utils.Point3D import Point3D


class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.subdivided = False

        self.north_east = None
        self.north_west = None
        self.south_east = None
        self.south_west = None

    def subdivide(self):
        x = self.boundary.center_point.x
        y = self.boundary.center_point.y
        half_width = self.boundary.half_width / 2
        half_height = self.boundary.half_height / 2

        north_east_boundary = Rectangle(Point2D(x + half_width, y - half_height), half_width, half_height)
        self.north_east = Quadtree(north_east_boundary, self.capacity)
        north_west_boundary = Rectangle(Point2D(x - half_width, y - half_height), half_width, half_height)
        self.north_west = Quadtree(north_west_boundary, self.capacity)
        south_east_boundary = Rectangle(Point2D(x + half_width, y + half_height), half_width, half_height)
        self.south_east = Quadtree(south_east_boundary, self.capacity)
        south_west_boundary = Rectangle(Point2D(x - half_width, y + half_height), half_width, half_height)
        self.south_west = Quadtree(south_west_boundary, self.capacity)
        self.subdivided = True

    def insert(self, obj):
        if not self.boundary.contains(obj.center_point_2d):
            return False
        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True
        if not self.subdivided:
            self.subdivide()
        return (self.north_east.insert(obj) or self.north_west.insert(obj) or self.south_east.insert(
            obj) or self.south_west.insert(obj))

    def query(self, boundary, found):
        if not boundary.intersects(self.boundary):
            return found
        for obj in self.objects:
            if boundary.contains(obj.center_point_2d):
                found.append(obj)
        if self.subdivided:
            self.north_west.query(boundary, found)
            self.north_east.query(boundary, found)
            self.south_west.query(boundary, found)
            self.south_east.query(boundary, found)
        return found
