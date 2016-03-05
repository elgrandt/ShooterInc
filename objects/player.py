import OGL
from macros import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import shoot

class Ak47(OGL.Cube):
    def __init__(self):
        self.standby_pos = [.4,-1,-3]#[.3,-.25,-1]
        self.pointing_pos = [0,-.6,-3]#[0,-.25,-1]
        OGL.Cube.__init__(self,.5,.3,.1,*self.standby_pos)
        self.setColor(100,100,100)
        self.setFilled(True)
        self.mode = "Standby" # Modes Standby and Pointing
        self.transition_time = 10.0
        self.actual_rotation_y = 0.0
        self.actual_rotation_z = -25
        self.model = OGL.OBJ("models/Handgun_obj.obj",swapyz=False)
        self.colitions = []
    def logic(self):
        pressing2 = pygame.mouse.get_pressed()[2]
        if self.mode == "Standby":
            self.real_pos = self.standby_pos[:]
            self.actual_rotation_y = 35
            self.actual_rotation_z = -25
            if pressing2:
                self.mode = "Transition to Pointing"
        if self.mode == "Transition to Pointing":
            self.actual_rotation_y -= (35-90) / self.transition_time
            self.actual_rotation_z -= -25 / self.transition_time
            self.real_pos[0] -= float(self.standby_pos[0] - self.pointing_pos[0]) / self.transition_time
            self.real_pos[1] -= float(self.standby_pos[1] - self.pointing_pos[1]) / self.transition_time
            self.real_pos[2] -= float(self.standby_pos[2] - self.pointing_pos[2]) / self.transition_time
            if int(self.actual_rotation_y) == 90:
                self.mode = "Pointing"
        if self.mode == "Pointing":
            self.real_pos = self.pointing_pos[:]
            self.actual_rotation_z = 0
            if not pygame.mouse.get_pressed()[2]:
                self.mode = "Transition to Standby"
        if self.mode == "Transition to Standby":
            self.actual_rotation_y += (35-90) / self.transition_time
            self.actual_rotation_z += -25 / self.transition_time
            self.real_pos[0] += float(self.standby_pos[0] - self.pointing_pos[0]) / self.transition_time
            self.real_pos[1] += float(self.standby_pos[1] - self.pointing_pos[1]) / self.transition_time
            self.real_pos[2] += float(self.standby_pos[2] - self.pointing_pos[2]) / self.transition_time
            if int(self.actual_rotation_y) == 35:
                self.mode = "Standby"
                self.real_pos = self.standby_pos[:]
        self.rotationY -= self.actual_rotation_y
        self.setRotationZ(self.actual_rotation_z)
    def blit(self):
        for x in self.model.objects.keys():
            self.model.objects[x].angley = 180
        self.model.blit()
        #glRotatef(180,0,1,0)
        #glCallList(self.model.gl_list)

class Player(OGL.ComplexObject):
    def __init__(self):
        OGL.ComplexObject.__init__(self,0,0,0)
        self.speed = .3
        self.angle = 0
        self.angle_speed = 0.1
        self.static_objects = []
        primary_weapon = Ak47()
        self.addObject(primary_weapon,"Primary Weapon")
        self.static_objects.append(primary_weapon)
        pointer = OGL.Ellipsoid(.004,.004,.004,0,0,-1)
        pointer.setColor(0,0,255)
        pointer.setFilled(True)
        self.addObject(pointer,"Pointer")
        self.static_objects.append(pointer)
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

        for obj in self.static_objects:
            obj.setPos( -obj.real_pos[2] * sin(radians(-self.angle)) + obj.real_pos[0] * cos(radians(-self.angle)), obj.real_pos[1], obj.real_pos[2] * cos(radians(-self.angle)) + obj.real_pos[0] * sin(radians(-self.angle)))
            obj.setRotationY(self.angle)

        #if CLICK():
        dist = 50
        pointing = self.x + sin(radians(self.angle)) * dist, self.y, self.z - cos(radians(self.angle)) * dist
        enemies = self.parent.QueryAllOfType("Enemy")
        pointer = self.getObject("Pointer")
        pointer.setColor(0,0,0)
        for en in enemies:
            start = -(en.x - en.width/2.0) , en.y - en.height/2.0 , en.z - en.depth/2.0
            end = -(en.x + en.width/2.0) , en.y + en.height/2.0 , en.z + en.depth/2.0
            #print start , end
            colition = shoot.EasyCollide([self.x,self.y,self.z], pointing, start, end)
            if colition != False:
                pointer.setColor(255,0,255)