import os
from datetime import datetime
from threading import Thread

import pyglet
from pyglet.gl import *
from pyglet.window import key

from engine.Camera import Camera
from engine.Colors import Colors
from engine.Renderer import Renderer
from json_writer.JSONWriter import JSONWriter


class WindowManager(pyglet.window.Window):

    def __init__(self, user_input, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(800, 600)
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        screen_width = screen.width
        screen_height = screen.height
        x = int(screen_width / 2 - self.width / 2)
        y = int(screen_height / 2 + self.height / 2)
        self.set_location(x, y)
        # Imposto la dimensione della finestra
        # Inizializzo il lock del mouse a False -> Il mouse inizialmente non è "legato" alla finestra
        self.colors = Colors()
        self.mouse_locked = False
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        screen_width = screen.width
        screen_height = screen.height
        self.set_location(int(screen_width / 4), int(screen_height / 4))
        # Imposto il titolo della finestra
        self.set_caption('Modello Computazionale')
        # Creo l'oggetto che si occupa di gestire la telecamera
        self.camera = Camera()
        # Creo l'oggetto che si occupa di disegnare all'interno della finestra
        self.renderer = Renderer(user_input)
        # Creo la struttura dati che si occupa di tenere traccia dei tasti che vengono premuti
        self.keys = key.KeyStateHandler()
        # La passo al gestore degli eventi
        self.push_handlers(self.keys)
        # Imposto che ad ogni frame deve essere chiamata la funzione 'update'
        pyglet.clock.schedule(self.update)
        # Imposto che quando chiamo il metodo clear(), la finestra va colorata di bianco
        glClearColor(1, 1, 1, 1)
        # Fa in modo che se un oggetto ne copre un altro quello coperto non si veda
        glEnable(GL_DEPTH_TEST)
        self.renderer.create_surface()
        self.renderer.create_antibodies()
        self.renderer.create_antigens()
        data = self.renderer.get_data()
        now = datetime.now()
        file_name = str(now.hour) + "." + str(now.minute) + "-" + str(now.day) + "." + str(now.month) + "." + str(now.year) + ".json"
        path = os.path.join(os.getcwd(), "data")
        writer = JSONWriter(data, path, file_name)
        writer.write_json()
        self.set_visible(True)

    def on_draw(self):
        # Coloro la finestra di bianco
        self.clear()
        # Imposto la prospettiva come se fosse 3D (oggetti più lontani sembrano più piccoli, ecc...)
        self.set_3d_prospective()
        # Aggiorno i valori della telecamera
        self.camera.update_rotation()
        self.camera.update_position()
        # Disegno gli oggetti presenti nel batch
        self.renderer.draw_batch()

    # Metodo che ogni volta che muovo il mouse fa muovere in accordo la telecamera
    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_locked:
            self.camera.mouse_motion(dx, dy)

    # Metodo che utilizza funzioni OpenGL per rendere la prospettiva 3D
    #  (oggetti più lontani sembrano più piccoli, ecc...)
    def set_3d_prospective(self):
        gl.glMatrixMode(GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(70, self.width / self.height, 0.05, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # Ad ogni frame aggiorno la telecamera
    def update(self, dt):
        if self.mouse_locked:
            self.camera.update(dt, self.keys)

    # Metodo per gestire i comandi da tastiera relativi alla finestra
    def on_key_press(self, key_pressed, modifiers):
        if key_pressed == key.ESCAPE and not self.mouse_locked:
            self.set_exclusive_mouse(True)
            self.mouse_locked = True
        elif key_pressed == key.ESCAPE and self.mouse_locked :
            self.set_exclusive_mouse(False)
            self.mouse_locked = False

