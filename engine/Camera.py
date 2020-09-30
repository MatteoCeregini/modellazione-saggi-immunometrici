from pyglet.gl import glRotatef, glTranslatef
from pyglet.window import key
import math


class Camera:

    def __init__(self):
        # Imposto la posizione iniziale della telecamera nello spazio
        self.pos = [25, 25, 25]
        # Coordinate per gestire la rotazione della telecamera usando il mouse
        self.rot = [0, -10]

    def update(self, dt, keys):
        s = dt * 50
        rot_y = -self.rot[1] / 180 * math.pi
        dx = s * math.sin(rot_y)
        dz = s * math.cos(rot_y)
        if keys[key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz
        if keys[key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz
        if keys[key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx
        if keys[key.D]:
            self.pos[0] += dz
            self.pos[2] += dx
        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s

    def mouse_motion(self, dx, dy):
        dx /= 8
        dy /= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update_rotation(self):
        glRotatef(-self.rot[0], 1, 0, 0)
        glRotatef(-self.rot[1], 0, 1, 0)

    def update_position(self):
        x, y, z = self.pos
        glTranslatef(-x, -y, -z)
