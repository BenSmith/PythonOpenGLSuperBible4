#!/usr/bin/env python
# simple.py
# The Simplest OpenGL program with pyglet
# Ben Smith
# benjamin.coder.smith@gmail.com
#
# Based heavily on: Simple.cpp
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

import pyglet
from pyglet.gl import *
from pyglet import window

class MainWindow(window.Window):
    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        
        # Setup the rendering state
        glClearColor(0, 0, 1, 1)

    # Called to draw scene
    def on_draw(self):
        # Clear the window with the current clearing color
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Flush drawing commands
        glFlush()

# Main program entry point
if __name__ == '__main__':
    w = MainWindow(caption='Simple', resizable=True)

    pyglet.app.run()
