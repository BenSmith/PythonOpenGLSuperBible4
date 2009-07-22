#!/usr/bin/env python
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on select.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from math import cos, sin
from pyglet.gl import *
from pyglet import window
from pyglet.window import mouse

import sys
sys.path.append("../shared")
from math3d import M3D_PI as M_PI

#############
# Object Names
TORUS  = 1
SPHERE = 2

global fAspect

boundingRect = {'top' : 0, 'bottom' : 0, 'left' : 0, 'right': 0} # Bounding rectangle
selectedObject = 0 # Who is selected

lightArrayType = GLfloat * 4

#############################
# Draw a torus (doughnut)  
# at z = 0... torus aligns with xy plane
def DrawTorus(numMajor, numMinor):

    majorRadius = 0.35
    minorRadius = 0.15
    majorStep = 2.0*M_PI / numMajor
    minorStep = 2.0*M_PI / numMinor

    glEnable(GL_NORMALIZE)
    for i in range(0, numMajor):

        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(0, numMinor):

            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)

            glTexCoord2f(i/numMajor, j/numMinor)
            glNormal3f(x0*c, y0*c, z/minorRadius)
            glVertex3f(x0*r, y0*r, z)

            glTexCoord2f((i+1)/numMajor, j/numMinor)
            glNormal3f(x1*c, y1*c, z/minorRadius)
            glVertex3f(x1*r, y1*r, z)
        glEnd()
    glDisable(GL_NORMALIZE)


#############################
# Just draw a sphere of some given radius
def DrawSphere(radius):
    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluSphere(pObj, radius, 26, 13)
    gluDeleteQuadric(pObj)


#############################
# Render the torus and sphere
def DrawObjects():
    # Save the matrix state and do the rotations
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    # Translate the whole scene out and into view	
    glTranslatef(-0.75, 0.0, -2.5)	

    # Initialize the names stack
    glInitNames()
    glPushName(0)

    # Set material color, Yellow
    # torus
    glColor3f(1.0, 1.0, 0.0)
    glLoadName(TORUS)
    glPassThrough(TORUS)
    DrawTorus(40, 20)

    # Draw Sphere
    glColor3f(0.5, 0.0, 0.0)
    glTranslatef(1.5, 0.0, 0.0)
    glLoadName(SPHERE)
    glPassThrough(SPHERE)	
    DrawSphere(0.5)

    # Restore the matrix state
    glPopMatrix()	# Modelview matrix



#############################
# Go into feedback mode and draw a rectangle around the object
FEED_BUFF_SIZE = 32768
# Space for the feedback buffer
feedBackBuff = (GLfloat * FEED_BUFF_SIZE)()
def MakeSelection(nChoice):
    # Initial minimum and maximum values
    boundingRect['right'] = boundingRect['bottom'] = -999999.0
    boundingRect['left'] = boundingRect['top'] =  999999.0

    # Set the feedback buffer
    glFeedbackBuffer(FEED_BUFF_SIZE,GL_2D, feedBackBuff)

    # Enter feedback mode
    glRenderMode(GL_FEEDBACK)

    # Redraw the scene
    DrawObjects()

    # Leave feedback mode
    size = glRenderMode(GL_RENDER)

    # Parse the feedback buffer and get the
    # min and max X and Y window coordinates
    i = 0
    while(i < size):
        # Search for appropriate token
        if feedBackBuff[i] == GL_PASS_THROUGH_TOKEN:
            if feedBackBuff[i+1] == nChoice:
                i+= 2
                # Loop until next token is reached
                while i < size and feedBackBuff[i] != GL_PASS_THROUGH_TOKEN:
                    # Just get the polygons
                    if(feedBackBuff[i] == GL_POLYGON_TOKEN):
                        # Get all the values for this polygon
                        i += 1 # for the pre-increment op in the c++ code
                        count = int(feedBackBuff[i]) # How many vertices
                        i += 1

                        for j in range(0, count):   # Loop for each vertex

                            # Min and Max X
                            if(feedBackBuff[i] > boundingRect['right']):
                                boundingRect['right'] = feedBackBuff[i]

                            if(feedBackBuff[i] < boundingRect['left']):
                                boundingRect['left'] = feedBackBuff[i]
                            i += 1

                            # Min and Max Y
                            if(feedBackBuff[i] > boundingRect['bottom']):
                                boundingRect['bottom'] = feedBackBuff[i]

                            if(feedBackBuff[i] < boundingRect['top']):
                                boundingRect['top'] = feedBackBuff[i]
                            i += 1
                    else:
                        i += 1	# Get next index and keep looking
                break
        i += 1


#############################/
# Process the selection, which is triggered by a right mouse
# click at (xPos, yPos).

BUFFER_LENGTH = 64
# Space for selection buffer
selectBuff = (GLuint * BUFFER_LENGTH)()

def ProcessSelection(xPos, yPos):

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
    gluPerspective(60.0, fAspect, 1.0, 425.0)

    # Draw the scene
    DrawObjects()

    # Collect the hits
    hits = glRenderMode(GL_RENDER)

    # Restore the projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    # Go back to modelview for normal rendering
    glMatrixMode(GL_MODELVIEW)

    # If a single hit occurred, display the info.
    if(hits == 1):
        global selectedObject
        MakeSelection(selectBuff[3])
        if selectedObject == selectBuff[3]:
            selectedObject = 0
        else:
            selectedObject = selectBuff[3]



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
        #glEnable(GL_CULL_FACE)		# Do not calculate insides

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
        glLineWidth(2.0)

    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw the objects in the scene
        DrawObjects()

        # If something is selected, draw a bounding box around it
        if selectedObject != 0:

            viewport = (GLint * 4)()
            
            # Get the viewport
            glGetIntegerv(GL_VIEWPORT, viewport)

            # Remap the viewing volume to match window coordinates (approximately)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            
            # Establish clipping volume (left, right, bottom, top, near, far)
            glOrtho(viewport[0], viewport[2], viewport[3], viewport[1], -1, 1)
            glMatrixMode(GL_MODELVIEW)

            glDisable(GL_LIGHTING)
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_LINE_LOOP)

            (left, right, top, bottom) = map(GLint, map(int, [boundingRect['left'], boundingRect['right'], boundingRect['top'], boundingRect['bottom']]))
            glVertex2i(left, top)
            glVertex2i(left, bottom)
            glVertex2i(right, bottom)
            glVertex2i(right, top)

            glEnd()
            glEnable(GL_LIGHTING)

            glMatrixMode(GL_PROJECTION)
            glPopMatrix()

        glMatrixMode(GL_MODELVIEW)


    #############################/
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
        gluPerspective(60.0, fAspect, 1.0, 425.0)

        # Reset Model view matrix stack
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_press(self, x, y, button, mod):
        if button == mouse.LEFT:
            ProcessSelection(x, y)

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Select an Object', resizable=True)
    pyglet.app.run()
