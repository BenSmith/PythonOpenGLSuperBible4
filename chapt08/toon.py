#!/usr/bin/env python
# Demonstrates Cell/Toon shading with a 1D texture
# Ben Smith
# benjamin.coder.smith@gmail.com

# Heavily based on Toon.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from math import sin, cos
from pyglet import window

import sys
sys.path.append("../shared")

from math3d import M3DVector3f, M3DMatrix44f, M3D_PI, m3dInvertMatrix44, m3dNormalizeVector, m3dTransformVector3, m3dDotProduct

yRot = 0.0

vLightDir = M3DVector3f(-1.0, 1.0, 1.0)

# Draw a torus (doughnut), using the current 1D texture for light shading
def toonDrawTorus(majorRadius, minorRadius, numMajor, numMinor, lightDir):
    
    mModelViewMatrix = M3DMatrix44f()
    mInvertedLight = M3DMatrix44f()
    vNewLight = M3DVector3f()
    vNormal = M3DVector3f()
    majorStep = 2.0*M3D_PI / numMajor
    minorStep = 2.0*M3D_PI / numMinor
    
    # Get the modelview matrix
    glGetFloatv(GL_MODELVIEW_MATRIX, mModelViewMatrix)
    
    # Instead of transforming every normal and then dotting it with
    # the light vector, we will transform the light into object 
    # space by multiplying it by the inverse of the modelview matrix
    m3dInvertMatrix44(mInvertedLight, mModelViewMatrix)
    m3dTransformVector3(vNewLight, vLightDir, mInvertedLight)
    vNewLight[0] -= mInvertedLight[12]
    vNewLight[1] -= mInvertedLight[13]
    vNewLight[2] -= mInvertedLight[14]
    m3dNormalizeVector(vNewLight)
    
    # Draw torus as a series of triangle strips
    for i in range(0, numMajor):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(0, numMinor + 1):

            b = j * minorStep
            c =  cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)

            # First point
            vNormal[0] = x0*c
            vNormal[1] = y0*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            
            # Texture coordinate is set by intensity of light
            glTexCoord1f(m3dDotProduct(vNewLight, vNormal))
            glVertex3f(x0*r, y0*r, z)

            # Second point
            vNormal[0] = x1*c
            vNormal[1] = y1*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            
            # Texture coordinate is set by intensity of light
            glTexCoord1f(m3dDotProduct(vNewLight, vNormal))
            glVertex3f(x1*r, y1*r, z)
            
        glEnd()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        # Load a 1D texture with toon shaded values
        # Green, greener...
        toonTable = (GLubyte * 3 * 4)(     (0, 32, 0), 
                                            (0, 64, 0),
                                            (0, 128, 0),
                                            (0, 192, 0))
        # Bluish background
        glClearColor(0.0, 0.0, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGB, 4, 0, GL_RGB, GL_UNSIGNED_BYTE, toonTable)
        
        glEnable(GL_TEXTURE_1D)
                                            
        
    def update(self, blah):
        global yRot
        yRot += 0.5

    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        
        glTranslatef(0.0, 0.0, -2.5)
        glRotatef(yRot, 0.0, 1.0, 0.0)
        toonDrawTorus(0.35, 0.15, 50, 25, vLightDir)
        
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
        gluPerspective(35.0, fAspect, 1.0, 50.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Toon/Cell Shading Demo', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/75.0)
    pyglet.app.run()
