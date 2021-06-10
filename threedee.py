import numpy as np
import math

import functions

class ThreeDee:

    def __init__(self, renderDistance, fov, chunk_size):

        self.renderDistance = 10.0
        self.fov = math.pi/3.0
        self.cameraPosX = 0.0
        self.cameraPosY = -5.0
        self.cameraPosZ = 0.0
        self.cameraAngleX = 0.0
        self.cameraAngleY = 1.0
        self.cameraAngleZ = 0.0
        self.renderlist = []
        self.output = [ [ None for y in range( 20 ) ] for x in range( 20 ) ]

    def addShape(self, shape):
        self.renderlist.append(shape)

    def render(self):
        while True:
            self.renderFrame()
            for x in range(0,3): #turn shape on z-axis
                self.renderlist[0].vertices[x] = np.matmul(functions.zRotationMatrix(np.pi/30),self.renderlist[0].vertices[x])

    def renderFrame(self):
        for shape in self.renderlist:
            self.castRay(shape)
        functions.display(self.output)

    def castRay(self, obj):
        step = self.fov/20 # make fov vertical too
        cameraPos = np.array([self.cameraPosX,self.cameraPosY, self.cameraPosZ])
        originFOV = self.fov/2
        fovOriginZ = np.matmul(functions.zRotationMatrix(originFOV),(functions.normalize(np.array([self.cameraAngleX, self.cameraAngleY, self.cameraAngleZ]))*self.renderDistance)+cameraPos)
        fovOrigin = functions.rotateDown(fovOriginZ,-originFOV)

        for xstep in range(0,20):
            rayVectorZ = np.matmul(functions.zRotationMatrix(-step*xstep),fovOrigin)

            for ystep in range(0, 20):
                rayVector= functions.rotateDown(rayVectorZ,step*ystep)
                point = functions.lineTriangleIntersect(obj.vertices, cameraPos, cameraPos+rayVector)
                
                if(point):
                    self.output[xstep][ystep] = "██"
                else:
                    self.output[xstep][ystep] = "  "
    
class Shape:
    def __init__(self, vertices):
        self.vertices = vertices
        
        self.coor=vertices[0]

start = ThreeDee(12, 3.14/2.3, 12)
shape = Shape([np.array([2.5,0.0,2.5]), np.array([-2.5,0.0,-2.5]), np.array([-2.5, 0.0,2.5])])
start.addShape(shape)
start.render()