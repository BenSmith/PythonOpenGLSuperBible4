#!/usr/bin/env python
# Demonstrates Motion Blur with the Accumulation Buffer
# Ben Smith 
# benjamin.coder.smith@gmail.com
#
# Based on Motionblur.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
from random import randint
from math import cos, sin

import sys
sys.path.append("../shared")

from fakeglut import glutSolidSphere
from gltools import gltDrawTorus

# Light and material Data
fLightPos   = (GLfloat * 4)(-100.0, 100.0, 50.0, 1.0)  # Point source
fLightPosMirror = (GLfloat * 4)(-100.0, -100.0, 50.0, 1.0)

lightArrayType = GLfloat * 4
fNoLight = lightArrayType(0.0, 0.0, 0.0, 0.0)
fLowLight = lightArrayType(0.25, 0.25, 0.25, 1.0)
fBrightLight = lightArrayType(1.0, 1.0, 1.0, 1.0)

yRot = 45.0         # Rotation angle for animation        

# Draw the ground as a series of triangle strips. The 
# shading model and colors are set such that we end up 
# with a black and white checkerboard pattern.
def DrawGround():
    fExtent = 20.0
    fStep = 0.5
    y = 0.0
    iBounce = 0
    
    glShadeModel(GL_FLAT)
    iStrip = -fExtent
    while iStrip <= fExtent:
        glBegin(GL_TRIANGLE_STRIP)
        iRun = fExtent
        while iRun >= -fExtent:
            if (iBounce % 2) == 0:
                fColor = 1.0
            else:
                fColor = 0.0
                
            glColor4f(fColor, fColor, fColor, 0.5)
            glVertex3f(iStrip, y, iRun)
            glVertex3f(iStrip + fStep, y, iRun)
            
            iBounce += 1
            iRun -= fStep
                
        glEnd()
        iStrip += fStep
        
    glShadeModel(GL_SMOOTH)
    
# Draw the ground and the revolving sphere
def DrawGeometry():
    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    DrawGround()

    # Place the moving sphere
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.5, -3.5)
    glRotatef(-(yRot * 2.0), 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 17, 9)
    glPopMatrix()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Grayish background
        glClearColor(fLowLight[0], fLowLight[1], fLowLight[2], fLowLight[3])
       
        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, fNoLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, fLowLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, fBrightLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, fBrightLight)
        glLightfv(GL_LIGHT0, GL_POSITION, fLightPos)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
         
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)


    # Called to draw scene
    def on_draw(self):
        global yRot
        fPasses = 10.0
        
        # Set the current rotation back a few degrees
        yRot = 35.0
                
        fPass = 0.0
        while fPass < fPasses:
            yRot += .75
           
            # Draw sphere
            DrawGeometry()
            
            # Accumulate to back buffer
            if(fPass == 0.0):
                glAccum(GL_LOAD, 0.5)
            else:
                glAccum(GL_ACCUM, 0.5 * (1.0 / fPasses))
            
            fPass += 1.0

        # copy accumulation buffer to color buffer and
        # do the buffer Swap
        glAccum(GL_RETURN, 1.0)

    def update(self, dt):
        global yRot
        yRot += 1.0
        
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
        glTranslatef(0.0, -0.4, 0.0)

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Motion Blur with the Accumulation Buffer', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1.0/30.0)
    pyglet.app.run()

