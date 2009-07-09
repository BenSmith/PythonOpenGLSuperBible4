#!/usr/bin/env python
# bounce.py
# Demonstrates a simple animated rectangle program with pyglet
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

# Initial square position and size
x = 0.0
y = 0.0
rsize = 25.0

# Step size in x and y directions
# (number of pixels to move each time)
xstep = 1.0
ystep = 1.0

# Keep track of windows changing width and height
windowWidth = 100.0
windowHeight = 100.0

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
        glRectf(x, y, x + rsize, y - rsize)
        
        # Flush drawing commands and swap
        # pyglet does this automatically when using pyglet.app.run()
        # otherwise, you can use flip() http://pyglet.org/doc/programming_guide/windows_and_opengl_contexts.html
        
    def update(self, dy):
        global x, y, xstep, ystep
        # Reverse direction when you reach left or right edge
        if (x > windowWidth - rsize) or x < -windowWidth:
            xstep = -xstep
        
        # Reverse direction when you reach top or bottom edge
        if y > windowHeight or (y < -windowHeight + rsize):
            ystep = -ystep
            
        # Actually move the square
        x += xstep
        y += ystep
        
        # Check bounds.  This is in case the window is made
        # smaller while the rectangle is bouncing and the 
        # rectangle suddenly finds itself outside the new
        # clipping volume
        if x > windowWidth - rsize + xstep:
            x = windowWidth - rsize - 1.0
        elif x < -(windowWidth + xstep):
            x = -windowWidth - 1.0
            
        if y > windowHeight + ystep:
            y = windowHeight - 1.0
        elif y < -(windowHeight - rsize + ystep):
            y = -windowHeight + rsize - 1.0
        
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
            windowWidth = 100.0
            windowHeight = 100.0 / aspectRatio
            glOrtho(-100.0, 100.0, -windowHeight, windowHeight, 1.0, -1.0)
        else:
            windowWidth = 100.0 * aspectRatio
            windowWidth = 100.0
            glOrtho(-windowWidth , windowWidth, -100.0, 100.0, 1.0, -1.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        
# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Bounce', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/33.0)
    pyglet.app.run()
