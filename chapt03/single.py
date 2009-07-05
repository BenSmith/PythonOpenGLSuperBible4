# single.py
# Single buffer rendering
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Bounce.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from pyglet.gl import *
from pyglet import window
from math import cos, sin

# TODO: actually use single buffering

radius = 0.1
angle = 0.0

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

    # Called to draw scene
    def on_draw(self):
        glClearColor(0, 0, 1, 0)
        if angle == 0.0:
            glClear(GL_COLOR_BUFFER_BIT)
        
        glBegin(GL_POINTS)
        glVertex2d(radius * cos(angle), radius * sin(angle))
        glEnd()
            
        glFlush()
        
    def update(self, dy):
        global radius, angle
        radius *= 1.01
        angle += 0.1
        
        if angle > 30.0:
            radius = 0.1
            angle = 0.0
        
    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Set the perspective coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set the 2D Coordinate system
        gluOrtho2D(-4.0, 4.0, -3.0, 3.0)
        
        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        
# Main program entry point
if __name__ == '__main__':
    w = MainWindow(caption='Single Buffering', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1.0/20.0)
    pyglet.app.run()
