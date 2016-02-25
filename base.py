__author__ = 'dylan'

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OGL import *
import time
from macros import *
import math
from test_gravitation import *
from random import randrange as RR

class Base:
    def __init__(self , width , height , caption):
        pygame.init()
        self.width = width
        self.height = height
        pygame.display.set_mode((width ,height) , DOUBLEBUF|OPENGL)
        pygame.display.set_caption(caption)
        gluPerspective(45, (self.width/self.height), 0.1, 200.0)
        glTranslatef(0,0,0)
        glEnable(GL_DEPTH_TEST)
        #glRotatef(45,1,0,0)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.on = True

        self.ogl = Graphics()

        #cube = Cube(6,6,6,0,0,-30)
        #cube.setColor((0,255,0))
        #self.ogl.AddObject(cube, "basic", "Cube 1")
        py1 = PhysicObject(2.0,2.0,2.0,0.0,0.0,-50.0,10.0,(0,255,0),"object 1",self.ogl)
        py2 = PhysicObject(2.0,2.0,2.0,0.0,0.0,-70.0,10000.0,(255,0,0),"object 2",self.ogl)
        py3 = PhysicObject(2.0,2.0,2.0,5.0,0.0,-70.0,10.0,(0,0,255),"object 3",self.ogl)

        py1.SetSpeed(0.0000000001,0.0000000001,0)
        py3.SetSpeed(0.0000000001,0.0000000001,0)

        self.ogl.AddObject( py1 , "PhysicObj" , "Obj1" )
        self.ogl.AddObject( py2 , "PhysicObj" , "Obj2" )
        self.ogl.AddObject( py3 , "PhysicObj" , "Obj3" )

        for x in range(30):
            color = (RR(255) , RR(255) , RR(255))
            name = "Default " + str(x)
            pyx = PhysicObject(2.0,2.0,2.0,RR(20000)/10000.0,RR(20000)/10000.0,-70.0,10.0,color,name,self.ogl)
            pyx.SetSpeed(-0.0000000001,0.0000000002,0)
            self.ogl.AddObject( pyx , "PhysicObj" , name + "####" )
    def refresh(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on = False
        if KEY(K_ESCAPE):
            self.on = False

        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.ogl.refresh()
        pygame.display.flip()
        self.clock.tick(self.FPS)

