#!/usr/bin/env python
# Ben Smith
# Demonstrates OpenGL Texture Coordinate Generation
# benjamin.coder.smith@gmail.com
#
# based on Texgen.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

import sys
sys.path.append("../shared")

from gltools import gltDrawTorus

# Rotation amounts
xRot = 0.0
yRot = 0.0


toTextures = (GLuint * 2)() # Two texture objects
iRenderMode = 3 # Sphere mapped is default

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate inside of jet

        # White background
        glClearColor(1.0, 1.0, 1.0, 1.0 )
        
        # Decal texture environment
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        # Two textures
        glGenTextures(2, toTextures)

        #####################/
        # Load the main texture
        glBindTexture(GL_TEXTURE_2D, toTextures[0])
        img = pyglet.image.load("stripes.png")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glEnable(GL_TEXTURE_2D)

        #####################/
        # Load environment map
        glBindTexture(GL_TEXTURE_2D, toTextures[1])
        img = pyglet.image.load("environment.jpg")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glEnable(GL_TEXTURE_2D)

        # Turn on texture coordiante generation
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        
        # Sphere Map will be the default
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)


    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Switch to orthographic view for background drawing
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0.0, 1.0, 0.0, 1.0)
        
        glMatrixMode(GL_MODELVIEW)
        glBindTexture(GL_TEXTURE_2D, toTextures[1])    # Background texture

        # We will specify texture coordinates
        glDisable(GL_TEXTURE_GEN_S)
        glDisable(GL_TEXTURE_GEN_T)
        
        # No depth buffer writes for background
        glDepthMask(GL_FALSE)

        # Background image
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0.0, 0.0)
    
        glTexCoord2f(1.0, 0.0)
        glVertex2f(1.0, 0.0)
    
        glTexCoord2f(1.0, 1.0)
        glVertex2f(1.0, 1.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0.0, 1.0)
        glEnd()

        # Back to 3D land
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        # Turn texgen and depth writing back on
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glDepthMask(GL_TRUE)

        # May need to swtich to stripe texture
        if iRenderMode != 3:
            glBindTexture(GL_TEXTURE_2D, toTextures[0])

        # Save the matrix state and do the rotations
        glPushMatrix()
        glTranslatef(0.0, 0.0, -2.0)
        glRotatef(xRot, 1.0, 0.0, 0.0)
        glRotatef(yRot, 0.0, 1.0, 0.0)

        # Draw the tours
        gltDrawTorus(0.35, 0.15, 61, 37)
                    
        # Restore the matrix state
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
        gluPerspective(45.0, fAspect, 1.0, 225.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def on_key_press(self, symbol, modifier):
        global xRot, yRot, iRenderMode
        # Projection plane
        zPlane = (GLfloat * 4)(0.0, 0.0, 1.0, 0.0)
        if symbol == key.UP:
            xRot -= 5.0
        elif symbol == key.DOWN:
            xRot += 5.0
        elif symbol == key.LEFT:
            yRot -= 5.0
        elif symbol == key.RIGHT:
            yRot += 5.0
            
        # Set up textgen based on selection
        elif symbol == key._1:
            # Object Linear
            iRenderMode = 1
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
            glTexGenfv(GL_S, GL_OBJECT_PLANE, zPlane)
            glTexGenfv(GL_T, GL_OBJECT_PLANE, zPlane)
        elif symbol == key._2:
            # Eye Linear
            iRenderMode = 2
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
            glTexGenfv(GL_S, GL_EYE_PLANE, zPlane)
            glTexGenfv(GL_T, GL_EYE_PLANE, zPlane)
        elif symbol == key._3:
            # Sphere Map
            iRenderMode = 3
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
            
        if xRot > 356.0:
            xRot = 0.0
        elif xRot < -1.0:
            xRot = 355.0
            
        if yRot > 356.0:
            yRot = 0.0
        elif yRot < -1.0:
            yRot = 355.0

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Texture Coordinate Generation', resizable=True)
    pyglet.app.run()
