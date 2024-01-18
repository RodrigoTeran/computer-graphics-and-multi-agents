#Autor: Ivan Olmos Pineda
#Curso: Multiagentes - Graficas Computacionales

import pygame
import random
import math
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Cubo import Cubo

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
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
#Dimension del plano
DimBoard = 200

pygame.init()

#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 50

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
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for i in range(ncubos):
        cubos.append(Cubo(DimBoard, 1.0, random.random() * 2 + 1))

def detect_colisiones():
    for i in range(len(cubos)):
        for j in range(i + 1, len(cubos)):
            cube_1 = cubos[i]
            cube_2 = cubos[j]

            cx_cube_1 = cube_1.Position[0] + cube_1.Direction[0]
            cy_cube_1 = cube_1.Position[1] + cube_1.Direction[1]
            cz_cube_1 = cube_1.Position[2] + cube_1.Direction[2]

            cx_cube_2 = cube_2.Position[0] + cube_2.Direction[0]
            cy_cube_2 = cube_2.Position[1] + cube_2.Direction[1]
            cz_cube_2 = cube_2.Position[2] + cube_2.Direction[2]

            de = math.sqrt(
                    math.pow((cx_cube_1 - cx_cube_2), 2) +
                    math.pow((cy_cube_1 - cy_cube_2), 2) +
                    math.pow((cz_cube_1 - cz_cube_2), 2)
                ) - 5
            r_cube_1 = cube_1.radius
            r_cube_2 = cube_2.radius
            r_sum = r_cube_1 + r_cube_2

            if de <= r_sum:
                # Colision
                cube_1.stop()
                cube_2.stop()
                break # ya no hay que checar con los demás

def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    #Se dibuja cubos
    for obj in cubos:
        obj.draw()
        obj.update()
    
done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    display()
    detect_colisiones()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()