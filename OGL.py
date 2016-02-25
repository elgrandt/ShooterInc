__author__ = 'Dylan'
from OpenGL.GL import *
import math
import pygame
from macros import *

class Object:
    def __init__(self , width , height , depth , x , y , z):
        self.width = width
        self.height = height
        self.depth = depth
        self.x = x
        self.y = y
        self.z = z
        self.name = 'Unnamed #' + RS(100000)
        self.visible = True
        self.dead = False
    def refresh(self):
        ## code to draw ##
        pass


class Texture:
    def __init__(self):
        texture = 0
        width = 1
        height = 1

class Graphics:
    def __init__(self):
        self.objects = dict()
        self.types = dict() ###
    def AddObject(self , object , type, name):
        object.name = name
        object.type = type

        self.objects[name] = object

        if not self.types.has_key(type):
            self.types[type] = []
        self.types[type].append( object )
    def GetObject(self,name):
        return self.objects[name]
    def Delete(self , name):
        self.objects[name].dead = True
        type = self.objects[name].type
        del self.objects[name]
        for x in range(len(self.objects[type])):
            if self.objects[type][x].name == name:
                del self.objects[type][x]
                return 0
    def refresh(self):
        for x in self.objects.keys():
            self.objects[x].refresh()
    def QueryAllOfType(self , type):
        return self.types[type]
    def DrawEllipsoid(self, uiStacks, uiSlices, fA, fB, fC, filled = True):
        Pi = 3.1416
        tStep = Pi / uiSlices
        sStep = Pi / uiStacks
        second_parameter = GL_FILL
        if not filled:
            second_parameter = GL_LINE
        glPolygonMode(GL_FRONT_AND_BACK, second_parameter)
        t = -Pi/2
        while (t <= (Pi/2)+.0001):
            glBegin(GL_TRIANGLE_STRIP)
            s = -Pi
            while (s <= Pi+.0001):
                glVertex3f(fA * math.cos(t) * math.cos(s), fB * math.cos(t) * math.sin(s), fC * math.sin(t))
                glVertex3f(fA * math.cos(t+tStep) * math.cos(s), fB * math.cos(t+tStep) * math.sin(s), fC * math.sin(t+tStep))
                s += sStep
            glEnd()
            t += tStep
    def GenerateTexture(self,surface):
        textureData = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        ret = Texture()
        ret.width = width
        ret.height = height
        ret.texture = texture
        return ret
    def BlitTexture(self, texture, w, h, x, y, rx = 1, ry = 1):
        glBindTexture( GL_TEXTURE_2D, texture )
        glEnable( GL_TEXTURE_2D )

        glBegin(GL_QUADS)
        glTexCoord2f(   0,   0 );  glVertex2f(x    ,  y )
        glTexCoord2f(rx  ,   0 );  glVertex2f(x + w,  y )
        glTexCoord2f(rx  ,  -ry);  glVertex2f(x + w,  y + h)
        glTexCoord2f(0   ,  -ry);  glVertex2f(x    ,  y + h)
        glEnd()

        glDisable( GL_TEXTURE_2D )

class Cube(Object):
    def setColor(self, color):
        self.color = color
    def refresh(self):
        w = self.width / 2
        h = self.height / 2
        d = self.depth / 2
        vertices= (
        (w, -h, -d),
        (w, h, -d),
        (-w, h, -d),
        (-w, -h, -d),
        (w, -h, d),
        (w, h, d),
        (-w, -h, d),
        (-w, h, d)
        )
        edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )

        surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
        )
        glPushMatrix()
        glTranslatef(self.x,self.y,self.z)
        glBegin(GL_QUADS)

        for surface in surfaces:
            x = 0
            glColor3fv(self.color)
            for vertex in surface:
                x+=1
                glVertex3fv(vertices[vertex])

        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor3fv((0,0,0))
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()
