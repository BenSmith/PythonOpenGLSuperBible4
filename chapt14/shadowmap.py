#!/usr/bin/env python
# Demonstrates shadow mapping
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on shadowmap.cpp
# OpenGL SuperBible, Chapter 14
# Program by Benjamin Lipchak

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
import ctypes
from math import cos, sin, atan, sqrt
from time import sleep

import sys
sys.path.append("../shared")
from sys import exit
from math3d import M3DMatrix44f, m3dLoadIdentity44, m3dTranslateMatrix44, m3dScaleMatrix44, m3dMatrixMultiply44, m3dTransposeMatrix44, m3dRadToDeg
from forpyglet import glutSolidCube, glutSolidSphere, glutSolidCone, glutSolidOctahedron, gltDrawTorus

ambientShadowAvailable = False
npotTexturesAvailable = False
controlCamera = True      # xyz keys will control lightpos
noShadows = False         # normal lighting
showShadowMap = False     # show the shadowmap texture

factor = 4.0                  # for polygon offset

windowWidth = 1024               # window size
windowHeight = 512

shadowWidth = 1024               # set based on window size
shadowHeight = 512
shadowTextureID = GLuint(0)

maxTexSize = GLint(0)                      # maximum allowed size for 1D/2D texture

ambientLight = (GLfloat * 4)(0.2, 0.2, 0.2, 1.0)
diffuseLight = (GLfloat * 4)(0.7, 0.7, 0.7, 1.0)
noLight = (GLfloat * 4)(0.0, 0.0, 0.0, 1.0)
lightPos = (GLfloat * 4)(100.0, 300.0, 100.0, 1.0)

cameraPos = (GLfloat * 4)(100.0, 150.0, 200.0, 1.0)
cameraZoom = 0.3

textureMatrix = M3DMatrix44f()

# Called to draw scene objects
def DrawModels(drawBasePlane):
    if drawBasePlane:
        # Draw plane that the objects rest on
        glColor3f(0.0, 0.0, 0.90) # Blue
        glNormal3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-100.0, -25.0, -100.0)
        glVertex3f(-100.0, -25.0, 100.0)
        glVertex3f(100.0,  -25.0, 100.0)
        glVertex3f(100.0,  -25.0, -100.0)
        glEnd()

    # Draw red cube
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(48.0)

    # Draw green sphere
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(-60.0, 0.0, 0.0)
    glutSolidSphere(25.0, 50, 50)
    glPopMatrix()

    # Draw yellow cone
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(60.0, 0.0, -24.0)
    glutSolidCone(25.0, 50.0, 50, 50)
    glPopMatrix()

    # Draw magenta torus
    glColor3f(1.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 60.0)
    gltDrawTorus(8.0, 16.0, 50, 50)
    glPopMatrix()

    # Draw cyan octahedron
    glColor3f(0.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.0, -60.0)
    glScalef(25.0, 25.0, 25.0)
    glutSolidOctahedron()
    glPopMatrix()

# Called to regenerate the shadow map
def RegenerateShadowMap():
    lightModelview = (GLfloat * 16)()
    lightProjection = (GLfloat * 16)()
    sceneBoundingRadius = 95.0 # based on objects in scene

    # Save the depth precision for where it's useful
    lightToSceneDistance = sqrt(lightPos[0] * lightPos[0] + lightPos[1] * lightPos[1] + lightPos[2] * lightPos[2])
    nearPlane = lightToSceneDistance - sceneBoundingRadius
    
    # Keep the scene filling the depth texture
    fieldOfView = m3dRadToDeg(2.0 * atan(sceneBoundingRadius / lightToSceneDistance))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fieldOfView, 1.0, nearPlane, nearPlane + (2.0 * sceneBoundingRadius))
    glGetFloatv(GL_PROJECTION_MATRIX, lightProjection)
    
    # Switch to light's point of view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(lightPos[0], lightPos[1], lightPos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glGetFloatv(GL_MODELVIEW_MATRIX, lightModelview)
    glViewport(0, 0, shadowWidth, shadowHeight)

    # Clear the depth buffer only
    glClear(GL_DEPTH_BUFFER_BIT)

    # All we care about here is resulting depth values
    glShadeModel(GL_FLAT)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_NORMALIZE)
    glColorMask(0, 0, 0, 0)

    # Overcome imprecision
    glEnable(GL_POLYGON_OFFSET_FILL)

    # Draw objects in the scene except base plane
    # which never shadows anything
    DrawModels(GL_FALSE)

    # Copy depth values into depth texture
    glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 0, 0, shadowWidth, shadowHeight, 0)

    # Restore normal drawing state
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glColorMask(1, 1, 1, 1)
    glDisable(GL_POLYGON_OFFSET_FILL)

    # Set up texture matrix for shadow map projection,
    # which will be rolled into the eye linear
    # texture coordinate generation plane equations
    tempMatrix = M3DMatrix44f()
    m3dLoadIdentity44(tempMatrix)
    m3dTranslateMatrix44(tempMatrix, 0.5, 0.5, 0.5)
    m3dScaleMatrix44(tempMatrix, 0.5, 0.5, 0.5)
    m3dMatrixMultiply44(textureMatrix, tempMatrix, lightProjection)
    m3dMatrixMultiply44(tempMatrix, textureMatrix, lightModelview)
    
    # transpose to get the s, t, r, and q rows for plane equations
    m3dTransposeMatrix44(textureMatrix, tempMatrix)

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        global maxTexSize, ambientShadowAvailable
        window.Window.__init__(self, *args, **kwargs)
        
        print ("Shadow Mapping Demo\n")

        # Make sure required functionality is available!

        if not gl_info.have_version(1, 4) and not gl_info.have_extension(GL_ARB_shadow):
            print ("Neither OpenGL 1.4 nor GL_ARB_shadow extension is available!")
            sleep(2)
            exit(0)

        # Check for optional extensions
        if gl_info.have_extension(GL_ARB_shadow_ambient):
            ambientShadowAvailable = True
        else:
            print ("GL_ARB_shadow_ambient extension not available!")
            print ("Extra ambient rendering pass will be required.\n")
            sleep(2)

        if gl_info.have_version(2, 0) or gl_info.have_extension(GL_ARB_texture_non_power_of_two):
            npotTexturesAvailable = True
        else:
            print ("Neither OpenGL 2.0 nor GL_ARB_texture_non_power_of_two extension")
            print ("is available!  Shadow map will be lower resolution (lower quality).\n")
            sleep(2)

        glGetIntegerv(GL_MAX_TEXTURE_SIZE, ctypes.byref(maxTexSize))

        print ("Controls:")
        print ("\tRight-click for menu\n")
        print ("\tx/X\t\tMove +/- in x direction")
        print ("\ty/Y\t\tMove +/- in y direction")
        print ("\tz/Z\t\tMove +/- in z direction\n")
        print ("\tf/F\t\tChange polygon offset factor +/-\n")
        print ("\tq\t\tExit demo\n")
        
        # Black background
        glClearColor(0.0, 0.0, 0.0, 1.0 )

        # Hidden surface removal
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glPolygonOffset(factor, 0.0)

        # Set up some lighting state that never changes
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHT0)

        # Set up some texture state that never changes
        glGenTextures(1, ctypes.byref(shadowTextureID))
        glBindTexture(GL_TEXTURE_2D, shadowTextureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE, GL_INTENSITY)
        if (ambientShadowAvailable):
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FAIL_VALUE_ARB, 0.5)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)

        RegenerateShadowMap()

    def __del__(self):
        pass
        
    # Called to draw scene
    def on_draw(self):
        # Track camera angle
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (windowWidth > windowHeight):
            ar = windowWidth / windowHeight
            glFrustum(-ar * cameraZoom, ar * cameraZoom, -cameraZoom, cameraZoom, 1.0, 1000.0)
        else:
            ar = windowHeight / windowWidth
            glFrustum(-cameraZoom, cameraZoom, -ar * cameraZoom, ar * cameraZoom, 1.0, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(cameraPos[0], cameraPos[1], cameraPos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glViewport(0, 0, windowWidth, windowHeight)
        
        # Track light position
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (showShadowMap):
            # Display shadow map for educational purposes
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glMatrixMode(GL_TEXTURE)
            glPushMatrix()
            glLoadIdentity()
            glEnable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_NONE)
            
            # Show the shadowMap at its actual size relative to window
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(-1.0, -1.0)
            glTexCoord2f(1.0, 0.0)
            glVertex2f((shadowWidth/windowWidth)*2.0-1.0, -1.0)
            glTexCoord2f(1.0, 1.0)
            glVertex2f((shadowWidth/windowWidth)*2.0-1.0, (shadowHeight/windowHeight)*2.0-1.0)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(-1.0, (shadowHeight/windowHeight)*2.0-1.0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_LIGHTING)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            gluPerspective(45.0, 1.0, 1.0, 1000.0)
            glMatrixMode(GL_MODELVIEW)
        
        elif noShadows:
            # Set up some simple lighting
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)

            # Draw objects in the scene including base plane
            DrawModels(GL_TRUE)
        
        else:
            if not ambientShadowAvailable:
                lowAmbient = (GLfloat * 4)(0.1, 0.1, 0.1, 1.0)
                lowDiffuse = (GLfloat * 4)(0.35, 0.35, 0.35, 1.0)

                # Because there is no support for an "ambient"
                # shadow compare fail value, we'll have to
                # draw an ambient pass first...
                glLightfv(GL_LIGHT0, GL_AMBIENT, lowAmbient)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, lowDiffuse)

                # Draw objects in the scene, including base plane
                DrawModels(GL_TRUE)

                # Enable alpha test so that shadowed fragments are discarded
                glAlphaFunc(GL_GREATER, 0.9)
                glEnable(GL_ALPHA_TEST)
                
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)

            # Set up shadow comparison
            glEnable(GL_TEXTURE_2D)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_R_TO_TEXTURE)

            # Set up the eye plane for projecting the shadow map on the scene
            glEnable(GL_TEXTURE_GEN_S)
            glEnable(GL_TEXTURE_GEN_T)
            glEnable(GL_TEXTURE_GEN_R)
            glEnable(GL_TEXTURE_GEN_Q)
            
            matrixPointer = pointer(textureMatrix)
            glTexGenfv(GL_S, GL_EYE_PLANE, matrixPointer[0])
            glTexGenfv(GL_T, GL_EYE_PLANE, matrixPointer[4])
            glTexGenfv(GL_R, GL_EYE_PLANE, matrixPointer[8])
            glTexGenfv(GL_Q, GL_EYE_PLANE, matrixPointer[12])

            # Draw objects in the scene, including base plane
            DrawModels(GL_TRUE)

            glDisable(GL_ALPHA_TEST)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_TEXTURE_GEN_S)
            glDisable(GL_TEXTURE_GEN_T)
            glDisable(GL_TEXTURE_GEN_R)
            glDisable(GL_TEXTURE_GEN_Q)
        
        
        if glGetError() != GL_NO_ERROR:
            print ("GL Error!\n")

    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):
        global windowWidth, windowHeight, shadowWidth, shadowHeight
        windowWidth = shadowWidth = w
        windowHeight = shadowHeight = h
        
        if not npotTexturesAvailable:
            # Find the largest power of two that will fit in window.

            # Try each width until we get one that's too big
            i = 0
            while (1 << i) <= shadowWidth:
                i += 1
            shadowWidth = (1 << (i-1))

            # Now for height
            i = 0
            while (1 << i) <= shadowHeight:
                i += 1
            shadowHeight = (1 << (i-1))

        if shadowWidth > maxTexSize:
            shadowWidth = maxTexSize
        if shadowHeight > maxTexSize:
            shadowHeight = maxTexSize

        RegenerateShadowMap()

    # Respond to arrow keys by moving the camera frame of reference
    def on_key_press(self, symbol, modifier):
        if symbol == key.UP:
            pass
            
# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Shadow Mapping Demo', resizable=True)
    pyglet.app.run()
