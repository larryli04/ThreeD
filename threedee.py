import numpy as np
import math
import os

def normalize(vector):
    sum = 0
    for component in vector:
        sum += component*component
    v_mag = math.sqrt(sum)
    
    return vector/v_mag


def display(display):
    for y in range(0,20):
        for x in range(0,20):
            print(display[x][y], end="")
        print()

def magnitude(vector):
    sum = 0
    for x in vector:
        sum+=(x*x)
    
    return math.sqrt(sum)

def lineTriangleIntersect(triangle, linePointA, linePointB, epsilon=1e-6):

    linePointA[linePointA==0]=epsilon
    linePointB[linePointB==0]=epsilon
    
    rayVector = linePointB-linePointA
    
    
    triPoint0 = triangle[0]
    triPoint1 = triangle[1]
    triPoint2 = triangle[2]
    triPoint0[triPoint0==0]=epsilon
    triPoint1[triPoint1==0]=epsilon
    triPoint2[triPoint2==0]=epsilon

    edge1 = triPoint1-triPoint0
    edge2 = triPoint2-triPoint0

    h = np.cross(rayVector, edge2)
    a = np.dot(edge1, h)

    if(a>epsilon) and (a<epsilon):
        return False
    
    f = 1.0 / a

    s = linePointA - triPoint0
    u = f * np.dot(s, h)
    if (u<0.0 or u>1.0):
        return False
    q = np.cross(s, edge1)
    v = f * np.dot(rayVector, q)
    if (v<0.0 or u+v>1.0):
        return False
    t = f * np.dot(edge2,q)
    if t>epsilon:
        intersection = linePointA + rayVector * t

        return True
    else:
        return False
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


    def zRotationMatrix(self, theta):
        return np.array([np.array([np.cos(theta),-np.sin(theta),0.0]),np.array([np.sin(theta),np.cos(theta), 0.0]),np.array([0.0,0.0,1.0])])
    def yRotationMatrix(self, theta):
        return np.array([np.array([np.cos(theta),0.0,np.sin(theta)]),np.array([0.0,1.0,0.0]),np.array([-np.sin(theta),0.0,np.cos(theta)])])
    def xRotationMatrix(self, theta):
        return np.array([np.array([1.0,0.0,0.0]),np.array([0.0,np.cos(theta),-np.sin(theta)]),np.array([0.0,np.sin(theta),np.cos(theta)])])
    def LinePlaneCollision(self, planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):
        print("planeNormal", planeNormal, "planePoint:", planePoint, "rayDirection:",rayDirection, "rayPoint:",rayPoint)
        ndotu = planeNormal.dot(rayDirection)
        print("ndotu")
        print(ndotu)
        if abs(ndotu) < epsilon:
            raise RuntimeError("no intersection or line is within plane")

        w = rayPoint - planePoint
        print(w)
        si = -planeNormal.dot(w) / ndotu
        print(si)
        Psi = w + si * rayDirection + planePoint
        return Psi

    def rotateDown(self, vector, angle):
        axisVector = normalize(np.cross(np.array([0,0,1]), vector))
        return vector*np.cos(angle) + np.cross(axisVector,vector)*np.sin(angle) + axisVector*np.dot(axisVector,vector)*(1-np.cos(angle))
    def addShape(self, shape):
        self.renderlist.append(shape)
    def render(self):
        while True:
            self.renderFrame()
            for x in range(0,3):
                self.renderlist[0].vertices[x] = np.matmul(self.zRotationMatrix(np.pi/30),self.renderlist[0].vertices[x])
    def renderFrame(self):
        for shape in self.renderlist:
            self.castRay(shape)
        display(self.output)

    def castRay(self, obj):

        step = self.fov/20 # make fov vertical too
        cameraPos = np.array([self.cameraPosX,self.cameraPosY, self.cameraPosZ])
        originFOV = self.fov/2
        fovOriginZ = np.matmul(self.zRotationMatrix(originFOV),(normalize(np.array([self.cameraAngleX, self.cameraAngleY, self.cameraAngleZ]))*self.renderDistance)+cameraPos)
        fovOrigin = self.rotateDown(fovOriginZ,-originFOV)

        for xstep in range(0,20):

            rayVectorZ = np.matmul(self.zRotationMatrix(-step*xstep),fovOrigin)

            for ystep in range(0, 20):

                rayVector= self.rotateDown(rayVectorZ,step*ystep)
                point = lineTriangleIntersect(obj.vertices, cameraPos, cameraPos+rayVector)
                
                if(point):
                    self.output[xstep][ystep] = "██"
                else:
                    self.output[xstep][ystep] = "  "
    
    class Square:
        def __init__(self, vertices):
            self.vertices = vertices
            #self.normal = normalize(np.cross(vertices[0], vertices[1]))
            self.coor=vertices[0]

start = ThreeDee(12, 3.14/2.3, 12)
square = ThreeDee.Square([np.array([2.5,0.0,2.5]), np.array([-2.5,0.0,-2.5]), np.array([-2.5, 0.0,2.5])])
start.addShape(square)
start.render()