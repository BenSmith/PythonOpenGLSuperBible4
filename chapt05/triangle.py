#!/usr/bin/env python
# Demonstrates OpenGL color triangle
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# based heavily on ccube.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key


xRot = 0.0
yRot = 0.0

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

    # Called to draw scene
    def on_draw(self):
        
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Enable smooth shading
        glShadeModel(GL_SMOOTH)

        # Draw the triangle
        glBegin(GL_TRIANGLES)

        # Red Apex
        glColor3ub(255,0,0)
        glVertex3f(0.0,200.0,0.0)

        # Green on the right bottom corner
        glColor3ub(0,255,0)
        glVertex3f(200.0,-70.0,0.0)

        # Blue on the left bottom corner
        glColor3ub(0,0,255)
        glVertex3f(-200.0, -70.0, 0.0)
        
        glEnd()

        
    def on_resize(self, w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glLoadIdentity()

        # Window is higher than wide
        if w <= h:
            windowHeight = 250.0 * h / w
            windowWidth = 250.0
        else:
            #window wider than high
            windowWidth = 250.0 * w/h
            windowHeight = 250.0
            
        # Set the clipping volume
        glOrtho(-windowWidth, windowWidth, -windowHeight, windowHeight, 1.0, -1.0)
        
# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='RGB Triangle', resizable=True)
    pyglet.app.run()
