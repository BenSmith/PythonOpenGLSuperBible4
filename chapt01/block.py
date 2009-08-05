#!/usr/bin/env python
# Demonstrates an assortment of basic 3D concepts
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on: Block.cpp
# OpenGL SuperBible, Chapter 1
# Program by Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

import sys
sys.path.append("../shared")

from math3d import M3DVector4f, M3DMatrix44f, m3dGetPlaneEquation, m3dMakePlanarShadowMatrix
from fakeglut import glutWireCube, glutSolidCube
    
# keep track of effects step
nStep = 0

# Lighting data
lightArrayType = GLfloat * 4
lightAmbient = lightArrayType(0.2, 0.2, 0.2, 1.0)
lightDiffuse = lightArrayType(0.7, 0.7, 0.7, 1.0)
lightSpecular = (GLfloat * 3)(0.9, 0.9, 0.9)
materialColor = (GLfloat * 3)(0.8, 0.0, 0.0)

ground = (GLfloat * 3 * 3)((0.0, -25.0, 0.0),
                            (10.0, -25.0, 0.0),
                            (10.0, -25.0, -10.0))
vLightPos = (GLfloat * 4)(-80.0, 120.0, 100.0, 0.0)

textures = (GLuint * 4)()

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glGenTextures(4, textures)
            
        # Load the texture objects
        img = pyglet.image.load("floor.jpg")
        
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,img.width, img.height, 0,
            GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))

        img = pyglet.image.load("block4.jpg")
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,img.width, img.height, 0,
            GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))

        img = pyglet.image.load("block5.jpg")
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,img.width, img.height, 0,
            GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))

        img = pyglet.image.load("block6.jpg")
        glBindTexture(GL_TEXTURE_2D, textures[3])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,img.width, img.height, 0,
            GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
    def __del__(self):
        glDeleteTextures(len(textures), textures)
        
    # Called to draw scene
    def on_draw(self):
        mCubeTransform = M3DMatrix44f()
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)

        glPushMatrix()

        # Draw plane that the cube rests on
        glDisable(GL_LIGHTING)
        if nStep == 5:
            glColor3ub(255,255,255)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textures[0])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-100.0, -25.3, -100.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-100.0, -25.3, 100.0)		
            glTexCoord2f(1.0, 1.0)
            glVertex3f(100.0,  -25.3, 100.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(100.0,  -25.3, -100.0)
            glEnd()
            
        else:
            glColor3f(0.0, 0.0, 0.90) # Blue
            glBegin(GL_QUADS)
            glVertex3f(-100.0, -25.3, -100.0)
            glVertex3f(-100.0, -25.3, 100.0)		
            glVertex3f(100.0,  -25.3, 100.0)
            glVertex3f(100.0,  -25.3, -100.0)
            glEnd()

        # Set drawing color to Red
        glColor3f(1.0, 0.0, 0.0)

        # Enable, disable lighting
        if nStep > 2:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            glEnable(GL_COLOR_MATERIAL)

            glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
            glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glMaterialfv(GL_FRONT, GL_SPECULAR,lightSpecular)
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, materialColor)
            glMateriali(GL_FRONT, GL_SHININESS,128)

        # Move the cube slightly forward and to the left
        glTranslatef(-10.0, 0.0, 10.0)

        if nStep == 0:
            # Just draw the wire framed cube
            glutWireCube(50.0)

            # Same wire cube with hidden line removal simulated
        elif nStep == 1:
            # Front Face (before rotation)
            glBegin(GL_LINES)
            glVertex3f(25.0,25.0,25.0)
            glVertex3f(25.0,-25.0,25.0)
            
            glVertex3f(25.0,-25.0,25.0)
            glVertex3f(-25.0,-25.0,25.0)

            glVertex3f(-25.0,-25.0,25.0)
            glVertex3f(-25.0,25.0,25.0)

            glVertex3f(-25.0,25.0,25.0)
            glVertex3f(25.0,25.0,25.0)
            glEnd()

            # Top of cube
            glBegin(GL_LINES)
            # Front Face
            glVertex3f(25.0,25.0,25.0)
            glVertex3f(25.0,25.0,-25.0)
            
            glVertex3f(25.0,25.0,-25.0)
            glVertex3f(-25.0,25.0,-25.0)

            glVertex3f(-25.0,25.0,-25.0)
            glVertex3f(-25.0,25.0,25.0)

            glVertex3f(-25.0,25.0,25.0)
            glVertex3f(25.0,25.0,25.0)
            glEnd()

            # Last two segments for effect
            glBegin(GL_LINES)
            glVertex3f(25.0,25.0,-25.0)
            glVertex3f(25.0,-25.0,-25.0)

            glVertex3f(25.0,-25.0,-25.0)
            glVertex3f(25.0,-25.0,25.0)
            glEnd()

        # Uniform colored surface, looks 2D and goofey
        elif nStep == 2:
            glutSolidCube(50.0)

        elif nStep == 3:
            glutSolidCube(50.0)

        # Draw a shadow with some lighting
        elif nStep == 4:
            glGetFloatv(GL_MODELVIEW_MATRIX, mCubeTransform)
            glutSolidCube(50.0)
            glPopMatrix()

            # Disable lighting, we'll just draw the shadow as black
            glDisable(GL_LIGHTING)
            
            glPushMatrix()

            pPlane = m3dGetPlaneEquation(ground[0], ground[1], ground[2])
            mCubeTransform = m3dMakePlanarShadowMatrix(pPlane, vLightPos)
            #MakeShadowMatrix(ground, lightpos, cubeXform)
            glMultMatrixf(mCubeTransform)
            
            glTranslatef(-10.0, 0.0, 10.0)			
            
            # Set drawing color to Black
            glColor3f(0.0, 0.0, 0.0)

            glutSolidCube(50.0)

        elif nStep == 5:
            glColor3ub(255,255,255)
            glGetFloatv(GL_MODELVIEW_MATRIX, mCubeTransform)

            # Front Face (before rotation)
            glBindTexture(GL_TEXTURE_2D, textures[1])
            glBegin(GL_QUADS)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(25.0,25.0,25.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(25.0,-25.0,25.0)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-25.0,-25.0,25.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-25.0,25.0,25.0)
            glEnd()

            # Top of cube
            glBindTexture(GL_TEXTURE_2D, textures[2])
            glBegin(GL_QUADS)
            # Front Face
            glTexCoord2f(0.0, 0.0)
            glVertex3f(25.0,25.0,25.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(25.0,25.0,-25.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-25.0,25.0,-25.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-25.0,25.0,25.0)
            glEnd()

            # Last two segments for effect
            glBindTexture(GL_TEXTURE_2D, textures[3])
            glBegin(GL_QUADS)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(25.0,25.0,-25.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(25.0,-25.0,-25.0)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(25.0,-25.0,25.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(25.0,25.0,25.0)
            glEnd()
        

            glPopMatrix()

            # Disable lighting, we'll just draw the shadow as black
            glDisable(GL_LIGHTING)
            glDisable(GL_TEXTURE_2D)
            
            glPushMatrix()

            pPlane = m3dGetPlaneEquation(ground[0], ground[1], ground[2])
            mCubeTransform = m3dMakePlanarShadowMatrix(pPlane, vLightPos)
            glMultMatrixf(mCubeTransform)			
            
            glTranslatef(-10.0, 0.0, 10.0)			
            
            # Set drawing color to Black
            glColor3f(0.0, 0.0, 0.0)
            glutSolidCube(50.0)

        glPopMatrix()
        
    def on_resize(self, w, h):
        # Prevent a divide by zero, when window is too short
        # (you cant make a window of zero width).
        if h == 0:
            h = 1

        # Keep the square square
        if w <= h:
            windowHeight = 100.0*h/w
            windowWidth = 100.0
        else:
            windowWidth = 100.0*w/h
            windowHeight = 100.0

        # Set the viewport to be the entire window
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        glOrtho(-100.0, windowWidth, -100.0, windowHeight, -200.0, 200.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLightfv(GL_LIGHT0,GL_POSITION, vLightPos)

        glRotatef(30.0, 1.0, 0.0, 0.0)
        glRotatef(330.0, 0.0, 1.0, 0.0)
        
    def on_key_press(self, symbol, modifier):
        if symbol == key.SPACE:
            global nStep
            nStep += 1
            if nStep > 5:
                nStep = 0

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='3D Effects Demo', resizable=True)
    pyglet.app.run()
