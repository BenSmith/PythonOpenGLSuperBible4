#!/usr/bin/env python
# pyramid.py
# Demonstrates Simple Texture Mapping
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Pyramid.cpp
# OpenGL SuperBible
# Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
import sys
sys.path.append("../shared")

from math import cos, sin

import math3d

xRot = 0.0
yRot = 0.0

lightArrayType = GLfloat * 4

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Light values and coordinates
        whiteLight = lightArrayType(0.45, 0.45, 0.45, 1.0)
        sourceLight = lightArrayType(0.25, 0.25, 0.25, 1.0)
        lightPos = lightArrayType(-50.0, 25.0, 250.0, 0.0)

        glEnable(GL_DEPTH_TEST)       # Hidden surface removal
        glFrontFace(GL_CCW)             # Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)
        
        # Enable lighting
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
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # Load texture
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        img = pyglet.image.load("Stone.jpg")
        
        glTexImage2D(GL_TEXTURE_2D, 0, img.components, img.width, img.height, 0, img.format, GL_UNSIGNED_BYTE, img.get_texture())
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnable(GL_TEXTURE_2D)

    # Called to draw scene
    def on_draw(self):
        vNormal = M3DVector3f()
        vCorners = [ M3DVector3f(0.0, 0.8, 0.0),
                            M3DVector3f(-0.5, 0.0, -0.5),
                            M3DVector3f(0.5, 0.0, -0.5),
                            M3DVector3f(0.5, 0.0, 0.5),
                            M3DVector3f(-0.5, 0.0, 0.5),
                        ]

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the matrix state and do the rotations
        glPushMatrix()
        # Move object back and do in place rotation
        glTranslatef(0.0, -0.25, -4.0)
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Draw the Pyramid
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        
        # Bottom section - two triangles
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        
        glTexCoord2f(0.0, 1.0)
        glVertex3fv(vCorners[1])
        
        
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[3])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        
        # Front Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[4], vCorners[3])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[4])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[3])
        
        # Left Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[1], vCorners[4])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[1])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[4])

        # Back Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[2], vCorners[1])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[2])
        
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[1])
        
        # Right Face
        m3dFindNormal(vNormal, vCorners[0], vCorners[3], vCorners[2])
        glNormal3fv(vNormal)
        glTexCoord2f(0.5, 1.0)
        glVertex3fv(vCorners[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3fv(vCorners[3])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(vCorners[2])
        
        glEnd()
    

        # Restore the matrix state
        glPopMatrix()


    # Called when the window has changed size (including when the window is created)
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

        # Produce the perspective projection
        gluPerspective(35.0, fAspect, 1.0, 40.0)
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
    w = MainWindow(800, 600, caption='Textured Pyramid', resizable=True)
    pyglet.app.run()
