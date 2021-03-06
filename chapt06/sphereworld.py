#!/usr/bin/env python
# Demonstrates an immersive 3D environment using actors and a camera
# This version adds fog and multisampling
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

from math3d import M3D_PI, M3DVector3f, M3DMatrix44f, m3dTransformVector3, m3dDegToRad, m3dRotationMatrix44, m3dGetPlaneEquation, m3dMakePlanarShadowMatrix
from glframe import GLFrame
from fakeglut import glutSolidSphere
from gltools import gltDrawTorus

NUM_SPHERES = 50
spheres = [GLFrame() for i in range(NUM_SPHERES)]
frameCamera = GLFrame()

# Light and material data

# pyglet reverses y direction
fLightPos = (GLfloat * 4)(-100.0, 100.0, 50.0, 1.0)

lightArrayType = GLfloat * 4
fNoLight = lightArrayType(0.0, 0.0, 0.0, 0.0)
fLowLight = lightArrayType(0.25, 0.25, 0.25, 1.0)
fBrightLight = lightArrayType(1.0, 1.0, 1.0, 1.0)

yRot = 0.0 # Rotation angle for animation

mShadowMatrix = M3DMatrix44f()

# Draw a gridded ground
def DrawGround():
    fExtent = 20.0
    fStep = 1.0
    y = -0.4
    
    iStrip = -fExtent
    
    while (iStrip <= fExtent):
        t = 0.0
        glBegin(GL_TRIANGLE_STRIP)
        
        glNormal3f(0.0, 1.0, 0.0) # All point up
        iRun = fExtent
        while (iRun >= -fExtent):
            glVertex3f(iStrip, y, iRun)
            
            glVertex3f(iStrip + fStep, y, iRun)
            
            iRun -= fStep
            
        glEnd()
        iStrip += fStep

# Draw random inhabitants and the rotating torus/sphere duo
def DrawInhabitants(nShadow):
    global yRot
    if nShadow == 0:
        pass #yRot += 0.5
    else:
        glColor4f(0.0, 0.0, 0.0, 0.5)
    
    # Draw the randomly located spheres
    if nShadow == 0:
        glColor3f(0.0, 1.0, 0.0)

    for sphere in spheres:
        glPushMatrix()
        
        sphere.ApplyActorTransform()
        glutSolidSphere(0.3, 21, 11)
        
        glPopMatrix()
        
    glPushMatrix()
    # -y is up in pyglet
    glTranslatef(0.0, 0.1, -2.5)
    
    if nShadow == 0:
        glColor3f(0.0, 0.0, 1.0)
    
    glPushMatrix()
    glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 21, 11)
    glPopMatrix()
    
    if nShadow == 0:
        # Torus alone will be specular
        glColor3f(1.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, fBrightLight)
        
    glRotatef(yRot, 0.0, 1.0, 0.0)
    gltDrawTorus(0.35, 0.15, 61, 37)
    glMaterialfv(GL_FRONT, GL_SPECULAR, fNoLight)
    glPopMatrix()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        global mShadowMatrix
        window.Window.__init__(self, *args, **kwargs)
        
        # Calculate shadow matrix
        vPoints = (M3DVector3f * 3)((0.0, -0.4, 0.0),
                                     (10.0, -0.4, 0.0),
                                     (5.0,-0.4, -5.0)
                                    )
        glEnable(GL_MULTISAMPLE_ARB)
        
        # Grayish background
        glClearColor(fLowLight[0], fLowLight[1], fLowLight[2], fLowLight[3])
        

        # Clear stencil buffer with zero, increment by one whenever anybody
        # draws into it. When stencil function is enabled, only write where
        # stencil value is zero. This prevents the transparent shadow from drawing
        # over itself
        glStencilOp(GL_INCR, GL_INCR, GL_INCR)
        glClearStencil(0)
        glStencilFunc(GL_EQUAL, 0x0, 0x01)
        
        # Setup Fog parameters
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, fLowLight)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 5.0)
        glFogf(GL_FOG_END, 30.0)
        glHint(GL_FOG_HINT, GL_NICEST)

        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        
        # already enabled this... but superbible code has it here, too
        glEnable(GL_MULTISAMPLE_ARB)
        
        # Setup light parameters
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, fNoLight)
        glLightfv(GL_LIGHT0, GL_AMBIENT, fLowLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, fBrightLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, fBrightLight)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Get the plane equation from three points on the ground
        vPlaneEquation = m3dGetPlaneEquation(vPoints[0], vPoints[1] , vPoints[2])
        
        # Calculate projection matrix to draw shadown on the ground
        mShadowMatrix = m3dMakePlanarShadowMatrix(vPlaneEquation, fLightPos)
        
        # Mostly use material tracking
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
      
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
        
        # Position light before any other transformations
        glLightfv(GL_LIGHT0, GL_POSITION, fLightPos)
        
        # Draw the ground
        glColor3f(0.60, 0.40, 0.10)
        DrawGround()
        
        # Draw shadows first
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_STENCIL_TEST)
        
        glPushMatrix()
        
        glMultMatrixf(mShadowMatrix)
        DrawInhabitants(1)
            
        glPopMatrix()
        glDisable(GL_STENCIL_TEST)
        glDisable(GL_BLEND)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        # Draw inhabitants normally
        DrawInhabitants(0)
        
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
    w = MainWindow(800, 600, caption='OpenGL SphereWorld Demo + Lights and Shadow', resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/60.0)
    pyglet.app.run()
