from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

class Astro:
    def __init__(self, dist, esc, color, v_ang):
        self.deg = 0.0
        self.dist = dist
        self.esc = esc
        self.color = np.copy(color)
        self.v_ang = v_ang
        self.sphere = gluNewQuadric()
        self.moons = []
        
    def update(self):
        self.deg += self.v_ang
        if self.deg >= 360.0:
            self.deg = 0
    
    def draw(self):
        glPushMatrix()
        glColor3fv(self.color)
        glRotatef(self.deg, 0.0, 1.0, 0.0)
        glTranslatef(self.dist, 0.0, 0.0)
        glScalef(self.esc, self.esc, self.esc)
        glRotatef(-90, 1, 0, 0.0)
        gluSphere(self.sphere, 1.0, 16, 16)
        glRotatef(90, 1, 0, 0.0)

        for moon in self.moons:
            moon.draw()

        glPopMatrix()
        self.update()
        

    def addMoon(self, moon):
        self.moons.append(moon)