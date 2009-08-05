#!/usr/bin/env python
# Demonstrates OpenGL coordinate transformation
# This is unsurprisingly slower than the c++ implementation, even with the timer changed
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Transformgl.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
import sys
sys.path.append("../shared")

from math import cos, sin

from math3d import M3D_PI, M3DVector3f, M3DMatrix44f, m3dTransformVector3, m3dDegToRad, m3dRotationMatrix44
from gltools import gltDrawTorus

xRot = 0.0
yRot = 0.0

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Bluish background
        glClearColor(0, 0, 0.5, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
    def update(self, blah):
        global yRot
        yRot += 0.5

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        transformationMatrix = M3DMatrix44f()
        # Build a rotation matrix
        m3dRotationMatrix44(transformationMatrix, m3dDegToRad(yRot), 0.0, 1.0, 0.0)
        transformationMatrix[12] = 0.0
        transformationMatrix[13] = 0.0
        transformationMatrix[14] = -2.5
            
        glLoadMatrixf(transformationMatrix)
        gltDrawTorus(0.35, 0.15, 40, 20)

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
        gluPerspective(35.0, fAspect, 1.0, 50.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Manual Transformations Demo', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/75.0)
    pyglet.app.run()
