import OGL
from macros import *
<<<<<<< HEAD
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
=======
import math
>>>>>>> 8f2e28495a61196ff3c848b7c352838f3d1aae61

class Player(OGL.ComplexObject):
    def __init__(self):
        OGL.ComplexObject.__init__(self,0,0,0)
        self.speed = .3
        self.angle = 0


    def logic(self):
        if KEY(pygame.K_LEFT):
            self.x -= self.speed
        if KEY(pygame.K_RIGHT):
            self.x += self.speed
        if KEY(pygame.K_UP):
            self.z -= self.speed
        if KEY(pygame.K_DOWN):
            self.z += self.speed
        if KEY(pygame.K_a):
            self.angle -= 0.1
            self.angle = (self.angle+360)%360
        if KEY(pygame.K_d):
<<<<<<< HEAD
            self.angle += 0.1
            self.angle = (self.angle+360) % 360

        plus_a = sin(self.angle) * 20;
        plus_b = cos(self.angle) * 20;
        print plus_a , plus_b
        gluLookAt( self.x , self.y , self.z , self.x - plus_a, self.y , self.z - plus_b , 0 , 1 , 0)
=======
            self.angle += 1
        if self.angle > 360:
            self.angle = 0
>>>>>>> 8f2e28495a61196ff3c848b7c352838f3d1aae61
