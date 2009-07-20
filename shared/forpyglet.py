
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

def gltDrawSphere(a, b, c):
    glutSolidSphere(a, b, c)
    
# Draw a 3D unit Axis set
# Draw the unit axis. A small white sphere represents the origin
# and the three axes are colored Red, Green, and Blue, which 
# corresponds to positive X, Y, and Z respectively. Each axis has
# an arrow on the end, and normals are provided should the axes
# be lit. These are all built using the quadric shapes. For best
# results, put this in a display list.
def gltDrawUnitAxes():
    # Measurements
    fAxisRadius = 0.025
    fAxisHeight = 1.0
    fArrowRadius = 0.06
    fArrowHeight = 0.1

    # Setup the quadric object
    pObj = gluNewQuadric()
    gluQuadricDrawStyle(pObj, GLU_FILL)
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluQuadricOrientation(pObj, GLU_OUTSIDE)
    gluQuadricTexture(pObj, GLU_FALSE)

    ###########################/
    # Draw the blue Z axis first, with arrowed head
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()

    ###########################/
    # Draw the Red X axis 2nd, with arrowed head
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glRotatef(90.0, 0.0, 1.0, 0.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()
    glPopMatrix()

    ###########################/
    # Draw the Green Y axis 3rd, with arrowed head
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()
    glPopMatrix()

    ############################
    # White Sphere at origin
    glColor3f(1.0, 1.0, 1.0)
    gluSphere(pObj, 0.05, 15, 15)

    # Delete the quadric
    gluDeleteQuadric(pObj)
