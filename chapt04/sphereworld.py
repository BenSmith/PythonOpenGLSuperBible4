#!/usr/bin/env python
# Demonstrates an immersive 3D environment using actors and a camera
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
from math import cos, sin

import sys
sys.path.append("../shared")

from math3d import M3D_PI, M3DVector3f, M3DMatrix44f, m3dTransformVector3, m3dDegToRad, m3dRotationMatrix44
from glframe import GLFrame
from gltools import gltDrawTorus
from fakeglut import glutSolidSphere

NUM_SPHERES = 50
spheres = [GLFrame() for i in range(NUM_SPHERES)]
frameCamera = GLFrame()

yRot = 0.0

# Draw a gridded ground
def DrawGround():
    fExtent = 20.0
    fStep = 1.0
    y = 0.4
    
    iLine = -fExtent
    glBegin(GL_LINES)
    while (iLine <= fExtent):
        
        glVertex3f(iLine, y, fExtent) # Draw Z lines
        glVertex3f(iLine, y, -fExtent)
        
        glVertex3f(fExtent, y, iLine)
        glVertex3f(-fExtent, y, iLine)
        
        iLine += fStep
        
    glEnd()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Bluish background
        glClearColor(0, 0, 0.5, 1)
        
        # Draw everything as wire frame
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # Randomly place sphere inhabitants
        for sphere in spheres:
            # Pick a random location between -20 and 20 at .1 increments
            sphere.setOrigin(float(randint(-200, 200)) * 0.1, 0.0, float(randint(-200, 200)) * 0.1)
        
    def update(self, blah):
        global yRot
        yRot += 0.5

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        
        frameCamera.ApplyCameraTransform()
        
        # Draw the ground
        DrawGround()
        
        # Draw the randomly located spheres
        for sphere in spheres:
            glPushMatrix()
            
            sphere.ApplyActorTransform()
            glutSolidSphere(0.1, 13, 26)
            
            glPopMatrix()

        glPushMatrix()
        
        glTranslatef(0.0, 0.0, -2.5)

        glPushMatrix()
        
        glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
        glTranslatef(1.0, 0.0, 0.0)
        glutSolidSphere(0.1, 13, 26)
            
        glPopMatrix()

        glRotatef(yRot, 0.0, 1.0, 0.0)
        gltDrawTorus(0.35, 0.15, 40, 20)
            
        glPopMatrix()
        
        glPopMatrix()

    # Respond to arrow keys by moving the camera frame of reference
    def on_key_press(self, symbol, modifier):
        if symbol == key.UP:
            frameCamera.MoveForward(1.0)
        elif symbol == key.DOWN:
            frameCamera.MoveForward(-1.0)
        elif symbol == key.LEFT:
            frameCamera.RotateLocalY(0.1)
        elif symbol == key.RIGHT:
            frameCamera.RotateLocalY(-0.1)

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
    w = MainWindow(800, 600, caption='OpenGL SphereWorld Demo', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/75.0)
    pyglet.app.run()
