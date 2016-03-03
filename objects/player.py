import OGL
from macros import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Ak47(OGL.Cube):
    def __init__(self):
        OGL.Cube.__init__(self,3,1,0.3,0,0,-10)
        self.setColor(100,100,100)
        self.setFilled(True)
    def logic(self):
        pass

class Player(OGL.ComplexObject):
    def __init__(self):
        OGL.ComplexObject.__init__(self,0,0,0)
        self.speed = .3
        self.angle = 0
        self.angle_speed = 0.1
        primary_weapon = Ak47()
        self.addObject(primary_weapon,"Primary Weapon")
    def logic(self):
        self.angle -= (MPOS()[0] - SSIZE()[0]/2) * self.angle_speed
        if (self.angle < -180):
            self.angle = 180
        if self.angle > 180:
            self.angle = -180
        pygame.mouse.set_pos(SSIZE()[0]/2,SSIZE()[1]/2)
        pygame.mouse.set_visible(False)
        if KEY(pygame.K_a):
            self.x -= self.speed * cos(radians(self.angle))
            self.z += self.speed * sin(radians(self.angle))
        if KEY(pygame.K_d):
            self.x += self.speed * cos(radians(self.angle))
            self.z -= self.speed * sin(radians(self.angle))
        if KEY(pygame.K_w):
            self.x -= self.speed * sin(radians(self.angle))
            self.z -= self.speed * cos(radians(self.angle))
        if KEY(pygame.K_s):
            self.x += self.speed * sin(radians(self.angle))
            self.z += self.speed * cos(radians(self.angle))
        plus_a = sin(radians(self.angle))
        plus_b = cos(radians(self.angle))
        gluLookAt( self.x , self.y , self.z , self.x - plus_a, self.y , self.z - plus_b , 0 , 1 , 0)