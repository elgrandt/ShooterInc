import OGL
from macros import *
import math

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
            self.angle -= 1
        if KEY(pygame.K_d):
            self.angle += 1
        if self.angle > 360:
            self.angle = 0