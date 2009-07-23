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
EARTH = 1
MARS = 2
MOON1 = 3
MOON2 = 4

global fAspect

lightArrayType = GLfloat * 4

# Just draw a sphere of some given radius
def DrawSphere(radius):
    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluSphere(pObj, radius, 26, 13)
    gluDeleteQuadric(pObj)

# Parse the selection buffer to see which 
# planet/moon was selected
def ProcessPlanet(pSelectBuff):
    # How many names on the name stack
    count = pSelectBuff[0]
    cMessage = "Error, no selection detected"
    # Bottom of the name stack
    id = pSelectBuff[3]
    
    # Select on earth or mars, whichever was picked
    if id == EARTH:
        cMessage = "You clicked Earth."
        
        # If there is another name on the name stack,
        # then it must be the moon that was selected
        # This is what was actually clicked on
        if count == 2:
            cMessage += " - Specifically the moon."
            
    elif id == MARS:
        cMessage = "You clicked Mars."
        
        if count == 2:
            if pSelectBuff[4] == MOON1:
                cMessage += " - Specifically Moon #1."
            else:
                cMessage += " - Specifically Moon #2."
    print cMessage
    
        

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
        ProcessPlanet(selectBuff)
    else:
        print ("You clicked empty space!")
        
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
        
        # Draw the Earth
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(-100.0,0.0,0.0)
        glLoadName(EARTH)
        DrawSphere(30.0)
        
        # Draw the Moon
        glTranslatef(45.0, 0.0, 0.0)
        glColor3f(0.85, 0.85, 0.85)
        glPushName(MOON1)
        DrawSphere(5.0)
        glPopName()
        glPopMatrix()

        # Draw Mars
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(100.0, 0.0, 0.0)
        glLoadName(MARS)
        DrawSphere(20.0)

        # Draw Moon1
        glTranslatef(-40.0, 40.0, 0.0)
        glColor3f(0.85, 0.85, 0.85)
        glPushName(MOON1)
        DrawSphere(5.0)
        glPopName()

        # Draw Moon2
        glTranslatef(0.0, -80.0, 0.0)
        glPushName(MOON2)
        DrawSphere(5.0)
        glPopName()
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
