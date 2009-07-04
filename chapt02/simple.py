import pyglet
from pyglet.gl import *
from pyglet import window

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        glClearColor(0, 0, 1, 1)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glFlush()

w = MainWindow(caption='Simple', resizable=True)

pyglet.app.run()
