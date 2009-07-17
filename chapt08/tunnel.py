#!/usr/bin/env python
# Demonstrates mipmapping and using texture objects
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Tunnel.cpp
# OpenGL SuperBible
# Richard S. Wright Jr.

import pyglet
import math
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

zPos = -60.0

# Texture Objects
TEXTURE_BRICK   = 0
TEXTURE_FLOOR   = 1
TEXTURE_CEILING = 2
TEXTURE_COUNT   = 3

textures = (GLuint * TEXTURE_COUNT)()

szTextureFiles = ['brick.jpg', 'floor.jpg', 'ceiling.jpg']

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)

        # Black Background
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # Textures applied as decals, no lighting or coloring effects
        glEnable(GL_TEXTURE_2D)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        # Load textures
        glGenTextures(TEXTURE_COUNT, textures)
        for iLoop in range (0, TEXTURE_COUNT):
            # Bind to next texture object
            glBindTexture(GL_TEXTURE_2D, textures[iLoop])
            
            # Load texture, set filter and wrap modes
            img = pyglet.image.load(szTextureFiles[iLoop])
            
            # Load texture, set filter and wrap modes
            gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.width, img.height, GL_RGB, GL_UNSIGNED_BYTE, img.get_data('RGB', img.pitch))
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
        
    # Shutdown the rendering context. Just deletes the
    # texture objects
    def __del__(self):
        glDeleteTextures(TEXTURE_COUNT, textures)
        
        
    # Called to draw scene
    def on_draw(self):
        # Clear the window with current clearing color
        glClear(GL_COLOR_BUFFER_BIT)

        # Save the matrix state and do the rotations
        glPushMatrix()
        # Move object back and do in place rotation
        glTranslatef(0.0, 0.0, zPos)

        # Floor
        z = 60.0 
        while z >= -1.0:
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_FLOOR])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, -10.0, z - 10.0)
                
            glEnd()

            # Ceiling
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_CEILING])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, 10.0, z)
                
            glEnd()

            
            # Left Wall
            glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_BRICK])
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10.0, -10.0, z)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(-10.0, -10.0, z - 10.0)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(-10.0, 10.0, z - 10.0)

            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10.0, 10.0, z)
                
            glEnd()


            # Right Wall
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 1.0)
            glVertex3f(10.0, 10.0, z)

            glTexCoord2f(1.0, 1.0)
            glVertex3f(10.0, 10.0, z - 10.0)

            glTexCoord2f(1.0, 0.0)
            glVertex3f(10.0, -10.0, z - 10.0)

            glTexCoord2f(0.0, 0.0)
            glVertex3f(10.0, -10.0, z)
                
            glEnd()
            z -= 10.0
        glPopMatrix()
        
    def on_key_press(self, symbol, modifier):
        global zPos
        if symbol == key.UP:
            zPos += 1.0
        elif symbol == key.DOWN:
            zPos -= 1.0

    def on_resize(self, w, h):
        # Prevent a divide by zero
        if(h == 0):
            h = 1

        # Set Viewport to window dimensions
        glViewport(0, 0, w, h)
        fAspect = float(w)/float(h)

        # Reset coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Produce the perspective projection
        gluPerspective(90.0, fAspect, 1.0, 120.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(800, 600, caption='Tunnel', resizable=True)
    pyglet.app.run()
