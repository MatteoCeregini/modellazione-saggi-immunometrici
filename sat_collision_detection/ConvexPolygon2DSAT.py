from math import inf


class ConvexPolygon2DSAT:
    def __init__(self, vertices):
        self.vertices = vertices

    def get_min_max(self, projection_axis):
        min_1 = +inf
        max_1 = -inf
        for v in self.vertices:
            q = v.dot_product(projection_axis)
            min_1 = min(min_1, q)
            max_1 = max(max_1, q)
        return min_1, max_1

    def overlaps(self, polygon):
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            projection_axis = self.vertices[j].subtraction(self.vertices[i]).orthogonal()
            min_1, max_1 = self.get_min_max(projection_axis)
            min_2, max_2 = polygon.get_min_max(projection_axis)
            if not max_2 >= min_1 and max_1 >= min_2:
                return False

        for i in range(len(polygon.vertices)):
            j = (i + 1) % len(polygon.vertices)
            projection_axis = self.vertices[j].subtraction(self.vertices[i]).orthogonal()
            min_1, max_1 = polygon.get_min_max(projection_axis)
            min_2, max_2 = self.get_min_max(projection_axis)
            if not max_2 >= min_1 and max_1 >= min_2:
                return False
        return True
