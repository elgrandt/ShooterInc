from oauthlib.oauth2.rfc6749.clients import backend_application

__author__ = 'Dylan'
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from math import *
import pygame
from macros import *
import copy
import threading
import numpy as np

loading_objects = 0

class Object:
    def __init__(self , width , height , depth , x , y , z):
        self.width = width
        self.height = height
        self.depth = depth
        self.x = x
        self.y = y
        self.z = z
        self.real_pos = [x,y,z]
        self.name = 'Unnamed #' + RS(100000)
        self.visible = True
        self.dead = False
        self.rotationX = False
        self.rotationY = False
        self.rotationZ = False
        self.color = False
        self.filled = True
        self.manualPosition = False
        self.manualRotation = False
        self.manualColor    = False
        self.manualFill     = False
        self.parent = None
    def setParent(self,parent):
        self.parent = parent
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setZ(self,z):
        self.z = z
    def setPos(self,x,y,z):
        self.x, self.y, self.z = x,y,z
    def setRotationX(self, angle):
        self.rotationX = angle
    def setRotationY(self, angle):
        self.rotationY = angle
    def setRotationZ(self, angle):
        self.rotationZ = angle
    def setColor(self, r, g, b):
        self.color = (r/255.0,g/255.0,b/255.0)
    def setFilled(self, is_filled):
        self.filled = is_filled
    def blit(self):
        ### Should be replaced with the heritage's blit function ###
        pass
    def logic(self):
        pass
    def logic2(self):
        pass
    def refresh(self):
        self.logic()
        if self.visible and not self.dead:
            glPushMatrix()
            if not self.manualPosition:
                glTranslatef(self.x,self.y,self.z)
            if not self.manualRotation:
                if self.rotationX != False:
                    glRotatef(self.rotationX,1,0,0)
                if self.rotationY != False:
                    glRotatef(self.rotationY,0,1,0)
                if self.rotationZ != False:
                    glRotatef(self.rotationZ,0,0,1)
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
        self.logic2()

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
    def getObject(self,name):
        if name in self.objects.keys():
            return self.objects[name]
        else:
            return None
    def refresh(self):
        self.logic()
        glTranslatef(self.x,self.y,self.z)
        for x in self.objects.keys():
            self.objects[x].refresh()
        glTranslatef(-self.x,-self.y,-self.z)

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
        #glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0,0,0,1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (.8,.8,.8,1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0,0,0,1))
        glLightfv(GL_LIGHT0, GL_POSITION, (0,1,0,1))
        glEnable(GL_LIGHT0)
        for x in self.objects.keys():
            self.objects[x].refresh()
        glDisable(GL_DEPTH_TEST)
        #glDisable(GL_LIGHTING)
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
        if self.types.has_key(type):
            return self.types[type]
        return [

        ]

class Cube(Object):
    def blit(self):
        w = self.width / 2.0
        h = self.height / 2.0
        d = self.depth / 2.0
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

def MTL(filename):
    contents = {}
    contents['map_Kd'] = False
    contents['objects'] = []
    mtl = None
    try:
        open("models/"+filename,"r")
    except:
        print "Error cargando el archivo",filename
        return {}
    for line in open("models/"+filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
            contents['objects'].append(values[1])
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd' or values[0] == 'map_Ks':
            # load the texture referred to by this declaration
            contents['map_Kd'] = True
            mtl[values[0]] = values[1]
        elif values[0] == 'map_Bump' or values[0] == 'map_Ks' or values[0] == 'map_Ka' or values[0] == 'map_bump' or values[0] == 'bump':
            pass
        else:
            mtl[values[0]] = map(float, values[1:])
    return contents

class ModelGroup:
    def __init__(self):
        self.name = ""
        self.faces = []
        self.mtl = None
        self.list = None
        self.pos = [0,0,0]
        self.anglex = 0
        self.angley = 0
        self.anglez = 0
        self.enabled = True

class ModelObject:
    def __init__(self):
        self.name = ""
        self.faces = []
        self.mtl = None
        self.list = None
        self.pos = [0,0,0]
        self.anglex = 0
        self.angley = 0
        self.anglez = 0
        self.enabled = True

class OBJ:
    def __init__(self, filename, swapyz=False, scale = 1, work_with_obj = False):
        """Loads a Wavefront OBJ file. """
        self.work_with_obj = work_with_obj
        self.pos = [0,0,0]
        self.anglex = 0
        self.angley = 0
        self.anglez = 0
        self.groups = {}
        self.objects = {}
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.scale = scale
        self.color = (0,0,0)
        self.width, self.height, self.depth = 0,0,0
        self.loaded = False
        self.almost_loaded = False
        self.onload = None
        global loading_objects
        loading_objects += 1
        load_thread = threading.Thread(target=self.loadFile, name = "ObjectLoad", args=[filename, swapyz])
        load_thread.start()
    def loadFile(self, filename, swapyz):
        actual_group = ModelGroup()
        actual_obj = ModelObject()
        material = None
        self.mtl = None
        minx, miny, minz = 10000000, 10000000, 10000000
        maxx, maxy, maxz = -10000000, -10000000, -10000000
        for line in open("models/"+filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                minx = min(v[0]/self.scale,minx)
                miny = min(v[1]/self.scale,miny)
                minz = min(v[2]/self.scale,minz)
                maxx = max(v[0]/self.scale,maxx)
                maxy = max(v[1]/self.scale,maxy)
                maxz = max(v[2]/self.scale,maxz)
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                actual_group.faces.append((face, norms, texcoords, material))
                actual_obj.faces.append((face, norms, texcoords, material))
            elif values[0] == 'g':
                if actual_group.name != "":
                    self.groups[actual_group.name] = copy.deepcopy(actual_group)
                actual_group = ModelGroup()
                actual_group.name = values[1]
            elif values[0] == 'o':
                if actual_obj.name != "":
                    self.objects[actual_obj.name] = copy.deepcopy(actual_obj)
                actual_obj = ModelObject()
                actual_obj.name = values[1]
        self.groups[actual_group.name] = copy.deepcopy(actual_group)
        self.objects[actual_obj.name] = copy.deepcopy(actual_obj)

        self.width = maxx - minx
        self.height = maxy - miny
        self.depth = maxz - minz
        self.almost_loaded = True
    def makeLists(self):
        for x in self.mtl['objects']:
            for y in self.mtl[x].keys():
                if y == 'map_Kd' or y == 'map_Ks':
                    surf = pygame.image.load("models/textures/"+self.mtl[x][y])
                    image = pygame.image.tostring(surf, 'RGBA', 1)
                    ix, iy = surf.get_rect().size
                    texid = self.mtl[x][y] = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texid)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        GL_LINEAR)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                        GL_UNSIGNED_BYTE, image)
                    glBindTexture(GL_TEXTURE_2D,0)
        work = self.groups
        if self.work_with_obj:
            work = self.objects
        for x in work.keys():
            obj = work[x]
            gl_list = glGenLists(1)
            glNewList(gl_list, GL_COMPILE)
            glFrontFace(GL_CCW)
            glColor4f(255,255,255,255)
            glEnable(GL_TEXTURE_2D)
            for face in obj.faces:
                vertices, normals, texture_coords, material = face
                if self.mtl:
                    mtl = self.mtl[material]
                    #glMaterialfv(GL_FRONT, GL_AMBIENT, mtl['Ka'])
                    if 'Kd' in mtl:
                        glMaterialfv(GL_FRONT, GL_DIFFUSE, mtl['Kd'])
                    if 'Ks' in mtl:
                        glMaterialfv(GL_FRONT, GL_SPECULAR, mtl['Ks'])
                    if 'Ns' in mtl:
                        glMaterialf(GL_FRONT, GL_SHININESS, mtl['Ns'][0]/1000*128)
                    if 'map_Kd' in mtl:
                        # use diffuse texmap
                        glBindTexture(GL_TEXTURE_2D, mtl['map_Kd'])
                        if 'map_Ks' in mtl:
                            pass#glBindTexture(GL_TEXTURE_2D, mtl['map_Ks'])

                else:
                    glColor3fv(self.color)
                glBegin(GL_POLYGON)
                for i in range(len(vertices)):
                    if normals[i] > 0:
                        glNormal3fv(self.normals[normals[i] - 1])
                    if texture_coords[i] > 0:
                        if self.mtl:
                            if self.mtl['map_Kd']:
                                glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                    v = self.vertices[vertices[i] - 1]
                    glVertex3f(v[0]/self.scale, v[1]/self.scale, v[2]/self.scale)
                glEnd()
                glBindTexture(GL_TEXTURE_2D,0)
            glDisable(GL_TEXTURE_2D)
            glEndList()
            obj.list = gl_list
        self.loaded = True
        global loading_objects
        loading_objects -= 1
        if self.onload != None:
            self.onload()
    def getGroup(self, name):
        if not self.loaded:
            return None
        for x in self.groups.keys():
            if self.groups[x].name == name:
                return self.groups[x]
        return None
    def getObject(self, name):
        if not self.loaded:
            return None
        for x in self.objects.keys():
            if self.objects[x].name == name:
                return self.objects[x]
        return None
    def blit(self):
        if not self.loaded:
            if self.almost_loaded:
                self.makeLists()
            return
        glTranslatef(*self.pos)
        glRotatef(self.anglex,1,0,0)
        glRotatef(self.angley,0,1,0)
        glRotatef(self.anglez,0,0,1)
        glColor4f(255,255,255,255)
        work = self.groups
        if self.work_with_obj:
            work = self.objects
        for obj in work.keys():
            if work[obj].enabled:
                glTranslatef(*work[obj].pos)
                glRotatef(work[obj].anglex,1,0,0)
                glRotatef(work[obj].angley,0,1,0)
                glRotatef(work[obj].anglez,0,0,1)
                glCallList(work[obj].list)
                glRotatef(-work[obj].anglez,0,0,1)
                glRotatef(-work[obj].angley,0,1,0)
                glRotatef(-work[obj].anglex,1,0,0)
                glTranslatef(-work[obj].pos[0],-work[obj].pos[1],-work[obj].pos[2])
        glRotatef(-self.anglez,0,0,1)
        glRotatef(-self.angley,0,1,0)
        glRotatef(-self.anglex,1,0,0)
        glTranslatef(-self.pos[0],-self.pos[1],-self.pos[2])

class Text2D(Object2D):
    def __init__(self, x, y, text, size, color = (0,0,0), background = (0,0,0), font = None):
        Object2D.__init__(self, x, y)
        self.text = text
        self.rendered = None
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.background = background
        self.render()
    def render(self):
        self.setSurface(self.font.render(self.text, 0, self.color, self.background))