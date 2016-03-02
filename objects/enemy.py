import OGL

class BasicEnemy(OGL.ComplexObject):
    def __init__(self,x,y,z):
        OGL.ComplexObject.__init__(self,x,y,z)
        self.body_size = (3,8,2)
        body = OGL.Cube(self.body_size[0],self.body_size[1],self.body_size[2],0,0,0)
        body.setColor(0,0,255)
        body.setFilled(True)
        self.addObject(body,"Body")
        self.head_size = (1,1,1)
        self.head_pos = (0,self.body_size[1]/2+self.head_size[1],0)
        head = OGL.Ellipsoid(self.head_size[0],self.head_size[1],self.head_size[2],self.head_pos[0],self.head_pos[1],self.head_pos[2])
        head.setColor(255,0,0)
        head.setFilled(True)
        head.setQuality(20)
        self.addObject(head,"Head")