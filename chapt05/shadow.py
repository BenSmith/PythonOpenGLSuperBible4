#!/usr/bin/env python
# Demonstrates simple planar shadows
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# based heavily on litjet.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
import sys
sys.path.append("../shared")

from math3d import M3DVector3f, m3dFindNormal, M3DMatrix44f, m3dGetPlaneEquation, m3dMakePlanarShadowMatrix
from forpyglet import glutSolidSphere

xRot = 0.0
yRot = 0.0

lightArrayType = GLfloat * 4
ambientLight = lightArrayType(0.3, 0.3, 0.3, 1.0)
diffuseLight = lightArrayType(0.7, 0.7, 0.7, 1.0)
specular = lightArrayType(1.0, 1.0, 1.0, 1.0)
lightPos = (GLfloat * 4)(-75.0, 150.0, -50.0, 0.0)
specref = (GLfloat * 4)(1.0, 1.0, 1.0, 1.0)

shadowMat = M3DMatrix44f()

def DrawJet(nShadow):
    
    # Set material color, note we only have to set to black
    # for the shadow once
    if nShadow == 0:
        glColor3ub(128, 128, 128)
    else:
        glColor3ub(0,0,0)

    # Nose Cone - Points straight down
    # Set material color
    glBegin(GL_TRIANGLES)
    
    glNormal3f(0.0, -1.0, 0.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 60.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(15.0,0.0,30.0)
            

    # Verticies for this panel
    vPoints = [ M3DVector3f(15.0, 0.0, 30.0),
                M3DVector3f(0.0, 15.0, 30.0),
                M3DVector3f(0.0, 0.0, 60.0)]
                
    # Calculate the normal for the plane
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(0.0, 0.0, 60.0),
                M3DVector3f(0.0, 15.0, 30.0),
                M3DVector3f(-15.0, 0.0, 30.0)]
                
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    


    # Body of the Plane ############
    vPoints = [ M3DVector3f(-15.0, 0.0, 30.0),
                M3DVector3f(0.0, 15.0, 30.0),
                M3DVector3f(0.0, 0.0, -56.0)]
                
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
        
    vPoints = [ M3DVector3f(0.0, 0.0, -56.0),
                M3DVector3f(0.0, 15.0, 30.0),
                M3DVector3f(15.0, 0.0, 30.0)]
                
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(15.0,0.0,30.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(0.0, 0.0, -56.0)

    #######################
    # Left wing
    # Large triangle for bottom of wing
    
    vPoints = [ M3DVector3f(0.0, 2.0, 27.0),
                M3DVector3f(-60.0, 2.0, -8.0),
                M3DVector3f(60, 2.0, -8.0)]
                
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(60.0, 2.0, -8.0),
                M3DVector3f(0.0, 7.0, -8.0),
                M3DVector3f(0.0, 2.0, 27.0)]
                
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(60.0, 2.0, -8.0),
                M3DVector3f(-60.0, 2.0, -8.0),
                M3DVector3f(0.0, 7.0, -8.0)]

    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(0.0, 2.0, 27.0),
                M3DVector3f(0.0, 7.0, -8.0),
                M3DVector3f(-60.0, 2.0, -8.0)]
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
            
                    
    # Tail section###############
    # Bottom of back fin
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-30.0, -0.50, -57.0)
    glVertex3f(30.0, -0.50, -57.0)
    glVertex3f(0.0,-0.50,-40.0)

    vPoints = [ M3DVector3f(0.0, -0.5, -40.0),
                M3DVector3f(30.0, -0.5, -57.0),
                M3DVector3f(0.0, 4.0, -57.0)]

    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(0.0, 4.0, -57.0),
                M3DVector3f(-30.0, -0.5, -57.0),
                M3DVector3f(0.0, -0.5, -40.0)]
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(30.0, -0.5, -57.0),
                M3DVector3f(-30.0, -0.5, -57.0),
                M3DVector3f(0.0, 4.0, -57.0)]
    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    

    vPoints = [ M3DVector3f(0.0, 0.5, -40.0),
                M3DVector3f(3.0, 0.5, -57.0),
                M3DVector3f(0.0, 25.0, -65.0)]

    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
                 
    vPoints = [ M3DVector3f(0.0, 25.0, -65.0),
                M3DVector3f(-3.0, 0.5, -57.0),
                M3DVector3f(0.0, 0.5, -40.0)]

    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])
    
    vPoints = [ M3DVector3f(3.0, 0.5, -57.0),
                M3DVector3f(-3.0, 0.5, -57.0),
                M3DVector3f(0.0, 25.0, -65.0)]

    vNormal = m3dFindNormal(vPoints[0], vPoints[1], vPoints[2])
    glNormal3fv(vNormal)
    glVertex3fv(vPoints[0])
    glVertex3fv(vPoints[1])
    glVertex3fv(vPoints[2])


    glEnd()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        global shadowMat
        window.Window.__init__(self, *args, **kwargs)

        # Any three points on the ground (counter clockwise order)
        points = [ M3DVector3f(-30.0, -149.0, -20.0),
                        M3DVector3f(-30.0, -149.0, 20.0),
                        M3DVector3f(40.0, -149.0, 20.0) ]

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out

        # Enable Lighting
        glEnable(GL_LIGHTING)
        
        # Setup and enable light 0
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glEnable(GL_LIGHT0)
        
        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # All materials hereafter have full specular reflectivity
        # with a high shine
        glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
        glMateriali(GL_FRONT, GL_SHININESS, 128)

        # light blue background
        glClearColor(0.0, 0.0, 1.0, 1.0)
        
        # Get the plane equation from three points on the ground

        vPlaneEquation = m3dGetPlaneEquation(points[0], points[1], points[2])

        # Calculate projection matrix to draw shadow on the ground
        shadowMat = m3dMakePlanarShadowMatrix(vPlaneEquation, lightPos)
        glEnable(GL_NORMALIZE)
        
    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the ground, we do manual shading to a darker green
        # in the background to give the illusion of depth
        glBegin(GL_QUADS)
        
        glColor3ub(0,32,0)
        glVertex3f(400.0, -150.0, -200.0)
        glVertex3f(-400.0, -150.0, -200.0)
        glColor3ub(0,255,0)
        glVertex3f(-400.0, -150.0, 200.0)
        glVertex3f(400.0, -150.0, 200.0)
        
        glEnd()

        # Save the matrix state and do the rotations
        glPushMatrix()

        # Draw jet at new orientation, put light in correct position
        # before rotating the jet
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        DrawJet(0)

        # Restore original matrix state
        glPopMatrix()


        # Get ready to draw the shadow and the ground
        # First disable lighting and save the projection state
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glPushMatrix()

        # Multiply by shadow projection matrix
        glMultMatrixf(shadowMat)

        # Now rotate the jet around in the new flattend space
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Pass true to indicate drawing shadow
        DrawJet(1)

        # Restore the projection to normal
        glPopMatrix()

        # Draw the light source
        glPushMatrix()
        glTranslatef(lightPos[0],lightPos[1], lightPos[2])
        glColor3ub(255,255,0)
        glutSolidSphere(5.0,10,10)
        glPopMatrix()

        # Restore lighting state variables
        glEnable(GL_DEPTH_TEST)

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        fAspect = float(w)/float(h)
        gluPerspective(60.0, fAspect, 200.0, 500.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Move out Z axis so we can see everything
        glTranslatef(0.0, 0.0, -400.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

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
    w = MainWindow(800, 600, caption='Shadow', resizable=True)
    pyglet.app.run()
