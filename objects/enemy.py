import OGL

class BasicEnemy(OGL.Cube):
    def __init__(self,x,y,z):
        OGL.Cube.__init__(self,3,8,2,x,y,z)
        self.model = OGL.OBJ("Man.obj",False,10)
        """self.model.getGroup("Object001").name = "Head"
        self.model.getGroup("Object002").name = "Body"
        self.model.getGroup("Object003").name = "Left arm"
        self.model.getGroup("Object004").name = "Right arm"
        self.model.getGroup("Object005").name = "Left hand"
        self.model.getGroup("Object006").name = "Right hand"
        self.model.getGroup("Object008").name = "Left leg"
        self.model.getGroup("Object009").name = "Right leg"
        self.model.getGroup("Object013").name = "Eyes"
        self.model.getGroup("Object019").name = "Left leg shit"
        self.model.getGroup("Object020").name = "Right leg shit"
        self.model.getGroup("Object021").name = "Both boots"
        """
        self.width = self.model.width
        self.height = self.model.height
        self.depth = self.model.depth
        #self.model.getGroup("Left arm").anglex = 180
    def blit(self):
        self.model.pos[1] = 0
        self.model.blit()