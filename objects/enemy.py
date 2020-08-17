import OGL
import pywavefront
from OpenGL.GL import *

class BasicEnemy(OGL.Cube):
    def __init__(self,x,y,z):
        OGL.Cube.__init__(self,3,8,2,x,y,z)
        self.model = pywavefront.Wavefront("Handgun_obj.obj","models/")
        self.model.onload = self.onload
        #self.model = OGL.OBJ("Man.obj",Fse,10)
        #self.width = self.model.widthal
        #self.height = self.model.height
        #self.depth = self.model.depth
    def onload(self):

        trigger = self.model.get_mesh("Cube.005_Cube.000")
        trigger.pos[0] = -.3
    def blit(self):
        self.model.draw()