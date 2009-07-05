#!/usr/bin/env python
# glrect.py
# Just draw a single rectangle in the middle of the screen
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: GLRect.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from pyglet.gl import *
from pyglet import window

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Setup the rendering state
        glClearColor(0, 0, 1, 1)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Set current drawing color to red
        #               R,      G,      B
        glColor3f(1.0, 0.0, 0.0)
        
        # Draw a filled rectangle with current color
        glRectf(-25.0, 25.0, 25.0, -25.0)
        
        # Flush drawing commands
        glFlush()
        
    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Establish clipping volume (left, right, bottom, top, near, far)
        aspectRatio = float(w) / float(h)
        if w <= h:
            glOrtho(-100.0, 100.0, -100.0/aspectRatio, 100.0/aspectRatio, 1.0, -1.0)
        else:
            glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(caption='GLRect', resizable=True)

    pyglet.app.run()
