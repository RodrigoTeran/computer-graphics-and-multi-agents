from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

class Piramide:
    def __init__(self, op):
        self.op3D = op
        self.points = np.array([[1.0,0.0,1.0,1.0], [1.0,0.0,-1.0,1.0], [-1.0,0.0,-1.0,1.0], [-1.0,0.0,1.0,1.0], [0.0,3.0,0.0,1.0]])
    
    def render(self):
        pointsR = self.points.copy()
        self.op3D.mult_Points(pointsR)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glVertex3f(pointsR[0][0],pointsR[0][1],pointsR[0][2])
        glVertex3f(pointsR[1][0],pointsR[1][1],pointsR[1][2])
        glVertex3f(pointsR[2][0],pointsR[2][1],pointsR[2][2])
        glVertex3f(pointsR[3][0],pointsR[3][1],pointsR[3][2])        
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(pointsR[0][0],pointsR[0][1],pointsR[0][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd() 
        glBegin(GL_LINES)
        glVertex3f(pointsR[1][0],pointsR[1][1],pointsR[1][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(pointsR[2][0],pointsR[2][1],pointsR[2][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()            
        glBegin(GL_LINES)
        glVertex3f(pointsR[3][0],pointsR[3][1],pointsR[3][2])
        glVertex3f(pointsR[4][0],pointsR[4][1],pointsR[4][2])
        glEnd()

