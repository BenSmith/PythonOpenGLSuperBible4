#!/usr/bin/env python
# Demonstrates OpenGL evaluators to draw bezier curve
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Bezier.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
from random import randint

import sys
sys.path.append("../shared")

# The number of control points for this curve
nNumPoints = 4

ctrlPoints = (GLfloat * 3 * 4)(   (-4.0, 0.0, 0.0),	# End Point
                                            (-6.0, 4.0, 0.0),	# Control Point
                                            (6.0, -4.0, 0.0),	# Control Point
                                            (4.0, 0.0, 0.0)) 	# End Point

# This function is used to superimpose the control points over the curve
def DrawPoints():
    # Set point size larger to make more visible
    glPointSize(5.0)

    # Loop through all control points for this example
    glBegin(GL_POINTS)
    for i in range(0, nNumPoints):
       glVertex2fv(ctrlPoints[i])
    glEnd()


class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        # Draw in Blue
        glColor3f(0.0, 0.0, 1.0)	


    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Sets up the bezier
        # This actually only needs to be called once and could go in
        # the setup function
        glMap1f(GL_MAP1_VERTEX_3,  # Type of data generated
        0.0,                                    # Lower u range
        100.0,                                 # Upper u range
        3,                                       # Distance between points in the data
        nNumPoints,                         # number of control points
        ctrlPoints[0])                  # array of control points

        # Enable the evaluator
        glEnable(GL_MAP1_VERTEX_3)

        # Use a line strip to "connect-the-dots"
        glBegin(GL_LINE_STRIP)
        
        for i in range (0, 101):
            # Evaluate the curve at this point
            glEvalCoord1f(i) 
        glEnd()

        # Use higher level functions to map to a grid, then evaluate the
        # entire thing.
        # Put these two functions in to replace above loop

        # Map a grid of 100 points from 0 to 100
        #glMapGrid1d(100,0.0,100.0)

        # Evaluate the grid, using lines
        #glEvalMesh1(GL_LINE,0,100)

        # Draw the Control Points
        DrawPoints()

    ###################/
    # Set 2D Projection negative 10 to positive 10 in X and Y
    # Called when the window has changed size (including when the window is created)
    def on_resize(self, w, h):

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='2D Bezier Curve', resizable=True)
    pyglet.app.run()
