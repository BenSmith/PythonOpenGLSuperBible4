#!/usr/bin/env python
# Creates a 3D Unit Axis model
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: sphereworld.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
from random import randint

import sys
sys.path.append("../shared")
from gltools import gltDrawUnitAxes

xRot = 0.0
yRot = 0.0


class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        whiteLight = (GLfloat * 4)(0.05, 0.05, 0.05, 1.0)
        sourceLight = (GLfloat * 4)(0.25, 0.25, 0.25, 1.0)
        lightPos = (GLfloat * 4)(-10.0, 5.0, 5.0, 1.0)
        
        glEnable(GL_DEPTH_TEST) # Hidden surface removal
        glFrontFace(GL_CCW) # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE) 
        
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight)
        glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        
    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Save the matrix state and do the rotations
        glPushMatrix()
        
        # Move object back and do in place rotation
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Draw something
        gltDrawUnitAxes()
            
        # Restore the matrix state
        glPopMatrix()

    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        fAspect = float(w) / float(h)
        
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluPerspective(35.0, fAspect, 1.0, 40.0)

        # Reset Model view matrix stack
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
    w = MainWindow(800, 600, caption='Unit Axis', resizable=True)
    pyglet.app.run()

