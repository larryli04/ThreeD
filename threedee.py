import numpy as np
import math

from functions import *

class ThreeDee:

    class Angle:
        def __init__(self, x, y, z):
            self.cameraAngle=np.array([x, y, z])

        def rotate(self, angle): # rotate left on axis using rhr
            self.cameraAngle = np.matmul(zRotationMatrix(angle), self.cameraAngle)
        
        def toString(self):
            return self.cameraAngle
    
    class Pos:
        def __init__(self, x, y, z):
            self.cameraPosX = x
            self.cameraPosY = y
            self.cameraPosZ = z
        
        def toString(self):
            return np.array([self.cameraPosX, self.cameraPosY, self.cameraPosZ])

    def __init__(self):

        self.density = '@%#*+=-:.' # select shading ASCII density
        self.density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,'."

        self.highI=0 # testing variables
        self.lowI=1000
        self.avgI=0
        self.sum=0

        self.high = 320 #90
        self.low = -30 #-7
        self.avg = 18
        self.count=0

        self.renderDistance = 49.5
        self.fov = math.pi/2.0 # 1/3 PI
        self.cameraPos = self.Pos(0.0, -3, 0.0)
        self.cameraAngle = self.Angle(0.0, 1.0, 0.0)
        self.lightPos = self.Pos(0.0, -5.0, 5)

        self.objects = []
        self.output = [ [ "  " for y in range( 40 ) ] for x in range( 40 ) ] # display size 40x40 of blank screen

    def addShape(self, shape):
        self.objects.append(shape)

    def render(self):
        while True:
            self.renderFrame()
            for x in range(0,3): #turn shape on z-axis
                for i in range(0, len(self.objects)):
                    self.objects[i].vertices[x] = np.matmul(zRotationMatrix(np.pi/40),self.objects[i].vertices[x])
                    
    
    def renderFrame(self):
        # for shape in self.objects:
        self.draw() #this draws the frame to self.display
        display(self.output)
        
        self.output = [ [ "  " for y in range( 40 ) ] for x in range( 40 ) ]

    def draw(self):
        step = self.fov/40 # number of pixels

        fovOriginZ = np.matmul(zRotationMatrix(self.fov/2),(normalize(self.cameraAngle.toString())*self.renderDistance)+self.cameraPos.toString()) #multiply sightiline vector with z rotation matrix
        fovOrigin = rotateDown(fovOriginZ,-self.fov/2) #origin is top left... fovOrigin is the starting top left vector and pixel

        for xstep in range(0,40):
            rayVectorZ = np.matmul(zRotationMatrix(-step*xstep),fovOrigin) # rotate the vector horizontally around the z axis

            for ystep in range(0, 40):
                rayVector= rotateDown(rayVectorZ,step*ystep) # rotate vector vertically, but it is trickier so we use the rotateDown function
                shortestIntersection = self.renderDistance # set variable to keep track of the closest intersection that is drawn
                
                for obj in self.objects:
                    collides, intersection = lineTriangleIntersect(obj.vertices, self.cameraPos.toString(), self.cameraPos.toString()+rayVector) # check if the ray hits something
                    if distance(intersection, self.cameraPos.toString()) < shortestIntersection:
                        shortestIntersection = distance(intersection, self.cameraPos.toString()) # update if closer intersection is found
                    else:
                        collides = False # discard drawing if intersection is not the closest
                
                    # calculate shading
                    lightDirection = intersection - self.lightPos.toString()
                    spec = specular(self.cameraAngle.toString(), lightDirection, obj.normal(), 1)
                    diff = diffuse(lightDirection, obj.normal())

                    k1, k2 = .5, .5 # sort of arbitrary

                    # used to calculate the max and min of illumination and normalize the output
                    illumination = spec*k1+diff*k2
                    if(illumination>self.highI):
                        self.highI=illumination
                    if(illumination<self.lowI):
                        self.lowI=illumination
                    self.sum += illumination
                    self.count+=1
                    # self.results()
                
                    if(collides):
                        self.output[xstep][ystep] = 2*self.density[round(((illumination-self.low)/(self.high-self.low))*len(self.density))-2] # linear scaling of pixel density at output pixel
                        pass
                
    def results(self):
        print(self.highI, self.lowI, self.sum/self.count)
                
class Shape:
    def __init__(self, vertices):
        self.vertices = vertices
        self.coor=vertices[0]
    def normal(self):
        line1 = self.vertices[0]-self.vertices[1]
        line2 = self.vertices[1]-self.vertices[2]
        
        return np.cross(line1, line2)

if __name__ == "__main__":

    start = ThreeDee()
    # shape = Shape([np.array([2.5,0,2.5]), np.array([-2.5,0,-2.5]), np.array([-2.5, 0,2.5])])
    # start.addShape(shape)

    # tetrahedron

    start.addShape(Shape([np.array([1.0,1.0,1.0]), np.array([-1.0,-1.0,1.0]), np.array([-1.0,1.0,-1.0])]))
    start.addShape(Shape([np.array([1.0,1.0,1.0]), np.array([1.0,-1.0,-1.0]), np.array([-1.0,1.0,-1.0])]))
    start.addShape(Shape([np.array([1.0,1.0,1.0]), np.array([-1.0,-1.0,1.0]), np.array([1.0,-1.0,-1.0])]))
    start.addShape(Shape([np.array([1.0,-1.0,-1.0]), np.array([-1.0,-1.0,1.0]), np.array([-1.0,1.0,-1.0])]))

    #ICOSAHEDRON BIG
    ϕ=1.618
    # start.addShape(Shape([np.array([0.0, 1.0, ϕ]), np.array([-ϕ, 0.0, 1.0]), np.array([-1.0, ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, +1.0, +ϕ]), np.array([0.0, -1.0, +ϕ]), np.array([-ϕ, 0.0, +1.0])]))
    # start.addShape(Shape([np.array([0.0, +1.0, +ϕ]), np.array([+1.0, +ϕ, 0.0]), np.array([-1.0, +ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, +1.0, +ϕ]), np.array([+ϕ, 0.0, +1.0]), np.array([+1.0, +ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, +1.0, +ϕ]), np.array([0.0, -1.0, +ϕ]), np.array([+ϕ, 0.0, +1.0])]))
    # start.addShape(Shape([np.array([-ϕ, 0.0, +1.0]), np.array([-1.0, +ϕ, 0.0]), np.array([-ϕ, 0.0, -1.0])]))
    # start.addShape(Shape([np.array([-ϕ, 0.0, -1.0]), np.array([-1.0, -ϕ, 0.0]), np.array([-ϕ, 0.0, +1.0])]))
    # start.addShape(Shape([np.array([-ϕ, 0.0, +1.0]), np.array([0.0, -1.0, +ϕ]), np.array([-1.0, -ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, -1.0, +ϕ]), np.array([-1.0, -ϕ, 0.0]), np.array([+1.0, -ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, -1.0, +ϕ]), np.array([+1.0, -ϕ, 0.0]), np.array([+ϕ, 0.0, +1.0])]))
    # start.addShape(Shape([np.array([+ϕ, 0.0, +1.0]), np.array([+1.0, -ϕ, 0.0]), np.array([+ϕ, 0.0, -1.0])]))
    # start.addShape(Shape([np.array([+ϕ, 0.0, +1.0]), np.array([+1.0, +ϕ, 0.0]), np.array([+ϕ, 0.0, -1.0])]))
    # start.addShape(Shape([np.array([+1.0, +ϕ, 0.0]), np.array([+ϕ, 0.0, -1.0]), np.array([0.0, +1.0, -ϕ])]))
    # start.addShape(Shape([np.array([+1.0, +ϕ, 0.0]), np.array([-1.0, +ϕ, 0.0]), np.array([0.0, +1.0, -ϕ])]))
    # start.addShape(Shape([np.array([-1.0, +ϕ, 0.0]), np.array([-ϕ, 0.0, -1.0]), np.array([0.0, +1.0, -ϕ])]))
    # start.addShape(Shape([np.array([0.0, -1.0, -ϕ]), np.array([+1.0, -ϕ, 0.0]), np.array([+ϕ, 0.0, -1.0])]))
    # start.addShape(Shape([np.array([0.0, -1.0, -ϕ]), np.array([+ϕ, 0.0, -1.0]), np.array([0.0, +1.0, -ϕ])]))
    # start.addShape(Shape([np.array([0.0, -1.0, -ϕ]), np.array([0.0, +1.0, -ϕ]), np.array([-ϕ, 0.0, -1.0])]))
    # start.addShape(Shape([np.array([0.0, -1.0, -ϕ]), np.array([-ϕ, 0.0, -1.0]), np.array([-1.0, -ϕ, 0.0])]))
    # start.addShape(Shape([np.array([0.0, -1.0, -ϕ]), np.array([+1.0, -ϕ, 0.0]), np.array([-1.0, -ϕ, 0.0])]))

    print(start.objects)
    start.render()
    
    