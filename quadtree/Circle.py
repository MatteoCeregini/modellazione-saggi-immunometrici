class Circle:
    def __init__(self, center_point, radius):
        self.center_point = center_point
        self.radius = radius

    def contains(self, point):
        return (point.x - self.center_point.x) ** 2 + (point.y - self.center_point.y) ** 2 <= self.radius ** 2
    """
    def intersects(self, boundary):
        dist_x = abs(boundary.center_point.x - self.center_point.x)
        dist_y = abs(boundary.center_point.y - self.center_point.y)
        if dist_x > self.radius + boundary.width or dist_y > self.radius + boundary.height:
            return False
        if dist_x <= boundary.width or dist_y <= boundary.height:
            return True
        return (dist_x - boundary.width) ** 2 + (dist_y - boundary.height) ** 2 <= self.radius ** 2

    """

    def contains(self, point):
        return (point.x - self.center_point.x) ** 2 + (point.y - self.center_point.y) ** 2 <= self.radius ** 2

    def intersects(self, rectangle):
        distance_x = abs(self.center_point.x - rectangle.center_point.x)
        distance_y = abs(self.center_point.y - rectangle.center_point.y)
        if distance_x > rectangle.width / 2 + self.radius:
            return False
        if distance_y > rectangle.height / 2 + self.radius:
            return False
        return (distance_x - rectangle.width / 2) ** 2 + (distance_y - rectangle.height / 2) ** 2 <= self.radius ** 2
