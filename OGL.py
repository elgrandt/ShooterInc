__author__ = 'Dylan'
from OpenGL.GL import *
from OpenGL.GLU import *
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
        self.rotation = False
        self.color = False
        self.filled = True
        self.manualPosition = False
        self.manualRotation = False
        self.manualColor    = False
        self.manualFill     = False
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setZ(self,z):
        self.z = z
    def setPos(self,x,y,z):
        self.x, self.y, self.z = x,y,z
    def setRotation(self, angle, x, y, z):
        self.rotation = [angle, x, y, z]
    def setColor(self, r, g, b):
        self.color = (r,g,b)
    def setFilled(self, is_filled):
        self.filled = is_filled
    def blit(self):
        ### Should be replaced with the heritage's blit function ###
        pass
    def logic(self):
        pass
    def refresh(self):
        if self.visible and not self.dead:
            glPushMatrix()
            if not self.manualPosition:
                glTranslatef(self.x,self.y,self.z)
            if not self.manualRotation:
                if self.rotation != False:
                    glRotatef(*self.rotation)
            if not self.manualColor:
                if self.color != False:
                    glColor3fv(self.color)
            if not self.manualFill:
                second_parameter = GL_FILL
                if not self.filled:
                    second_parameter = GL_LINE
                glPolygonMode(GL_FRONT_AND_BACK, second_parameter)
            self.blit()
            glPopMatrix()
        self.logic()

class Object2D:
    def __init__(self, x, y):
        self.width = -1
        self.height = -1
        self.x = x
        self.y = y
        self.name = "Unnamed #" + RS(100000)
        self.visible = True
        self.dead = False
        self.surface = None
        self.texture = None
        self.autoblit = True
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setSurface(self, surface):
        self.surface = surface
        self.texture = self.generateTexture(surface)
    def generateTexture(self,surface):
        textureData = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        return texture
    def blitTexture(self, texture, w, h, x, y, rx = 1, ry = 1):
        if texture == None:
            return
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBindTexture( GL_TEXTURE_2D, texture )
        glEnable( GL_TEXTURE_2D )

        glBegin(GL_QUADS)
        glColor4f(255,255,255,255)
        glTexCoord2f(   0,   0 );  glVertex2f(x    ,  y    )
        glTexCoord2f(rx  ,   0 );  glVertex2f(x + w,  y    )
        glTexCoord2f(rx  ,  -ry);  glVertex2f(x + w,  y + h)
        glTexCoord2f(0   ,  -ry);  glVertex2f(x    ,  y + h)
        glEnd()
        glDisable( GL_TEXTURE_2D )
    def blitSurface(self , x=-1 , y=-1 , w=-1 , h=-1 , rx=1 , ry=1):
        if self.surface != None:
            if x == -1:
                x = self.x
            if y == -1:
                y = self.y
            if w == -1:
                w = self.width
                if self.width == -1:
                    w = self.surface.get_size()[0]
            if h == -1:
                h = self.height
                if self.height == -1:
                    h = self.surface.get_size()[1]
            self.blitTexture(self.texture, w, h, x, y, rx, ry)
    def blit(self):
        pass
    def refresh(self):
        if self.visible and not self.dead:
            self.blit()
            if self.autoblit:
                self.blitSurface()

class ComplexObject(Object):
    def __init__(self,x,y,z):
        Object.__init__(self,0,0,0,x,y,z)
        self.visible = False
        self.objects = dict()
    def addObject(self, object, name):
        object.name = name
        self.objects[name] = object
    def logic(self):
        glTranslatef(self.x,self.y,self.z)
        for x in self.objects.keys():
            self.objects[x].refresh()

class Texture:
    def __init__(self):
        texture = 0
        width = 1
        height = 1

class Graphics:
    def __init__(self):
        self.objects = dict()
        self.objects2d = dict()
        self.types = dict() ###
    def AddObject(self , object , type, name):
        object.name = name
        object.type = type

        self.objects[name] = object

        if not self.types.has_key(type):
            self.types[type] = []
        self.types[type].append( object )
    def GetObject(self,name):
        if name in self.objects.keys():
            return self.objects[name]
        else:
            return None
    def Delete(self , name):
        self.objects[name].dead = True
        type = self.objects[name].type
        del self.objects[name]
        for x in range(len(self.objects[type])):
            if self.objects[type][x].name == name:
                del self.objects[type][x]
                return 0
    def Add2D(self , object , name):
        object.name = name
        self.objects2d[name] = object
    def Delete2D(self , name):
        self.objects2d[name].dead = True
        del self.objects2d[name]
    def refresh(self):
        gluPerspective(45, (SSIZE()[0]/SSIZE()[1]), 0.1, 200.0)
        glEnable(GL_DEPTH_TEST)
        player = self.GetObject("Main Player")
        #if player != None:
        #    gluLookAt(player.x, player.y, player.z, player.x + math.sin(math.radians(player.angle))*20, player.y, player.z - math.cos(math.radians(player.angle))*20, 0,1,0)
        for x in self.objects.keys():
            self.objects[x].refresh()
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glOrtho(0.0, SSIZE()[0], SSIZE()[1], 0.0, -1.0, 10.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        for x in self.objects2d.keys():
            glLoadIdentity()
            self.objects2d[x].refresh()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    def QueryAllOfType(self , type):
        return self.types[type]

class Cube(Object):
    def blit(self):
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

class Ellipsoid(Object):
    def __init__(self,width,height,depth,x,y,z):
        Object.__init__(self,width,height,depth,x,y,z)
        self.uiStacks = 10
        self.uiSlices = 10
    def setQuality(self, quality):
        self.uiStacks = quality
        self.uiSlices = quality
    def blit(self):
        Pi = 3.1416
        tStep = Pi / self.uiSlices
        sStep = Pi / self.uiStacks
        t = -Pi/2
        while (t <= (Pi/2)+.0001):
            glBegin(GL_TRIANGLE_STRIP)
            s = -Pi
            while (s <= Pi+.0001):
                glVertex3f(self.width * math.cos(t) * math.cos(s), self.height * math.cos(t) * math.sin(s), self.depth * math.sin(t))
                glVertex3f(self.width * math.cos(t+tStep) * math.cos(s), self.height * math.cos(t+tStep) * math.sin(s), self.depth * math.sin(t+tStep))
                s += sStep
            glEnd()
            t += tStep