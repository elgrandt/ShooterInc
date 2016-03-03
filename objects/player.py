import OGL
from macros import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Player(OGL.ComplexObject):
    def __init__(self):
        OGL.ComplexObject.__init__(self,0,0,0)
        self.speed = .3
        self.angle = 0


    def logic(self):
        if KEY(pygame.K_LEFT):
            self.x -= self.speed * cos(radians(self.angle))
            self.z += self.speed * sin(radians(self.angle))
        if KEY(pygame.K_RIGHT):
            self.x += self.speed * cos(radians(self.angle))
            self.z -= self.speed * sin(radians(self.angle))
        if KEY(pygame.K_UP):
            self.z -= self.speed
        if KEY(pygame.K_DOWN):
            self.z += self.speed
        if KEY(pygame.K_a):
            self.angle -= 1
            if (self.angle < -180):
                self.angle = 180
        if KEY(pygame.K_d):
            self.angle += 1
            if self.angle > 180:
                self.angle = -180
        print self.angle
        plus_a = sin(radians(self.angle))
        plus_b = cos(radians(self.angle))
        print plus_a , plus_b
        gluLookAt( self.x , self.y , self.z , self.x - plus_a, self.y , self.z - plus_b , 0 , 1 , 0)