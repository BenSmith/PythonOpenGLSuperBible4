#!/usr/bin/env python

# a python implementation of math3d.h & math3d.cpp from the OpenGL SuperBible

# Math3d.h
# Header file for the Math3d library. The C-Runtime has math.h, this file and the
# accompanying math.c are meant to suppliment math.h by adding geometry/math routines
# useful for graphics, simulation, and physics applications (3D stuff).
# Richard S. Wright Jr.
from pyglet.gl import *
from math import sin, cos

M3D_PI = 3.14159265358979323846
M3D_PI_DIV_180 = M3D_PI / 180.0

M3DVector3f = GLfloat * 3 # Vector of three floats (x, y, z)
M3DMatrix44f = GLfloat * 16 # A 4 X 4 matrix, column major (floats) - OpenGL style

def m3dTransformVector3(vOut, v, m):
    vOut[0] = m[0] * v[0] + m[4] * v[1] + m[8] *  v[2] + m[12]
    vOut[1] = m[1] * v[0] + m[5] * v[1] + m[9] *  v[2] + m[13]
    vOut[2] = m[2] * v[0] + m[6] * v[1] + m[10] * v[2] + m[14]

def m3dLoadIdentity44(m):
    m[0] = m[5] = m[10] = m[15] = 1.0
    m[1] = m[2] = m[3] = m[4] = 0.0
    m[6] = m[7] = m[8] = m[9] = 0.0
    m[11] = m[12] = m[13] = m[14] = 0.0
    

# Creates a 4x4 rotation matrix, takes radians NOT degrees
def m3dRotationMatrix44(m, angle, x, y, z):
    s = sin(angle)
    c = cos(angle)
    mag = float((x * x + y * y + z * z) ** 0.5)
    
    if mag == 0.0:
        m3dLoadIdentity(m)
        return
    
    x /= mag
    y /= mag
    z /= mag
    
    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    zx = z * x
    xs = x * s
    ys = y * s
    zs = z * s
    one_c = 1.0 - c
    
    m[0] = (one_c * xx) + c
    m[1] = (one_c * xy) - zs
    m[2] = (one_c * zx) + ys
    m[3] = 0.0
    
    m[4] = (one_c * xy) + zs
    m[5] = (one_c * yy) + c
    m[6] = (one_c * yz) - xs
    m[7] = 0.0
    
    m[8] = (one_c * zx) - ys
    m[9] = (one_c * yz) + xs
    m[10] = (one_c * zz) + c
    m[11]  = 0.0
    
    m[12] = 0.0
    m[13] = 0.0
    m[14] = 0.0
    m[15] = 1.0

def m3dDegToRad(num):
    return (num * M3D_PI_DIV_180)
