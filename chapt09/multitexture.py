#!/usr/bin/env python
# Demonstrates a applying a cube map to an object (sphere) using
# texgen, and using the same map for the skybox applying the coordinates
# manually
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on: cubemap.cpp
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

from math3d import M3DMatrix44f, m3dInvertMatrix44
from glframe import GLFrame
from fakeglut import glutSolidSphere
from gltools import gltDrawSphere

frameCamera = GLFrame()
textureObjects = (GLuint * 2)()
CUBE_MAP = 0
COLOR_MAP = 1

# Six sides of a cube map
szCubeFaces = ["pos_x.jpg", "neg_x.jpg", "pos_y.jpg", "neg_y.jpg", "pos_z.jpg", "neg_z.jpg"]
cube = (GLenum * 6)(GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                     # pyglet reverses y axis
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                     GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                     GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                     GL_TEXTURE_CUBE_MAP_NEGATIVE_Z)

# Draw the skybox. This is just six quads, with texture
# coordinates set to the corners of the cube map
def DrawSkyBox():
    fExtent = 15.0
    
    glBegin(GL_QUADS)
    #######################
    # Negative X
    # Note, we must now use the multi-texture version of glTexCoord
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)


    #######################/
    #  Postive X
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)


    ########################
    # Negative Z 
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)


    ########################
    # Positive Z 
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)


    #########################
    # Positive Y
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, 1.0)
    glVertex3f(-fExtent, fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, 1.0, -1.0)
    glVertex3f(-fExtent, fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, -1.0)
    glVertex3f(fExtent, fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, 1.0, 1.0)
    glVertex3f(fExtent, fExtent, fExtent)


    #########################/
    # Negative Y
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, -1.0)
    glVertex3f(-fExtent, -fExtent, -fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, -1.0, -1.0, 1.0)
    glVertex3f(-fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, 1.0)
    glVertex3f(fExtent, -fExtent, fExtent)
    
    glMultiTexCoord3f(GL_TEXTURE1, 1.0, -1.0, -1.0)
    glVertex3f(fExtent, -fExtent, -fExtent)
    glEnd()


class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Cull backs of polygons
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
            
        glGenTextures(2, textureObjects)
            
        # Set up texture maps   
        
        # Cube Map
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureObjects[CUBE_MAP])
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)        
      
        # Load Cube Map images
        for i in range(6):
            # Load this texture map
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_GENERATE_MIPMAP, GL_TRUE)
            img = pyglet.image.load(szCubeFaces[i])
            glTexImage2D(cube[i], 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
            
        # Color map
        glBindTexture(GL_TEXTURE_2D, textureObjects[COLOR_MAP])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        img = pyglet.image.load("tarnish.jpg")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
        
        ##################################/
        # Set up the texture units

        # First texture unit contains the color map
        glActiveTexture(GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textureObjects[COLOR_MAP])
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)   # Decal tarnish
        
        # Second texture unit contains the cube map
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureObjects[CUBE_MAP])
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
        glEnable(GL_TEXTURE_CUBE_MAP)
        
        # Multiply this texture by the one underneath
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    def __del__(self):
        glDeleteTextures(2, textureObjects)
        
    # Called to draw scene
    def on_draw(self):
        # Clear the window
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        glPushMatrix() 
        frameCamera.ApplyCameraTransform() # Move the camera about

        # Sky Box is manually textured
        glActiveTexture(GL_TEXTURE0)
        glDisable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE1)

        glEnable(GL_TEXTURE_CUBE_MAP)
        glDisable(GL_TEXTURE_GEN_S)
        glDisable(GL_TEXTURE_GEN_T)
        glDisable(GL_TEXTURE_GEN_R)     
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
#        DrawSkyBox()
 

        # Use texgen to apply cube map
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glEnable(GL_TEXTURE_GEN_R)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
       
        glActiveTexture(GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)

        glPushMatrix()
        glTranslatef(0.0, 0.0, -3.0)    

        glActiveTexture(GL_TEXTURE1)
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        
        # Invert camera matrix (rotation only) and apply to 
        # texture coordinates
        invert = M3DMatrix44f()
        
        m = frameCamera.GetCameraOrientation()
        m3dInvertMatrix44(invert, m)
        glMultMatrixf(invert)

        glColor3f(1.0, 1.0, 1.0)
        gltDrawSphere(0.75, 41, 41)

        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
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
        gluPerspective(35.0, fAspect, 1.0, 2000.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='OpenGL Cube Maps', resizable=True)
    pyglet.app.run()
