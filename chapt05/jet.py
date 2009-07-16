#!/usr/bin/env python
# A hand modeled Jet airplane
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# based heavily on jet.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key


xRot = 0.0
yRot = 0.0

lightArrayType = GLfloat * 4

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        ambientLight = lightArrayType(1.0, 1.0, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST)	
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out

        # Nice light blue
        glClearColor(0.0, 0.0, 5.0,1.0)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the matrix state
        glPushMatrix()
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Nose Cone ##############/
        # Bright Green
        glColor3ub(0, 255, 0)
        glBegin(GL_TRIANGLES)
        
        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(15.0,0.0,30.0)

        glVertex3f(15.0,0.0,30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, 60.0)

        glVertex3f(0.0, 0.0, 60.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(-15.0,0.0,30.0)

        # Body of the Plane ############
        # light gray
        glColor3ub(192,192,192)
        glVertex3f(-15.0,0.0,30.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)

        glVertex3f(0.0, 0.0, -56.0)
        glVertex3f(0.0, 15.0, 30.0)
        glVertex3f(15.0,0.0,30.0)	

        glVertex3f(15.0,0.0,30.0)
        glVertex3f(-15.0, 0.0, 30.0)
        glVertex3f(0.0, 0.0, -56.0)

        #######################
        # Left wing
        # Dark gray
        glColor3ub(64,64,64)
        glVertex3f(0.0,2.0,27.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(60.0, 2.0, -8.0)

        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(0.0,2.0,27.0)

        glVertex3f(60.0, 2.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)
        glVertex3f(0.0,7.0,-8.0)


        # Other wing top section
        glVertex3f(0.0,2.0,27.0)
        glVertex3f(0.0, 7.0, -8.0)
        glVertex3f(-60.0, 2.0, -8.0)

        # Tail section###############/
        # Bottom of back fin
        glColor3ub(255,255,0)
        glVertex3f(-30.0, -0.50, -57.0)
        glVertex3f(30.0, -0.50, -57.0)
        glVertex3f(0.0,-0.50,-40.0)

        # top of left side
        glVertex3f(0.0,-0.0,-40.0)
        glVertex3f(30.0, -0.0, -57.0)
        glVertex3f(0.0, 4.0, -57.0)

        # top of right side
        glVertex3f(0.0, 4.0, -57.0)
        glVertex3f(-30.0, -0.0, -57.0)
        glVertex3f(0.0,-0.0,-40.0)

        # back of bottom of tail
        glVertex3f(30.0,-0.0,-57.0)
        glVertex3f(-30.0, -0.0, -57.0)
        glVertex3f(0.0, 4.0, -57.0)


        # Top of Tail section left
        glColor3ub(255,0,0)
        glVertex3f(0.0,0.0,-40.0)
        glVertex3f(3.0, 0.0, -57.0)
        glVertex3f(0.0, 25.0, -65.0)

        glVertex3f(0.0, 25.0, -65.0)
        glVertex3f(-3.0, 0.0, -57.0)
        glVertex3f(0.0,0.0,-40.0)


        # Back of horizontal section
        glVertex3f(3.0,0.0,-57.0)
        glVertex3f(-3.0, 0.0, -57.0)
        glVertex3f(0.0, 25.0, -65.0)
        glEnd()

        glPopMatrix()
        
        
    def on_resize(self, w, h):
        nRange = 80.0
        
        # Prevent a divide by zero
        if(h == 0):
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        if (w <= h):
            glOrtho (-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
        else:
            glOrtho (-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_key_press(self, symbol, modifier):
        global xRot, yRot
        if symbol == key.UP:
            xRot -= 5.0
        elif symbol == key.DOWN:
            xRot += 5.0
        elif symbol == key.LEFT:
            yRot -= 5.0
        elif symbol == key.RIGHT:
            yRot += 5.0
        
        xRot = float(int(xRot) % 360)
        yRot = float(int(yRot) % 360)

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Jet', resizable=True)
    pyglet.app.run()
