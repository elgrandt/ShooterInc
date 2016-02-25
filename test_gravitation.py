
__author__ = 'dylan'

from OGL import *
from time import *
from math import *

G_CONSTANT = 0.000000000000000000000001

class PhysicObject(Object):
    def __init__(self, w , h , d , x , y , z , mass , color, name , ogl ):
        self.mass = mass
        self.object = Cube(w,h,d,x,y,z)
        self.object.setColor(color)
        self.ogl = ogl
        self.ogl.AddObject( self.object , "Physic" , name )
        self.speedX = 0
        self.speedY = 0
        self.speedZ = 0
        self.last_update = 0

    def SetSpeed(self,sx,sy,sz):
        self.speedX = sx
        self.speedY = sy
        self.speedZ = sz

    def refresh(self):
        #return 0
        dif = time() - self.last_update
        physic_objects = self.ogl.QueryAllOfType("PhysicObj")

        acel_x = 0
        acel_y = 0
        acel_z = 0
        for x in range(len(physic_objects)):
            actual = physic_objects[x]
            if actual.name == self.name:
                continue
            dx = actual.object.x - self.object.x
            dy = actual.object.y - self.object.y
            dz = actual.object.z - self.object.z

            dis = sqrt(dx*dx+dy*dy+dz*dz)
            #print dx , actual.mass , dis , G_CONSTANT
            acel_x += (G_CONSTANT * actual.mass * dx) / dis
            acel_y += (G_CONSTANT * actual.mass * dy) / dis
            acel_z += (G_CONSTANT * actual.mass * dz) / dis

        self.speedX += acel_x * dif
        self.speedY += acel_y * dif
        self.speedZ += acel_z * dif

        self.object.x += self.speedX * dif
        self.object.y += self.speedY * dif
        self.object.z += self.speedZ * dif
