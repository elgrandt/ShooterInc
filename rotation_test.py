import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import DOUBLEBUF, OPENGL, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_s
import OGL
from macros import KEY

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
        glRotate(rotX,1,0,0)
        glRotate(rotY,0,1,0)
        glRotate(rotZ,0,0,1)
        Cube.blit()
        glPopMatrix()

        DrawAxis()

        pygame.display.flip()

if __name__ == "__main__":
    main()