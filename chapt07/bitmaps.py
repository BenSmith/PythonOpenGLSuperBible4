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

# Bitmap of camp fire
fireType = GLubyte * 128

fire = fireType(0x00, 0x00, 0x00, 0x00, 
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0xc0,
                        0x00, 0x00, 0x01, 0xf0,
                        0x00, 0x00, 0x07, 0xf0,
                        0x0, 0x00, 0x1f, 0xe0,
                        0x1f, 0x80, 0x1f, 0xc0,
                        0x0, 0xc0, 0x3f, 0x80,	
                        0x07, 0xe0, 0x7e, 0x00,
                        0x03, 0xf0, 0xff, 0x80,
                        0x03, 0xf5, 0xff, 0xe0,
                        0x07, 0xfd, 0xff, 0xf8,
                        0x1f, 0xfc, 0xff, 0xe8,
                        0xff, 0xe3, 0xbf, 0x70, 
                        0xde, 0x80, 0xb7, 0x00,
                        0x71, 0x10, 0x4a, 0x80,
                        0x03, 0x10, 0x4e, 0x40,
                        0x02, 0x88, 0x8c, 0x20,
                        0x05, 0x05, 0x04, 0x40,
                        0x02, 0x82, 0x14, 0x40,
                        0x02, 0x40, 0x10, 0x80, 
                        0x02, 0x64, 0x1a, 0x80,
                        0x00, 0x92, 0x29, 0x00,
                        0x00, 0xb0, 0x48, 0x00,
                        0x00, 0xc8, 0x90, 0x00,
                        0x00, 0x85, 0x10, 0x00,
                        0x00, 0x03, 0x00, 0x00,
                        0x00, 0x00, 0x10, 0x00
                        )


class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 0.0)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Set color to white
        glColor3f(1.0, 1.0, 1.0)
        
        # Loop through 16 rows and columns
        for y in range(16):
            # Set raster position for this "square"
            glRasterPos2i(0, y * 32)
            for x in range(16):
                # Draw the "fire" bitmap, advance raster position
                glBitmap(32, 32, 0.0, 0.0, 32.0, 0.0, fire)

    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
            
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Psuedo window coordinates
        gluOrtho2D(0.0, float(w), 0.0, float(h))

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()    

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(512, 512, caption='OpenGL Bitmaps', resizable=True)
    pyglet.app.run()
