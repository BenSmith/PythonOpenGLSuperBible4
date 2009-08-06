#!/usr/bin/env python

# Some Python implementations of glut functions.  
# Based either on OpenGL SuperBible code or MesaGL
# Ben Smith
# benjamin.coder.smith@gmail.com

from pyglet.gl import *
from math import cos, sin, sqrt, pi as M_PI

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
    size = float(size)
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

def doughnut(r, R, nsides, rings):
    ringDelta = 2.0 * M_PI / float(rings)
    sideDelta = 2.0 * M_PI / float(nsides)

    theta = 0.0
    cosTheta = 1.0
    sinTheta = 0.0

    for i in range(rings - 1, -1, -1):
        theta1 = theta + ringDelta
        cosTheta1 = cos(theta1)
        sinTheta1 = sin(theta1)
        glBegin(GL_QUAD_STRIP)
        phi = 0.0
        for j in range(nsides, -1, -1):

            phi += sideDelta
            cosPhi = cos(phi)
            sinPhi = sin(phi)
            dist = R + r * cosPhi

            glNormal3f(cosTheta1 * cosPhi, -sinTheta1 * cosPhi, sinPhi)
            glVertex3f(cosTheta1 * dist, -sinTheta1 * dist, r * sinPhi)
            glNormal3f(cosTheta * cosPhi, -sinTheta * cosPhi, sinPhi)
            glVertex3f(cosTheta * dist, -sinTheta * dist,  r * sinPhi)

        glEnd()
        theta = theta1
        cosTheta = cosTheta1
        sinTheta = sinTheta1
    

def glutWireTorus(innerRadius, outerRadius, nsides, rings):
    glPushAttrib(GL_POLYGON_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    doughnut(innerRadius, outerRadius, nsides, rings)
    glPopAttrib()

def glutSolidTorus(innerRadius, outerRadius, nsides, rings):
    doughnut(innerRadius, outerRadius, nsides, rings)

def DIFF3(v1, v2, result):
    result[0] = v1[0] - v2[0]
    result[1] = v1[1] - v2[1]
    result[2] = v1[2] - v2[2]
    
def crossprod(v1, v2, prod):
    p = (GLfloat * 3)()
    p[0] = v1[1] * v2[2] - v2[1] * v1[2]
    p[1] = v1[2] * v2[0] - v2[2] * v1[0]
    p[2] = v1[0] * v2[1] - v2[0] * v1[1]
    prod[0] = p[0]
    prod[1] = p[1]
    prod[2] = p[2]
    
def normalize(v):
    d = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    
    if d == 0.0:
        raise(Exception("normalize: zero length vector"))
    d = 1.0 / d
    v[0] *= d
    v[1] *= d
    v[2] *= d


def recorditem(n1, n2, n3, shadeType):
    q0 = (GLfloat * 3)()
    q1 = (GLfloat * 3)()
    
    DIFF3(n1, n2, q0)
    DIFF3(n2, n3, q1)
    crossprod(q0, q1, q1)
    normalize(q1)
    
    glBegin(shadeType)
    glNormal3fv(q1)
    glVertex3fv(n1)
    glVertex3fv(n2)
    glVertex3fv(n3)
    glEnd()
    
def subdivide(v0, v1, v2, shadeType):
    w0 = (GLfloat * 3)()
    w1 = (GLfloat * 3)()
    w2 = (GLfloat * 3)()
    
    depth = 1
    for i in range(depth):
        ii = float(i)
        j = 0
        while i + j < depth:
            jj = float(j)
            k = depth - i - j
            kk = float(k)
            fdepth = float(depth)
            for n in range(3):
                w0[n] = (ii * v0[n] + jj * v1[n] + k * v2[n]) / fdepth
                w1[n] = ((ii + 1.0) * v0[n] + jj * v1[n] + (kk - 1.0) * v2[n]) / fdepth
                w2[n] = (ii * v0[n] + (jj + 1) * v1[n] + (kk - 1.0) * v2[n]) / fdepth

            l = sqrt(w0[0] * w0[0] + w0[1] * w0[1] + w0[2] * w0[2])
            w0[0] /= l
            w0[1] /= l
            w0[2] /= l
            l = sqrt(w1[0] * w1[0] + w1[1] * w1[1] + w1[2] * w1[2])
            w1[0] /= l
            w1[1] /= l
            w1[2] /= l
            l = sqrt(w2[0] * w2[0] + w2[1] * w2[1] + w2[2] * w2[2])
            w2[0] /= l
            w2[1] /= l
            w2[2] /= l
            recorditem(w1, w0, w2, shadeType)
            j += 1

def drawtriangle(i, data, ndx, shadeType):
    x0 = data[ndx[i][0]]
    x1 = data[ndx[i][1]]
    x2 = data[ndx[i][2]]
    subdivide(x0, x1, x2, shadeType)

# octahedron data: The octahedron produced is centered at the
#   origin and has radius 1.0
odata = ((GLfloat * 3) * 6)(
  (1.0, 0.0, 0.0),
  (-1.0, 0.0, 0.0),
  (0.0, 1.0, 0.0),
  (0.0, -1.0, 0.0),
  (0.0, 0.0, 1.0),
  (0.0, 0.0, -1.0)
)


ondex = ((GLint * 3) * 8)(
  (0, 4, 2),
  (1, 2, 4),
  (0, 3, 4),
  (1, 4, 3),
  (0, 2, 5),
  (1, 5, 2),
  (0, 5, 3),
  (1, 3, 5)
)

def octahedron(shadeType):
    for i in range(7, -1, -1):
        drawtriangle(i, odata, ondex, shadeType)

def glutWireOctahedron():
    octahedron(GL_LINE_LOOP)

def glutSolidOctahedron():
    octahedron(GL_TRIANGLES)
    