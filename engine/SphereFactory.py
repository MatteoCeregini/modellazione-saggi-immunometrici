from math import radians, cos, sin

from pyglet.gl import GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_TRIANGLES

from engine.Model import Model


class SphereFactory:
    def get_models(self, x_1, y_1, z_1, color):
        models = []
        step = 15
        for lat in range(-90, 90, step):
            verts = []
            for lon in range(-180, 181, step):
                x = x_1 +
                y = y_1 + sin(radians(lat))
                z = z_1 + cos(radians(lat)) * sin(radians(lon))
                verts += [x, y, z]
                x = x_1 + -cos(radians((lat + step))) * cos(radians(lon))
                y = y_1 + sin(radians((lat + step)))
                z = z_1 + cos(radians((lat + step))) * sin(radians(lon))
                verts += [x, y, z]
            count = int(len(verts) / 3)
            m = Model(count, GL_TRIANGLES, None, verts, color * count)
            models.append(m)
        return models
