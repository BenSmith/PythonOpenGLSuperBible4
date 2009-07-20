#!/usr/bin/env python
# Demonstrates vertex arrays (with point sprites!)
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# based on starrynight.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from math import cos, sin
from pyglet.gl import *
from pyglet import window
from random import randint

import sys
sys.path.append("../shared")

from math3d import M3DVector2f


# Array of small stars
SMALL_STARS = 100
vSmallStars = (GLfloat * 2 * SMALL_STARS)()

MEDIUM_STARS = 40
vMediumStars = (GLfloat * 2 * MEDIUM_STARS)()

LARGE_STARS = 40
vLargeStars = (GLfloat * 2 * LARGE_STARS)()

SCREEN_X = 800
SCREEN_Y = 600

drawMode = 3
textureObjects = (GLuint * 2)()
class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Turn off blending and all smoothing
        if drawMode == 1:
            glDisable(GL_BLEND)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_POINT_SPRITE)
            
        # Turn on antialiasing, and give hint to do the best
        # job possible.
        if drawMode == 2:
            
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)
            glEnable(GL_POINT_SMOOTH)
            glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_POINT_SPRITE)

        # Point Sprites
        elif drawMode == 3:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_POLYGON_SMOOTH)
   
        # Populate star list
        for i in range(0, SMALL_STARS):
            vSmallStars[i][0] = float(randint(0, SCREEN_X))
            vSmallStars[i][1] = float(randint(0, SCREEN_Y - 100))+100.0

        # Populate star list
        for i in range(0, MEDIUM_STARS):
            vMediumStars[i][0] = float(randint(0, SCREEN_X * 10))/10.0
            vMediumStars[i][1] = float(randint(0, SCREEN_Y - 100))+100.0

        # Populate star list
        for i in range(0, LARGE_STARS):
            vLargeStars[i][0] = float(randint(0, SCREEN_X * 10))/10.0
            vLargeStars[i][1] = float(randint(0, SCREEN_Y - 100) * 10.0)/ 10.0 +100.0
            
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        # Set drawing color to white
        glColor3f(0.0, 0.0, 0.0)

        # Load our textures
        glGenTextures(2, textureObjects)
        glBindTexture(GL_TEXTURE_2D, textureObjects[0])
           
        # Load this texture map
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        img = pyglet.image.load('star.png')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glBindTexture(GL_TEXTURE_2D, textureObjects[1])
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        img = pyglet.image.load('moon.png')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def __del__(self):
        glDeleteTextures(2, textureObjects)

    # Called to draw scene
    def on_draw(self):
    
        x = 700.0     # Location and radius of moon
        y = 500.0
        r = 50.0
        angle = 0.0   # Another looping variable

        # Clear the window
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
             
        # Everything is white
        glColor3f(1.0, 1.0, 1.0)
        
        if (drawMode == 3):
            glEnable(GL_POINT_SPRITE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, textureObjects[0])
            glEnable(GL_BLEND)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        
        # Draw small stars
        glPointSize(7.0)
        glVertexPointer(2, GL_FLOAT, 0, vSmallStars)
        glDrawArrays(GL_POINTS, 0, SMALL_STARS)
        
        # Draw medium sized stars
        glPointSize(12.0)
        glVertexPointer(2, GL_FLOAT, 0, vMediumStars)
        glDrawArrays(GL_POINTS, 0, MEDIUM_STARS)
            
        # Draw largest stars
        glPointSize(20.0)
        glVertexPointer(2, GL_FLOAT, 0, vLargeStars)
        glDrawArrays(GL_POINTS, 0, LARGE_STARS)
            
        glDisableClientState(GL_VERTEX_ARRAY)
        
        glPointSize(120.0)
        if (drawMode == 3):
            glDisable(GL_BLEND)
            glBindTexture(GL_TEXTURE_2D, textureObjects[1])
            
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_POINT_SPRITE)

        # Draw distant horizon
        glLineWidth(3.5)
        glBegin(GL_LINE_STRIP)
        
        glVertex2f(0.0, 25.0)
        glVertex2f(50.0, 100.0)
        glVertex2f(100.0, 25.0)
        glVertex2f(225.0, 115.0)
        glVertex2f(300.0, 50.0)
        glVertex2f(375.0, 100.0)
        glVertex2f(460.0, 25.0)
        glVertex2f(525.0, 100.0)
        glVertex2f(600.0, 20.0)
        glVertex2f(675.0, 70.0)
        glVertex2f(750.0, 25.0)
        glVertex2f(800.0, 90.0)
        
        glEnd()


    def on_resize(self, w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)

        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Establish clipping volume (left, right, bottom, top, near, far)
        gluOrtho2D(0.0, SCREEN_X, 0.0, SCREEN_Y)


        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='', resizable=True)
    pyglet.app.run()

