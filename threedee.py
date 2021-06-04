import numpy as np
import math

def normalize(vector):
    sum = 0
    for component in vector:
        sum += component*component
    v_mag = math.sqrt(sum)
    
    return vector/v_mag
class ThreeDee:

    def __init__(self, renderDistance, fov, chunk_size):

        self.renderDistance = 12
        self.fov = 3.14/2
        self.cameraPosX = 20
        self.cameraPosY = 0
        self.cameraPosZ = 0
        self.cameraAngleX = 0
        self.cameraAngleY = 1
        self.cameraAngleZ = 0
        self.renderlist = []
        
        #world = np.fill((20,20,20), 0)
    def create_square(self):
        #centered at 0, side length of 5
        square = self.Square([[2.5, 2.5], [2.5, -2.5], [-2.5, -2.5], [-2.5, 2.5]])
        self.addShape(square)
    def zRotationMatrix(self, theta):
        return np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta), 0],[0,0,1]])
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

        
    def addShape(self, shape):
        self.renderlist.append(shape)
    def renderFrame(self):
        for shape in self.renderlist:
            self.castRay(shape)
    def pointInShape(self, point, poly):#for convex polygons
        if(poly[0]-point != 0):
            #check all other lines
            for vert in poly:
                pass
    def castRay(self, obj):
        step = self.fov/20 # make fov vertical too
        print(self.zRotationMatrix(-self.fov/2))
        fovOrigin = np.matmul(self.zRotationMatrix(-self.fov/2),np.array([self.cameraAngleX, self.cameraAngleY, self.cameraAngleZ]))
        print(fovOrigin)
        for xstep in range(0,20):
            for ystep in range(0, 20):
                print(self.zRotationMatrix(step*xstep))
                print(fovOrigin)
                print(self.zRotationMatrix(step*xstep)*fovOrigin)
                point = self.LinePlaneCollision(obj.normal, obj.coor, np.matmul(self.zRotationMatrix(step*xstep),fovOrigin), normalize(np.array([self.cameraPosX, self.cameraAngleY, self.cameraAngleZ])))

    
        
    class Square:
        def __init__(self, vertices):
            self.vertices = vertices
            self.normal = normalize(np.cross(vertices[0], vertices[1]))
            self.coor=vertices[0]

start = ThreeDee(12, 3.14/2.3, 12)
square = ThreeDee.Square([[2.5,0,2.5],[2.5,0,-2.5], [-2.5,0,-2.5], [-2.5, 0,2.5]])
#start.normalize(np.array([1, 1, 1]))
start.addShape(square)
start.renderFrame()
