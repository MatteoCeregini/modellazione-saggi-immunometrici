from utils.Point2D import Point2D


class Rectangle:
    def __init__(self, center_point, half_width, half_height):
        self.center_point = center_point
        self.half_width = half_width
        self.half_height = half_height
        
    def completely_contains_polygon(self, vertices_polygon):
        for v in vertices_polygon:
            if not self.contains(v):
                return False
        return True

    def contains(self, point):
        return self.center_point.x - self.half_width <= point.x <= self.center_point.x + self.half_width and self.center_point.y - self.half_height <= point.y <= self.center_point.y + self.half_height

    def intersects(self, boundary):
        return not (boundary.center_point.x - boundary.half_width > self.center_point.x + self.half_width or
                    boundary.center_point.x + boundary.half_width < self.center_point.x - self.half_width or
                    boundary.center_point.y - boundary.half_height > self.center_point.y + self.half_height or
                    boundary.center_point.y + boundary.half_height < self.center_point.y - self.half_height)
    """
    def intersects(self, rectangle):
        return self.left < rectangle.right and self.right > rectangle.left and self.top > rectangle.bottom and self.bottom < rectangle.top

    def contains(self, point):
        # x1 < x < x2 and y1 < y < y2
        return self.left <= point.x <= self.right and self.bottom <= point.y <= self.top
    """
