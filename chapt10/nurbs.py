#!/usr/bin/env python
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Nurbs.cpp
# OpenGL SuperBible
# Program by Richard S. Wright Jr.

import pyglet
from pyglet.gl import *
from pyglet import window

import sys
sys.path.append("../shared")

# NURBS object
global pNurb

# The number of control points for this curve
nNumPoints = 4 # 4 x 4

# Mesh extends four units -6 to +6 along x and y axis
# Lies in Z plane
#                 u  v  (x,y,z)	
ctrlPoints = (GLfloat * 3 * 4 * 4)(((-6.0, -6.0, 0.0),	# u = 0,	v = 0
                                     (-6.0, -2.0, 0.0),	#			v = 1
                                     (-6.0,  2.0, 0.0),	#			v = 2	
                                     (-6.0,  6.0, 0.0)), #			v = 3

                                    ((-2.0, -6.0, 0.0),	# u = 1	v = 0
                                     (-2.0, -2.0, 8.0),	#			v = 1
                                     (-2.0,  2.0, 8.0),	#			v = 2
                                     (-2.0,  6.0, 0.0)),	#			v = 3

                                    ((2.0, -6.0, 0.0 ), # u =2		v = 0
                                     (2.0, -2.0, 8.0 ), #			v = 1
                                     (2.0,  2.0, 8.0 ),	#			v = 2
                                     (2.0,  6.0, 0.0 )),#			v = 3

                                    ((6.0, -6.0, 0.0),	# u = 3	v = 0
                                     (6.0, -2.0, 0.0),	#			v = 1
                                     (6.0,  2.0, 0.0),	#			v = 2
                                     (6.0,  6.0, 0.0)))#			v = 3


# Knot sequence for the NURB
Knots = (GLfloat * 8)(0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0)

lightArrayType = GLfloat * 4

# Called to draw the control points in Red over the NURB
def DrawPoints():
    # Large Red Points
    glPointSize(5.0)
    glColor3ub(255,0,0)

    # Draw all the points in the array
    glBegin(GL_POINTS)
    for i in range(0, nNumPoints):
        for j in range(0, nNumPoints):
            glVertex3fv(ctrlPoints[i][j])
    glEnd()
    
class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        global pNurb
        
        whiteLight = lightArrayType(0.7, 0.7, 0.7, 1.0)
        specular = lightArrayType(0.7, 0.7, 0.7, 1.0)
        shine = GLfloat(100.0)
        
        # Clear Window to white
        glClearColor(1.0, 1.0, 1.0, 1.0 )

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Enable color tracking
        glEnable(GL_COLOR_MATERIAL)
        
        # Set Material properties to follow glColor values
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, shine)
        
        # Automatically generate normals for evaluated surfaces
        glEnable(GL_AUTO_NORMAL)

        # Setup the Nurbs object
        pNurb = gluNewNurbsRenderer()

        # Install error handler to notify user of NURBS errors
       # GLVoid (*callback)()
       # TODO: python equiv?
#        gluNurbsCallback(pNurb, GLU_ERROR, (CallBack)NurbsErrorHandler)  

        gluNurbsProperty(pNurb, GLU_SAMPLING_TOLERANCE, 25.0)
        # Uncomment the next line and comment the one following to produce a
        # wire frame mesh.
        #gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_OUTLINE_POLYGON)
        gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_FILL)


    # Called to draw scene
    def on_draw(self):
        # Draw in Blue
        glColor3ub(0,0,220)

        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Save the modelview matrix stack
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Rotate the mesh around to make it easier to see
        glRotatef(330.0, 1.0,0.0,0.0)
        
        # Render the NURB
        # Begin the NURB definition
        gluBeginCurve(pNurb)
        
        # Evaluate the surface
        gluNurbsSurface(pNurb,	# pointer to NURBS renderer
            8, Knots,			# No. of knots and knot array u direction	
            8, Knots,			# No. of knots and knot array v direction
            4 * 3,				# Distance between control points in u dir.
            3,					# Distance between control points in v dir.
            ctrlPoints[0][0], # Control points
            4, 4,					# u and v order of surface
            GL_MAP2_VERTEX_3)		# Type of surface
            
        # Done with surface
        gluEndSurface(pNurb);
        
        # Show the control points
        DrawPoints()

        # Restore the modelview matrix
        glPopMatrix()


    def on_resize(self, w, h):

        # Prevent a divide by zero
        if h == 0:
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Perspective view
        gluPerspective (45.0, float(w)/float(h), 1.0, 40.0)

        # Modelview matrix reset
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Viewing transformation, position for better view
        glTranslatef (0.0, 0.0, -20.0)

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='NURBS Surface', resizable=True)
    pyglet.app.run()
