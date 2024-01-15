from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math

class OpMat:
    def __init__(self):
        self.T = np.identity(4)
        self.R = np.identity(4)
        self.A = np.identity(4)
        self.S = np.identity(4)
        
    def translate(self, tx, ty, tz):
        self.T = np.identity(4)
        self.T[0][3] = tx
        self.T[1][3] = ty
        self.T[2][3] = tz
        self.A = self.T @ self.A

    def rotateX(self, deg):
        self.R = np.identity(4)
        radians = np.radians(deg)
        self.R[1][1] = np.cos(radians)
        self.R[1][2] = -1 * np.sin(radians)
        self.R[2][1] = np.sin(radians)
        self.R[2][2] = np.cos(radians)
        self.A = self.R @ self.A
    
    def rotateY(self, deg):
        self.R = np.identity(4)
        radians = np.radians(deg)
        self.R[0][0] = np.cos(radians)
        self.R[0][2] = np.sin(radians)
        self.R[2][0] = -1 * np.sin(radians)
        self.R[2][2] = np.cos(radians)
        self.A = self.R @ self.A

    def rotateZ(self, deg):
        self.R = np.identity(4)
        radians = np.radians(deg)
        self.R[0][0] = np.cos(radians)
        self.R[0][1] = -1  * np.sin(radians)
        self.R[1][0] = np.sin(radians)
        self.R[1][1] = np.cos(radians)
        self.A = self.R @ self.A
    
    def scale(self, sx, sy, sz):
        self.S = np.identity(4)
        self.S[0][0] = sx
        self.S[1][1] = sy
        self.S[2][2] = sz
        self.A = self.S @ self.A

    def rotate(self, theta, x, y, z):
        # Asumimos que P1 es (0, 0, 0)
        v_norm = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
        a = x / v_norm
        b = y / v_norm
        c = z / v_norm
        d = math.sqrt(math.pow(b, 2) + math.pow(c, 2))

        if b == 0 and c == 0:
            # rotacion en X
            self.rotateX(theta)
            return

        # Else
        def RX():
            R = np.identity(4)
            R[1][1] = c / d
            R[1][2] = -1 * b / d
            R[2][1] = b / d
            R[2][2] = c / d
            return R
        
        def RX_minus():
            R = np.identity(4)
            R[1][1] = c / d
            R[1][2] = b / d
            R[2][1] = -1 * b / d
            R[2][2] = c / d
            return R
        
        def RY():
            R = np.identity(4)
            R[0][0] = d
            R[0][2] = a
            R[2][0] = -1 * a
            R[2][2] = d
            return R
        
        def RY_minus():
            R = np.identity(4)
            R[0][0] = d
            R[0][2] = -1 * a
            R[2][0] = a
            R[2][2] = d
            return R
        
        def RZ():
            R = np.identity(4)
            radians = np.radians(theta)
            R[0][0] = np.cos(radians)
            R[0][1] = -1  * np.sin(radians)
            R[1][0] = np.sin(radians)
            R[1][1] = np.cos(radians)
            return R
        
        self.A = self.A @ RX_minus() @ RY_minus() @ RZ() @ RY() @ RX()


    def mult_Points(self, points):
        pointsR = (self.A @ points.T).T

        for i in range(0, pointsR.shape[1] + 1):
            for j in range(0, 4):
                points[i][j] = pointsR[i][j]

    def loadIdentity(self):
        self.A = np.identity(4)