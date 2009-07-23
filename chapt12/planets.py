#!/usr/bin/env python
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on Planets.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from math import cos, sin
from pyglet.gl import *
from pyglet import window
from pyglet.window import mouse

# Define object names
SUN = 1
MERCURY = 2
VENUS = 3
EARTH = 4
MARS = 5

global fAspect

lightArrayType = GLfloat * 4

# Just draw a sphere of some given radius
def DrawSphere(radius):
    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluSphere(pObj, radius, 26, 13)
    gluDeleteQuadric(pObj)


def ProcessPlanet(id):
    if id == SUN:
        print ("You clicked on the Sun!")
    elif id == MERCURY:
        print ("You clicked on Mercury!")
    elif id == VENUS:
        print ("You clicked on Venus!")
    elif id == EARTH:
        print ("You clicked on Earth!")
    elif id == MARS:
        print ("You clicked on Mars!")
    else:
        print ("Nothing was clicked on!")
        

#############################
# Process the selection, which is triggered by a right mouse
# click at (xPos, yPos).

BUFFER_LENGTH = 64
# Space for selection buffer
selectBuff = (GLuint * BUFFER_LENGTH)()

def ProcessSelection(window, xPos, yPos):

    # Hit counter and viewport storage
    viewport = (GLint * 4)()

    # Setup selection buffer
    glSelectBuffer(BUFFER_LENGTH, selectBuff)

    # Get the viewport
    glGetIntegerv(GL_VIEWPORT, viewport)

    # Switch to projection and save the matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()

    # Change render mode
    glRenderMode(GL_SELECT)

    # Establish new clipping volume to be unit cube around
    # mouse cursor point (xPos, yPos) and extending two pixels
    # in the vertical and horizontal direction
    glLoadIdentity()
    gluPickMatrix(xPos, viewport[3] - yPos + viewport[1], 2,2, viewport)

    # Apply perspective matrix 
    gluPerspective(45.0, fAspect, 1.0, 425.0)

    # Draw the scene
    window.on_draw()

    # Collect the hits
    hits = glRenderMode(GL_RENDER)

    # If a single hit occurred, display the info.
    if(hits == 1):
        ProcessPlanet(selectBuff[3])
    else:
        print ("Nothing was clicked on!")
        
    # Restore the projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    # Go back to modelview for normal rendering
    glMatrixMode(GL_MODELVIEW)



class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Lighting values
        dimLight = lightArrayType(0.1, 0.1, 0.1, 1.0)
        sourceLight = lightArrayType(0.65, 0.65, 0.65, 1.0)
        lightPos = (GLfloat * 4)(0.0, 0.0, 0.0, 1.0)

        # Light values and coordinates
        glEnable(GL_DEPTH_TEST)	# Hidden surface removal
        glFrontFace(GL_CCW)		# Counter clock-wise polygons face out
        glEnable(GL_CULL_FACE)		# Do not calculate insides

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Setup and enable light 0
        glLightfv(GL_LIGHT0,GL_AMBIENT,dimLight)
        glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Gray background
        glClearColor(0.60, 0.60, 0.60, 1.0 )
        
    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        # Save the matrix state and do the rotations
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Translate the whole scene out and into view	
        glTranslatef(0.0, 0.0, -300.0)	

        # Initialize the names stack
        glInitNames()
        glPushName(0)

        
        # Name and draw the Sun
        glColor3f(1.0, 1.0, 0.0)
        glLoadName(SUN)
        DrawSphere(15.0)

        # Draw Mercury
        glColor3f(0.5, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(24.0, 0.0, 0.0)
        glLoadName(MERCURY)
        DrawSphere(2.0)
        glPopMatrix()

        # Draw Venus
        glColor3f(0.5, 0.5, 1.0)
        glPushMatrix()
        glTranslatef(60.0, 0.0, 0.0)
        glLoadName(VENUS)
        DrawSphere(4.0)
        glPopMatrix()

        # Draw the Earth
        glColor3f(0.0, 0.0, 1.0)
        glPushMatrix()
        glTranslatef(100.0,0.0,0.0)
        glLoadName(EARTH)
        DrawSphere(8.0)
        glPopMatrix()

        # Draw Mars
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(150.0, 0.0, 0.0)
        glLoadName(MARS)
        DrawSphere(4.0)
        glPopMatrix()


        # Restore the matrix state
        glPopMatrix()	# Modelview matrix


    #############################
    # Set viewport and projection
    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1
        
        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        global fAspect
        fAspect = float(w) / float(h)
        
        # Reset the coordinate system before modifying
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set the clipping volume
        gluPerspective(45.0, fAspect, 1.0, 425.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_press(self, x, y, button, mod):
        if button == mouse.LEFT:
            ProcessSelection(self, x, y)

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Pick a Planet', resizable=True)
    pyglet.app.run()
