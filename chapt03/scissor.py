# scissor.py
# Demonstates OpenGL Primitive GL_POINTS
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Scissor.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClearColor(0, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Now set scissor to smaller red sub region
        glClearColor(1, 0, 0, 0)
        glScissor(100, 100, 600, 400)
        glEnable(GL_SCISSOR_TEST)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Finally, an even smaller green rectangle
        glClearColor(0, 1, 0, 0)
        glScissor(200, 200, 400, 200)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Turn scissor back off for next render
        glDisable(GL_SCISSOR_TEST)
        

        # Flush drawing commands
        # pyglet does this automatically when using pyglet.app.run()
        # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html

    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        nRange = 100.0
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        if w <= h:
            glOrtho (-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
        else:
            glOrtho (-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Lines Example', resizable=True)
    pyglet.app.run()
