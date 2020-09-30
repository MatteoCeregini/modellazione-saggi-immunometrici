from math import radians, cos, sin
from random import randrange

from pyglet.gl import GL_TRIANGLES

from engine.Model import Model


# Uso matrice di rotazione che ruota rispetto l'asse y
from utils.Point3D import Point3D


def rotate(x, y, z, theta):
    x_new = x * cos(theta) - z * sin(theta)
    z_new = x * sin(theta) + z * cos(theta)
    return [x_new, y, z_new]


class EllipsoidFactory:
    def get_models(self, x_1, y_1, z_1, a, b, c, color, theta):
        models = []
        step = 15
        vertices = []
        for lat in range(-90, 90, step):
            verts = []
            for lon in range(-180, 181, step):
                x_tmp = a * cos(radians(lat)) * sin(radians(lon))
                y_tmp = c * sin(radians(lat))
                z_tmp = b * cos(radians(lat)) * cos(radians(lon))
                x_rot, y_rot, z_rot = rotate(x_tmp, y_tmp, z_tmp, theta)
                x = x_1 + x_rot
                y = y_1 + y_rot
                z = z_1 + z_rot
                verts += [x, y, z]
                vertices.append(Point3D(x, y, z))

                x_tmp = a * cos(radians(lat + step)) * sin(radians(lon))
                y_tmp = c * sin(radians(lat + step))
                z_tmp = b * cos(radians(lat + step)) * cos(radians(lon))
                x_rot, y_rot, z_rot = rotate(x_tmp, y_tmp, z_tmp, theta)
                x = x_1 + x_rot
                y = y_1 + y_rot
                z = z_1 + z_rot
                verts += [x, y, z]

                vertices.append(Point3D(x, y, z))

            count = int(len(verts) / 3)
            m = Model(count, GL_TRIANGLES, None, verts, color * count)
            models.append(m)
        return models, vertices
