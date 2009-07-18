# a python implementation of math3d.h & math3d.cpp from the OpenGL SuperBible
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on Frame.h
# Implementation of the GLFrame Class
# Richard S. Wright Jr.
# Code by Richard S. Wright Jr.

# The GLFrame (OrthonormalFrame) class. Possibly the most useful little piece of 3D graphics
# code for OpenGL immersive environments.
# Richard S. Wright Jr.
from pyglet.gl import glMultMatrixf, glTranslatef, gluLookAt
from math3d import M3DVector3f, M3DMatrix44f, m3dCrossProduct, m3dSetMatrixColumn44, m3dRotationMatrix44

class GLFrame(object):
    def __init__(self):
        # Default position and orientation.  At the origin, looking
        # down the positive Z axis (right handed coordinate system).

        # At origin
        self.vOrigin = M3DVector3f(0.0, 0.0, 0.0)    # Where am I?
        # Forward is -Z (default OpenGL)
        self.vForward = M3DVector3f(0.0, 0.0, -1.0) # Where am I going?
        # Up is -y in pyglet
        self.vUp = M3DVector3f(0.0, -1.0, 0.0)       # Which way is up?
        
    def setOrigin(self, x, y, z):
        self.vOrigin[0] = x
        
        self.vOrigin[1] = y
        
        self.vOrigin[2] = z

    # Get a 4x4 transformation matrix that describes the camera
    # orientation.
    def GetCameraOrientation(self):
        m = M3DMatrix44f()
        x = M3DVector3f()
        z = M3DVector3f()
        # Make rotation matrix
        # Z vector is reversed
        z[0] = -self.vForward[0]
        z[1] = -self.vForward[1]
        z[2] = -self.vForward[2]

        # X vector = Y cross Z 
        
        #BS I had to switch the order of the vectors for the example to work correctly.  I'm sure I'm doing something wrong, but I don't understand what.
        x = m3dCrossProduct(z, self.vUp)

        # Matrix has no translation information and is
        # transposed.... (rows instead of columns)
        m[0] = x[0]
        m[1] = x[1]
        m[2] = x[2]
        m[3] = 0.0

        m[4] = self.vUp[0]
        m[5] = self.vUp[1]
        m[6] = self.vUp[2]
        m[7] = 0.0

        m[8] = z[0]
        m[9] = z[1]
        m[10] = z[2]
        m[11] = 0.0

        m[12] = 0.0
        m[13] = 0.0
        m[14] = 0.0
        m[15] = 1.0

        return m
    
    # Perform viewing or modeling transformations
    # Position as the camera (for viewing). Apply this transformation
    # first as your viewing transformation
    # The default implementation of gluLookAt can be considerably sped up
    # since it uses doubles for everything... then again profile before you
    # tune... -) You might get a boost form page fault reduction too... if
    # no other glu routines are used...
    # This will get called once per frame.... go ahead and inline
    def ApplyCameraTransform(self, bRotOnly = False):

        m = self.GetCameraOrientation()
        
        # Camera Transform
        glMultMatrixf(m)
    
        # If Rotation only, then do not do the translation
        if not bRotOnly:
            glTranslatef(-self.vOrigin[0], -self.vOrigin[1], -self.vOrigin[2])

    # Just assemble the matrix
    def GetMatrix(self, bRotationOnly = False):
        matrix = M3DMatrix44f()
        
        # Calculate the right side (x) vector, drop it right into the matrix
        vXAxis = m3dCrossProduct(self.vUp, self.vForward)
        
        # m3dSetMatrixColum44 does not fill in the fourth value...
        # X Column
        m3dSetMatrixColumn44(matrix, vXAxis, 0)
        matrix[3] = 0.0

        # Y Column
        m3dSetMatrixColumn44(matrix, self.vUp, 1)
        matrix[7] = 0.0

        # Z Column
        m3dSetMatrixColumn44(matrix, self.vForward, 2)
        matrix[11] = 0.0

        # Translation (already done)
        if(bRotationOnly == True):
            matrix[12] = 0.0
            matrix[13] = 0.0
            matrix[14] = 0.0
        else:
            m3dSetMatrixColumn44(matrix, self.vOrigin, 3)

        matrix[15] = 1.0
        return matrix

    # Position as an object in the scene. This places and orients a
    # coordinate frame for other objects (besides the camera)
    # There is ample room for optimization here... 
    # This is going to be called alot... don't inline
    # Add flag to perform actor rotation only and not the translation
    def ApplyActorTransform(self, bRotationOnly = False):
        rotMat = self.GetMatrix(bRotationOnly)
        
        # Apply rotation to the current matrix
        glMultMatrixf(rotMat)
        
    # Move Forward (along Z axis)
    def MoveForward(self, fDelta):
        # Move along direction of front direction
        self.vOrigin[0] += self.vForward[0] * fDelta
        self.vOrigin[1] += self.vForward[1] * fDelta
        self.vOrigin[2] += self.vForward[2] * fDelta
        
    # Rotate around local Y
    def RotateLocalY(self, fAngle):
        # Just Rotate around the up vector
        # Create a rotation matrix around my Up (Y) vector
        rotMat = M3DMatrix44f()
        m3dRotationMatrix44(rotMat, fAngle, -self.vUp[0], -self.vUp[1], -self.vUp[2])

        newVect = M3DVector3f()
        
        # Rotate forward pointing vector (inlined 3x3 transform)
        newVect[0] = rotMat[0] * self.vForward[0] + rotMat[4] * self.vForward[1] + rotMat[8] *  self.vForward[2]
        newVect[1] = rotMat[1] * self.vForward[0] + rotMat[5] * self.vForward[1] + rotMat[9] *  self.vForward[2]
        newVect[2] = rotMat[2] * self.vForward[0] + rotMat[6] * self.vForward[1] + rotMat[10] * self.vForward[2]
        self.vForward[0] = newVect[0]
        self.vForward[1] = newVect[1]
        self.vForward[2] = newVect[2]
