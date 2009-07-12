
from pyglet.gl import *
from math import sin, cos
from math3d import M3DVector3f, M3D_PI, m3dNormalizeVector

def glutSolidSphere(radius, slices, stacks):
    sphere = gluNewQuadric()
    gluQuadricTexture(sphere, True)
    gluSphere(sphere, radius, slices, stacks)
    gluDeleteQuadric(sphere)
    
# For best results, put this in a display list
# Draw a torus (doughnut)  at z = fZVal... torus is in xy plane
def gltDrawTorus(majorRadius, minorRadius, numMajor, numMinor):
    vNormal = M3DVector3f()
    majorStep = 2.0*M3D_PI / numMajor
    minorStep = 2.0*M3D_PI / numMinor

    i = j = 0
    while i < numMajor:
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)
        
        glBegin(GL_TRIANGLE_STRIP)
        j = 0
        while j <= numMinor:
            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)
            
            # First point
            glTexCoord2f(float(i)/float(numMajor), float(j)/float(numMinor))
            vNormal[0] = x0*c
            vNormal[1] = y0*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(vNormal)
            glVertex3f(x0*r, y0*r, z)
            
            glTexCoord2f(float(i+1)/float(numMajor), float(j)/float(numMinor))
            vNormal[0] = x1*c
            vNormal[1] = y1*c
            vNormal[2] = z/minorRadius
            m3dNormalizeVector(vNormal)
            glNormal3fv(vNormal)
            glVertex3f(x1*r, y1*r, z)
            
            j += 1
            
        glEnd()
        i += 1
