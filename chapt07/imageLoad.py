#!/usr/bin/env python
# Demonstrates loading and displaying bitmaps
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on Bitmaps.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window



class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 0.0)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)
        
        img = pyglet.image.load("fire.jpg")
        
        # Use window coordinates to set raster position.
        glRasterPos2i(0, 0)
        # TODO: it's upside down!
        glDrawPixels(img.width, img.height, GL_RGB, GL_UNSIGNED_BYTE, img.get_data("RGB", img.pitch))
        

    # For this example, it really doesn't matter what the 
    # projection is since we are using glWindowPos
    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
            
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluOrtho2D(0.0, float(w), 0.0, float(h))

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()    



# Main program entry point
if __name__ == '__main__':
    w = MainWindow(512, 512, caption='OpenGL Image Loading', resizable=True)
    pyglet.app.run()
