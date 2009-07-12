#!/usr/bin/env python
# Demonstrates OpenGL coordinate transformation
# This is unsurprisingly slower than the c++ implementation, even with the timer changed
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Transform.cpp
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

xRot = 0.0
yRot = 0.0

# Draw a torus (doughnut), using the current 1D texture for light shading
def DrawTorus(mTransform):
    majorRadius = 0.35
    minorRadius = 0.15
    numMajor = 40
    numMinor = 20
    objectVertex = M3DVector3f()         # Vertex in object/eye space
    transformedVertex = M3DVector3f()    # New Transformed vertex   
    majorStep = 2.0 
    majorStep = 2.0 * M3D_PI / float(numMajor)
    minorStep = 2.0 * M3D_PI / float(numMinor)
    
    i = 0
    while (i < numMajor):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP)
        j = 0
        # BS some sort of rounding error keeps a strip from being drawn
        while (j < numMinor + 1):
            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)

            # First point
            objectVertex[0] = x0*r
            objectVertex[1] = y0*r
            objectVertex[2] = z
            m3dTransformVector3(transformedVertex, objectVertex, mTransform)
            glVertex3fv(transformedVertex)

            # Second point
            objectVertex[0] = x1*r
            objectVertex[1] = y1*r
            objectVertex[2] = z
            m3dTransformVector3(transformedVertex, objectVertex, mTransform)
            glVertex3fv(transformedVertex)
            j += 1
        glEnd()
        i += 1


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
            
        DrawTorus(transformationMatrix)

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
