import OGL

class BasicEnemy(OGL.Cube):
    def __init__(self,x,y,z):
        OGL.Cube.__init__(self,3,8,2,x,y,z)
        self.model = OGL.OBJ("Man.obj",False,10)
        self.width = self.model.width
        self.height = self.model.height
        self.depth = self.model.depth
    def blit(self):
        if self.model.loaded:
            self.model.pos[1] = 0
        self.model.blit()