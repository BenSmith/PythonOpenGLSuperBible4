# stencil.py
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Stencil.cpp
# OpenGL SuperBible
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from pyglet.gl import *
from pyglet import window
from math import sin, cos

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

    # Called to draw scene
    def on_draw(self):
        radius = 0.1 # Initial radius of spiral
        angle = 0.0 # Looping variable
        
        # Clear blue window
        glClearColor(0, 0, 1, 0)
        
        # Use 0 for clear stencil, enable stencil test
        glClearStencil(0)
        glEnable(GL_STENCIL_TEST)
        
        
        # Clear color and stencil buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        
        # All drawing commands fail the stencil test, and are not
        # drawn, but increment the value in the stencil buffer. 
        glStencilFunc(GL_NEVER, 0x0, 0x0)
        glStencilOp(GL_INCR, GL_INCR, GL_INCR)

        # Spiral pattern will create stencil pattern
        # Draw the spiral pattern with white lines. We 
        # make the lines  white to demonstrate that the 
        # stencil function prevents them from being drawn
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        while angle < 400.0:
            glVertex2d(radius * cos(angle), radius * sin(angle))
            
            angle += 0.1
            radius *= 1.002
        glEnd()
    
        # Now, allow drawing, except where the stencil pattern is 0x1
        # and do not make any further changes to the stencil buffer
        glStencilFunc(GL_NOTEQUAL, 0x1, 0x1);
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP);
            
        # Now draw red bouncing square
        # (x and y) are modified by a timer function
        glColor3f(1.0, 0.0, 0.0)
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
    w = MainWindow(800, 600, caption='OpenGL Stencil Test', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/33.0)
    pyglet.app.run()
