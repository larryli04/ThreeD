import numpy as np


import functions

class ThreeDee:

    def __init__(self, renderDistance, fov, res):
        self.res = res
        self.renderDistance = renderDistance
        self.fov = fov
        self.cameraPosX = 0.0
        self.cameraPosY = -10.0
        self.cameraPosZ = 0.0
        self.cameraAngleX = 0.0
        self.cameraAngleY = 1.0
        self.cameraAngleZ = 0.0
        self.renderlist = []
        self.output = [ [ "  " for y in range( self.res ) ] for x in range( self.res ) ]

    def addComplex(self,shape):
        for x in range(len(shape.triangles)):
            self.addShape(shape.triangles[x])

    def addShape(self, shape):
        self.renderlist.append(shape)

    def render(self):
        while True:
            self.renderFrame()
            self.output = [ [ "  " for y in range( self.res ) ] for x in range( self.res ) ]
    def renderFrame(self):
        for shape in self.renderlist:
            self.castRay(shape)
            for x in range(0,3): #turn shape on z-axis
                shape.vertices[x] = np.matmul(functions.zRotationMatrix(np.pi/20),shape.vertices[x])
        functions.display(self.output, self.res)

    def castRay(self, obj):
    
        step = self.fov/self.res # make fov vertical too
        cameraPos = np.array([self.cameraPosX,self.cameraPosY, self.cameraPosZ])
        originFOV = self.fov/2
        fovOriginZ = np.matmul(functions.zRotationMatrix(originFOV),(functions.normalize(np.array([self.cameraAngleX, self.cameraAngleY, self.cameraAngleZ]))*self.renderDistance)+cameraPos)
        fovOrigin = functions.rotateDown(fovOriginZ,-originFOV)

        for xstep in range(0,self.res):
            rayVectorZ = np.matmul(functions.zRotationMatrix(-step*xstep),fovOrigin)

            for ystep in range(0, self.res):
                rayVector= functions.rotateDown(rayVectorZ,step*ystep)
                point = functions.lineTriangleIntersect(obj.vertices, cameraPos, cameraPos+rayVector)
                
                if(point):
                    self.output[xstep][ystep] = "██"
                
    
class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices
        
        self.coor=vertices[0]
class Cube:
    def __init__(self, diagonal): # [2.5,2.5,2.5] [2.5,-2.5,-2.5]
        self.drad = diagonal/2
        self.triangles=[]
        #front
        self.triangles.append(Triangle([np.array([self.drad,self.drad,self.drad]), np.array([self.drad,-self.drad,self.drad]), np.array([self.drad, -self.drad,-self.drad])]))
        self.triangles.append(Triangle([np.array([self.drad,self.drad,self.drad]), np.array([self.drad,self.drad,-self.drad]), np.array([self.drad, -self.drad,-self.drad])]))
        #back
        self.triangles.append(Triangle([np.array([-self.drad,self.drad,self.drad]), np.array([-self.drad,-self.drad,self.drad]), np.array([-self.drad, -self.drad,-self.drad])]))
        self.triangles.append(Triangle([np.array([-self.drad,self.drad,self.drad]), np.array([-self.drad,self.drad,-self.drad]), np.array([-self.drad, -self.drad,-self.drad])]))
        #left
        self.triangles.append(Triangle([np.array([self.drad,-self.drad,self.drad]), np.array([-self.drad,-self.drad,self.drad]), np.array([-self.drad, -self.drad,-self.drad])]))
        self.triangles.append(Triangle([np.array([self.drad,-self.drad,self.drad]), np.array([self.drad,-self.drad,-self.drad]), np.array([-self.drad, -self.drad,-self.drad])]))

        #finish rest of the sides



start = ThreeDee(15.0, np.pi/3, 50)
cube = Cube(5)
start.addComplex(cube)
start.render()