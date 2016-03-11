import OGL
import pywavefront

class BasicEnemy(OGL.Cube):
    def __init__(self,x,y,z):
        OGL.Cube.__init__(self,3,8,2,x,y,z)
        self.model = pywavefront.Wavefront("Rock.obj","models/",10)
        #self.model = OGL.OBJ("Man.obj",Fse,10)
        #self.width = self.model.widthal
        #self.height = self.model.height
        #self.depth = self.model.depth

    def blit(self):
        self.model.draw()
        #if self.model.loaded:
        #    self.model.pos[1] = 0
        #self.model.blit()