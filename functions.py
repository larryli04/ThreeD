import numpy as np
import math

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

def zRotationMatrix(theta):
    return np.array([np.array([np.cos(theta),-np.sin(theta),0.0]),np.array([np.sin(theta),np.cos(theta), 0.0]),np.array([0.0,0.0,1.0])])
def yRotationMatrix(theta):
    return np.array([np.array([np.cos(theta),0.0,np.sin(theta)]),np.array([0.0,1.0,0.0]),np.array([-np.sin(theta),0.0,np.cos(theta)])])
def xRotationMatrix(theta):
    return np.array([np.array([1.0,0.0,0.0]),np.array([0.0,np.cos(theta),-np.sin(theta)]),np.array([0.0,np.sin(theta),np.cos(theta)])])

def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):
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

def rotateDown(vector, angle):
    axisVector = normalize(np.cross(np.array([0,0,1]), vector))
    return vector*np.cos(angle) + np.cross(axisVector,vector)*np.sin(angle) + axisVector*np.dot(axisVector,vector)*(1-np.cos(angle))