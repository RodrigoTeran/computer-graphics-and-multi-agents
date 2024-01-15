import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

import sys
sys.path.append('..')
from Astro import Astro

Astros = []

pygame.init()

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=500.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
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

planets = [
    # Implementar un primer planeta que gire alrededor del sol
    # - de color blanco
    # - con una velocidad angular de 1
    # - sin lunas
    {
        "dist": 3.0,
        "size": 0.5,
        "color": [255 / 255, 255 / 255, 255 / 255],
        "v_ang": 1,
        "moons": []
    },
    # Implementar un segundo planeta que gire alrededor del sol
    # - con un diámetro ligeramente superior al primer planeta
    # - con un color verde
    # - que tenga una velocidad angular ligeramente mayor al primer planeta.
    {
        "dist": 5.0,
        "size": 0.6,
        "color": [0 / 255, 255 / 255, 0 / 255],
        "v_ang": 1.1,
        # Implementar dos lunas alrededor de este planeta
        # - cada luna debe ser de menor tamaño al planeta de referencia
        # - cada luna con una velocidad de rotación diferente
        "moons": [
            {
                "dist": 1.4,
                "size": 0.25,
                "color": [223 / 255, 67 / 255, 132 / 255],
                "v_ang": 1.4,
            },
            {
                "dist": 1.6,
                "size": 0.15,
                "color": [67 / 255, 223 / 255, 223 / 255],
                "v_ang": 0.9,
            },
        ]
    },
    # Implementar un tercer planeta
    # - el más alejado del sol
    # - con el mayor diámetro
    # - el color será a elección del alumno
    # - este planeta es el que debe girar más rápido alrededor del sol
    {
        "dist": 7.0,
        "size": 1.25,
        "color": [157 / 255, 115 / 255, 247 / 255],
        "v_ang": 1.5,
        # Además, deberá de tener cuatro lunas
        # - con velocidades angulares diferentes entre todas
        # - las lunas deben de tener un tamaño menor que el planeta anfitrión.
        "moons": [
            {
                "dist": 1.3,
                "size": 0.12,
                "color": [115 / 255, 247 / 255, 168 / 255],
                "v_ang": 0.9,
            },
            {
                "dist": 1.2,
                "size": 0.15,
                "color": [212 / 255, 247 / 255, 115 / 255],
                "v_ang": 1.9,
            },
            {
                "dist": 1.9,
                "size": 0.2,
                "color": [250 / 255, 146 / 255, 196 / 255],
                "v_ang": 0.5,
            },
            {
                "dist": 1.7,
                "size": 0.17,
                "color": [165 / 255, 255 / 255, 179 / 255],
                "v_ang": 1.2,
            },
        ]
    }
]

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

    # Se generan todos los astros
    for planet in planets:
        new_planet = Astro(planet.get("dist", None), planet.get("size", None), planet.get("color", None), planet.get("v_ang", None))
        Astros.append(new_planet)
        for moon in planet.get("moons", None):
            new_moon = Astro(moon.get("dist", None), moon.get("size", None), moon.get("color", None), moon.get("v_ang", None))
            new_planet.addMoon(new_moon)
  
sphere = gluNewQuadric()

deg_sun = 0.0

def Sun():
    global deg_sun
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glScalef(2.0, 2.0, 2.0)
    glRotatef(deg_sun, 0.0, 0.0, 1.0)
    gluSphere(sphere, 1.0, 16, 16)
    deg_sun += 1.0
    if deg_sun >= 360.0:
        deg_sun = 0.0
    glPopMatrix()
   
   
Init()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glShadeModel(GL_FLAT)    
    Axis()
    Sun()
    
    for obj in Astros:
        obj.draw()
        obj.update()
    
    pygame.display.flip()
    pygame.time.wait(20)

pygame.quit()