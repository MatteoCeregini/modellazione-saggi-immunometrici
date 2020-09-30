from pyglet.gl import GL_QUADS
from engine.Model import Model


class CuboidFactory:

    def get_models(self, x, y, z, width, height, colors):
        x_2 = x + width
        y_2 = y + height
        z_2 = z + width
        m1 = Model(4, GL_QUADS, None, (x, y, z, x, y, z_2, x, y_2, z_2, x, y_2, z), colors[0] * 4)
        m2 = Model(4, GL_QUADS, None, (x_2, y, z_2, x_2, y, z, x_2, y_2, z, x_2, y_2, z_2), colors[1] * 4)
        m3 = Model(4, GL_QUADS, None, (x, y, z, x_2, y, z, x_2, y, z_2, x, y, z_2), colors[2] * 4)  # Faccia che sta a contatto con la superfice
        m4 = Model(4, GL_QUADS, None, (x, y_2, z_2, x_2, y_2, z_2, x_2, y_2, z, x, y_2, z), colors[3] * 4)
        m5 = Model(4, GL_QUADS, None, (x_2, y, z, x, y, z, x, y_2, z, x_2, y_2, z), colors[4] * 4)
        m6 = Model(4, GL_QUADS, None, (x, y, z_2, x_2, y, z_2, x_2, y_2, z_2, x, y_2, z_2), colors[5] * 4)
        return [m1, m2, m3, m4, m5, m6]


