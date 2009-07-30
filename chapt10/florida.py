#!/usr/bin/env python
# Demonstrates polygon tesselation
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based on Florida.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet.gl.glu import _GLUfuncptr
from pyglet.gl.lib import link_GLU as _link_function
from pyglet import window
from pyglet.window import key
from random import randint
import ctypes

functype = ctypes.CFUNCTYPE
import sys
if sys.platform == 'win32':
    functype = ctypes.WINFUNCTYPE

COAST_POINTS = 24
vCoast = (GLdouble * 3 * COAST_POINTS)((-70.0, 30.0, 0.0 ),
                                    (-50.0, 30.0, 0.0 ),
                                    (-50.0, 27.0, 0.0 ),
                                    ( -5.0, 27.0, 0.0 ),
                                    (  0.0, 20.0, 0.0 ),
                                    (  8.0, 10.0, 0.0 ),
                                    ( 12.0,  5.0, 0.0 ),
                                    ( 10.0,  0.0, 0.0 ),
                                    ( 15.0,-10.0, 0.0 ),
                                    ( 20.0,-20.0, 0.0 ),
                                    ( 20.0,-35.0, 0.0 ),
                                    ( 10.0,-40.0, 0.0 ),
                                    (  0.0,-30.0, 0.0 ),
                                    ( -5.0,-20.0, 0.0 ),
                                    (-12.0,-10.0, 0.0 ),
                                    (-13.0, -5.0, 0.0 ),
                                    (-12.0,  5.0, 0.0 ),
                                    (-20.0, 10.0, 0.0 ),
                                    (-30.0, 20.0, 0.0 ),
                                    (-40.0, 15.0, 0.0 ),
                                    (-50.0, 15.0, 0.0 ),
                                    (-55.0, 20.0, 0.0 ),
                                    (-60.0, 25.0, 0.0 ),
                                    (-70.0, 25.0, 0.0 ))

# Lake Okeechobee
LAKE_POINTS = 4
vLake = (GLdouble * 3 * LAKE_POINTS)(( 10.0, -20.0, 0.0 ),
                                                    ( 15.0, -25.0, 0.0 ),
                                                    ( 10.0, -30.0, 0.0 ),
                                                    (  5.0, -25.0, 0.0 ))

# Which Drawing Method
DRAW_LOOPS = 0
DRAW_CONCAVE = 1
DRAW_COMPLEX = 2
iMethod = DRAW_LOOPS   # Default, draw line loops

glBeginFuncType = functype(None, GLenum)
glEndFuncType = functype(None)
glVertex3dvFuncType = functype(None, POINTER(GLdouble))
glTessErrorFuncType = functype(None, GLenum)

glBeginFunc = glBeginFuncType(glBegin)
glEndFunc = glEndFuncType(glEnd)
glVertex3dvFunc = glVertex3dvFuncType(glVertex3dv)

def py_tessError(error):
    print gluErrorString(error)

tessError = glTessErrorFuncType(py_tessError)

begin = ctypes.cast(glBeginFunc, CFUNCTYPE(None))
end = ctypes.cast(glEndFunc, CFUNCTYPE(None))
vertex = ctypes.cast(glVertex3dvFunc, CFUNCTYPE(None))
tessError = ctypes.cast(tessError, CFUNCTYPE(None))

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Blue background
        glClearColor(1.0, 1.0, 1.0, 1.0 )
        
        # Fat smooth lines to make it look nicer
        glLineWidth(2.0)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Clear the window
        glClear(GL_COLOR_BUFFER_BIT)
            
        if iMethod ==  DRAW_LOOPS:                    # Draw line loops
            
            glColor3f(0.0, 0.0, 0.0)    # Just black outline
            
            # Line loop with coastline shape
            glBegin(GL_LINE_LOOP)
            for i in range(0, COAST_POINTS):
                glVertex3dv(vCoast[i])
            glEnd()

            # Line loop with shape of interior lake
            glBegin(GL_LINE_LOOP)
            for i in range(0, LAKE_POINTS):
                glVertex3dv(vLake[i])
            glEnd()
            
        elif iMethod ==  DRAW_CONCAVE:              # Tesselate concave polygon
            
            # Green polygon
            glColor3f(0.0, 1.0, 0.0) 
            
            # Create the tesselator object
            pTess = gluNewTess()
            
            # Set callback functions
            # Just call glBegin at begining of triangle batch
            gluTessCallback(pTess, GLU_TESS_BEGIN, begin) 
            
            # Just call glEnd at end of triangle batch
            gluTessCallback(pTess, GLU_TESS_END, end)
            
            # Just call glVertex3dv for each  vertex
            gluTessCallback(pTess, GLU_TESS_VERTEX, vertex)
            
            # Register error callback
            gluTessCallback(pTess, GLU_TESS_ERROR, tessError)
            
            # Begin the polygon
            gluTessBeginPolygon(pTess, None)
            
            # Gegin the one and only contour
            gluTessBeginContour(pTess)

            # Feed in the list of vertices
            for i in range(0, COAST_POINTS):
                gluTessVertex(pTess, vCoast[i], vCoast[i]) # Can't be NULL
                
            # Close contour and polygon
            gluTessEndContour(pTess)
            gluTessEndPolygon(pTess)
            
            # All done with tesselator object
            gluDeleteTess(pTess)
            
            pTess = None
    
        elif iMethod == DRAW_COMPLEX:          # Tesselate, but with hole cut out
            
            # Green polygon
            glColor3f(0.0, 1.0, 0.0) 

             # Create the tesselator object
            pTess = gluNewTess()
            
            # Set callback functions
            # Just call glBegin at begining of triangle batch
            gluTessCallback(pTess, GLU_TESS_BEGIN, begin)
            
            # Just call glEnd at end of triangle batch
            gluTessCallback(pTess, GLU_TESS_END, end)
            
            # Just call glVertex3dv for each  vertex
            gluTessCallback(pTess, GLU_TESS_VERTEX, vertex)
            
            # Register error callback
            gluTessCallback(pTess, GLU_TESS_ERROR, tessError)

            # How to count filled and open areas
            gluTessProperty(pTess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
            
            # Begin the polygon
            gluTessBeginPolygon(pTess, None) # No user data
            
            # First contour, outline of state
            gluTessBeginContour(pTess)
            for i in range(0, COAST_POINTS):
                gluTessVertex(pTess, vCoast[i], vCoast[i])
            gluTessEndContour(pTess)
            
            # Second contour, outline of lake
            gluTessBeginContour(pTess)
            for i in range(0, LAKE_POINTS):
                gluTessVertex(pTess, vLake[i], vLake[i])
            gluTessEndContour(pTess)
            
            # All done with polygon
            gluTessEndPolygon(pTess)
            
            # No longer need tessellator object
            gluDeleteTess(pTess)


    ###################/
    # Reset projection
    def on_resize(self, w, h):
        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        
        # Reset projection matrix stack
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(-80, 35, -50, 50)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_key_press(self, symbol, modifier):
        global iMethod
        if symbol == key._1:
            iMethod = 0
        elif symbol == key._2:
            iMethod = 1
        elif symbol == key._3:
            iMethod = 2
        print iMethod

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Tesselated Florida', resizable=True)
    pyglet.app.run()
