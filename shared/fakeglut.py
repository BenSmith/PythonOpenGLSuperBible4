#!/usr/bin/env python

# Some Python implementations of glut functions.  
# Based either on OpenGL SuperBible code or MesaGL
# Ben Smith
# benjamin.coder.smith@gmail.com

from pyglet.gl import *

# translated from mesagl's glut library.
def drawBox(size, type):
    n = ((GLfloat * 3) * 6)((-1.0, 0.0, 0.0),
                            (0.0, 1.0, 0.0),
                            (1.0, 0.0, 0.0),
                            (0.0, -1.0, 0.0),
                            (0.0, 0.0, 1.0),
                            (0.0, 0.0, -1.0))
    
    faces = ((GLint * 4) * 6)((0, 1, 2, 3),
                                (3, 2, 6, 7),
                                (7, 6, 5, 4),
                                (4, 5, 1, 0),
                                (5, 6, 2, 1),
                                (7, 4, 0, 3))
    v = ((GLfloat * 3) * 8)()
    v[0][0] = v[1][0] = v[2][0] = v[3][0] = -size / 2.0
    v[4][0] = v[5][0] = v[6][0] = v[7][0] = size / 2.0
    v[0][1] = v[1][1] = v[4][1] = v[5][1] = -size / 2.0
    v[2][1] = v[3][1] = v[6][1] = v[7][1] = size / 2.0
    v[0][2] = v[3][2] = v[4][2] = v[7][2] = -size / 2.0
    v[1][2] = v[2][2] = v[5][2] = v[6][2] = size / 2.0

    for i in range(5):
        glBegin(type)
        glNormal3fv(n[i])
        glVertex3fv(v[faces[i][0]])
        glVertex3fv(v[faces[i][1]])
        glVertex3fv(v[faces[i][2]])
        glVertex3fv(v[faces[i][3]])
        glEnd()
    
def glutWireCube(size):
    drawBox(float(size), GL_LINE_LOOP)
    
def glutSolidCube(size):
    drawBox(float(size), GL_QUADS)

# translated from mesa's glut lib
def glutSolidCone(base, height, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, base, 0.0, height, slices, stacks)

def glutSolidSphere(radius, slices, stacks):
    sphere = gluNewQuadric()
    gluQuadricTexture(sphere, True)
    gluSphere(sphere, radius, slices, stacks)
    gluDeleteQuadric(sphere)

def glutSolidOctahedron():
    pass
    