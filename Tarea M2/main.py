import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
sys.path.append("..")

# Piramide y Op3D
from OpMat import OpMat
from Piramide import Piramide

op3D = OpMat()
objeto1 = Piramide(op3D)

pygame.init()

screen_width = 900
screen_height = 600

FOVY=60.0
ZNEAR=0.01
ZFAR=500.0

EYE_X=10.0
EYE_Y=10.0
EYE_Z=10.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
    (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: ejes 3D")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

Init()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    op3D.loadIdentity()

    # Incisio 1
    # 1: rotación libre con theta = 15 grados y eje de rotación = (0.5, 0.5, 0.0);
    # 2: traslación = (3.0, - 5.0, 1.0);
    # 3: escalado = (1.5, 1.0, 1.5)
    # op3D.rotate(15, 0.5, 0.5, 0.0)
    # op3D.translate(3.0, - 5.0, 1.0)
    # op3D.scale(1.5, 1.0, 1.5)

    # Incisio 2
    # 1: escalado = (1.5, 1.0, 1.5);
    # 2: rotación libre con theta = 15 grados y eje de rotación = (0.5, 0.5, 0.0);
    # 3: traslación = (3.0, - 5.0, 1.0)
    op3D.scale(1.5, 1.0, 1.5)
    op3D.rotate(15, 0.5, 0.5, 0.0)
    op3D.translate(3.0, - 5.0, 1.0)

    objeto1.render()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()