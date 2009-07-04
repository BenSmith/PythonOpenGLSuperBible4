import pyglet
from pyglet.gl import *
from pyglet import window

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        glClearColor(0, 0, 1, 1)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
        glColor3f(1.0, 0.0, 0.0)
        glRectf(-25.0, 25.0, 25.0, -25.0)
        
        glFlush()
        
    def on_resize(self, w, h):
        
        if h == 0:
            h = 1
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        aspectRatio = float(w) / float(h)
        if w <= h:
            glOrtho(-100.0, 100.0, -100.0/aspectRatio, 100.0/aspectRatio, 1.0, -1.0)
        else:
            glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        

w = MainWindow(caption='Simple', resizable=True)

pyglet.app.run()
