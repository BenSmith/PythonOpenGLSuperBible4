#!/usr/bin/env python
# Demonstrates Perspective Projection
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Perspect.cpp
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
# Earth and Moon angle of revolution
fMoonRot = 0.0
fEarthRot = 0.0
lightPos = lightArrayType(0.0, 0.0, 0.0, 1.0)

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Light values and coordinates
        
        whiteLight = lightArrayType(0.2, 0.2, 0.2, 1.0)
        sourceLight = lightArrayType(0.8, 0.8, 0.8, 1.0)

        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0)

    # Called to draw scene
    def on_draw(self):
        
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the matrix state and do the rotations
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Translate the whole scene out and into view	
        glTranslatef(0.0, 0.0, -300.0)
        
        # Set material color, Red
        # Sun
        glDisable(GL_LIGHTING)
        glColor3ub(255, 255, 0)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 15.0, 30, 17)    
        gluDeleteQuadric(sphere)
        glEnable(GL_LIGHTING)

        # Move the light after we draw the sun!
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

        # Rotate coordinate system
        glRotatef(fEarthRot, 0.0, 1.0, 0.0)

        # Draw the Earth
        glColor3ub(0,0,255)
        glTranslatef(105.0,0.0,0.0)
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 15.0, 30, 17)    
        gluDeleteQuadric(sphere)

        # Rotate from Earth based coordinates and draw Moon
        glColor3ub(200,200,200)
        glRotatef(fMoonRot,0.0, 1.0, 0.0)
        glTranslatef(30.0, 0.0, 0.0)

        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, True)
        gluSphere(sphere, 6.0, 30, 17)    
        gluDeleteQuadric(sphere)

        # Restore the matrix state
        glPopMatrix()	# Modelview matrix

        
    def on_resize(self, w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        fAspect = float(w)/float(h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # field of view of 45 degrees, near and far planes 1.0 and 425
        gluPerspective(45.0, fAspect, 1.0, 425.0)
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

    def update(self, blah):
        global fEarthRot, fMoonRot
        
        # Step earth orbit 5 degrees
        fEarthRot += 5.0
        if(fEarthRot > 360.0):
            fEarthRot = 0.0
        fMoonRot+= 15.0
        if(fMoonRot > 360.0):
            fMoonRot = 0.0

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption="Earth/Moon/Sun System", resizable=True)
    pyglet.clock.schedule_interval(w.update, 1/10.0)
    pyglet.app.run()
