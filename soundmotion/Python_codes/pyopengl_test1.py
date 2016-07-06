#Listing 1. Opening a Window, Setting up Lighting and Drawing a Teapot with GLUT

from OpenGL.GL import *
from OpenGL.GLUT import *

def init():
   glClearColor(0, 0, 0, 0)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glLightfv(GL_LIGHT0, GL_AMBIENT,
   [0.0, 0.0, 0.0, 1.0])
   glLightfv(GL_LIGHT0, GL_DIFFUSE,
   [1.0, 1.0, 1.0, 1.0])
   glLightfv(GL_LIGHT0, GL_POSITION,
   [0.0, 3.0, 3.0, 0.0])
   glLightModelfv(GL_LIGHT_MODEL_AMBIENT,
   [0.2, 0.2, 0.2, 1.0])
   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)

def display():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glMaterialfv(GL_FRONT, GL_AMBIENT,
   [0.1745, 0.0, 0.1, 0.0])
   glMaterialfv(GL_FRONT, GL_DIFFUSE,
   [0.1, 0.0, 0.6, 0.0])
   glMaterialfv(GL_FRONT, GL_SPECULAR,
   [0.7, 0.6, 0.8, 0.0])
   glMaterialf(GL_FRONT, GL_SHININESS, 80)
   glutSolidTeapot(0.5)
   glFlush()

glutInit('')
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutCreateWindow('Hello GLUT')
glutSetDisplayFuncCallback(display)
glutDisplayFunc()
init()
glutMainLoop()
