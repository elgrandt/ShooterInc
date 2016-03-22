import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import DOUBLEBUF, OPENGL, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_s
import OGL
from macros import KEY
from math import sin, cos, sqrt, radians
import numpy as np

def DrawAxis():
    vertices = [[[0,0,-10],[0,0,10]],[[0,-10,0],[0,10,0]],[[-10,0,0],[10,0,0]]]
    colors = [[255,255,0],[0,255,255],[0,255,0]]
    glLineWidth(2)
    for x in range(len(vertices)):
        glBegin(GL_LINES)
        glColor3fv(colors[x])
        glVertex3fv(vertices[x][0])
        glVertex3fv(vertices[x][1])
        glEnd()

class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def Generate(self, angle, x_axis, y_axis, z_axis):
        sinA = sin(radians(angle)/2)
        cosA = cos(radians(angle)/2)
        self.x = x_axis * sinA
        self.y = y_axis * sinA
        self.z = z_axis * sinA
        self.w = cosA
        self.Normalize(self)
    def Magnitude(self):
        return sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
    def Normalize(self, quat):
        mag = quat.Magnitude()
        quat.x = quat.x/mag
        quat.y = quat.y/mag
        quat.z = quat.z/mag
        quat.w = quat.w/mag
    def __mul__(self, other):
        ret = [0,0,0,0]
        ret[0] = self.w*other.x - self.z*other.y + self.y*other.z + self.x*other.w
        ret[1] = self.z*other.x + self.w*other.y - self.x*other.z + self.y*other.w
        ret[2] = -self.y*other.x + self.x*other.y + self.w*other.z + self.z*other.w
        ret[3] = -self.x*other.x - self.y*other.y - self.z*other.z + self.w*other.w
        return Quaternion(*ret)
    def GetMatrix(self):
        """
            |       2     2                                |
            | 1 - 2Y  - 2Z    2XY - 2ZW      2XZ + 2YW     |
            |                                              |
            |                       2     2                |
        M = | 2XY + 2ZW       1 - 2X  - 2Z   2YZ - 2XW     |
            |                                              |
            |                                      2     2 |
            | 2XZ - 2YW       2YZ + 2XW      1 - 2X  - 2Y  |
            |                                              |
        """
        X,Y,Z,W = self.x, self.y, self.z, self.w
        matrix = np.array([
            [1 - 2 * Y * Y - 2 * Z * Z, 2 * X * Y - 2* Z * W     , 2 * X * Z + 2 * Y * W    , 0],
            [2 * X * Y + 2 * Z * W    , 1 - 2 * X * X - 2 * Z * Z, 2 * Y * Z - 2 * X * W    , 0],
            [2 * X * Z - 2 * Y * W    , 2 * Y * Z + 2 * X * W    , 1 - 2 * X * X - 2 * Y * Y, 0],
            [0                        , 0                        , 0                        , 1]
        ])
        return matrix

def rotateLocalAxis(rX, rY, rZ):
    quaX = Quaternion()
    quaX.Generate(rX,1,0,0)
    quaY = Quaternion()
    quaY.Generate(rY,0,1,0)
    quaZ = Quaternion()
    quaZ.Generate(rZ,0,0,1)
    mult = quaX * quaY * quaZ
    glMultMatrixf(mult.GetMatrix())

def rotateGlobalAxis(rX, rY, rZ):
    glRotate(rX, 1, 0, 0)
    glRotate(rY, 0, 1, 0)
    glRotate(rZ, 0, 0, 1)

def main():
    pygame.init()
    pygame.display.set_mode((800 ,600) , DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Rotation Test")
    gluPerspective(45, (800/600), 0.1, 200.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    Cube = OGL.Cube(5,5,5,0,0,0)
    Cube.setColor(0,0,255)
    Cube.setFilled(True)
    gluLookAt( -10, 10, 20, 0, 0, 0, 0 , 1 , 0)

    rotX = 0
    rotY = 0
    rotZ = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if KEY(K_ESCAPE):
            return
        if KEY(K_LEFT):
            rotY += 1
        if KEY(K_RIGHT):
            rotY -= 1
        if KEY(K_UP):
            rotX += 1
        if KEY(K_DOWN):
            rotX -= 1
        if KEY(K_w):
            rotZ += 1
        if KEY(K_s):
            rotZ -= 1
        if rotX > 360:
            rotX = 0
        if rotY > 360:
            rotY = 0
        if rotZ > 360:
            rotZ = 0

        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        rotateLocalAxis(rotX, rotY, rotZ)
        Cube.blit()
        glPopMatrix()

        DrawAxis()

        pygame.display.flip()

if __name__ == "__main__":
    main()