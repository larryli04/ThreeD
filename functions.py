from asyncio.windows_events import NULL
import numpy as np
import math

def normalize(vector):
    sum = 0
    for component in vector:
        sum += component*component
    v_mag = math.sqrt(sum)
    
    return vector/v_mag

def display(display):
    print("frame")
    for y in range(0,40):
        for x in range(0,40):
            print(display[x][y], end="")
            
        print()
    

def magnitude(vector):
    sum = 0
    for x in vector:
        sum+=(x*x)
    
    return math.sqrt(sum)

def specular(viewDirection, lightDirection, surfaceNormal, n):
    v = viewDirection
    r = 2*np.dot(surfaceNormal, lightDirection)*surfaceNormal-lightDirection
    specular = np.dot(v, r)
    return np.power(specular, n)

def diffuse(lightDirection, surfaceNormal):
    return np.dot(lightDirection, surfaceNormal)
    

def lineTriangleIntersect(triangle, linePointA, linePointB, epsilon=1e-6):
    intersection = np.array([NULL, NULL, NULL])
    
    linePointA[linePointA==0]=epsilon # if any element is 0, replace it with epsilon THIS IS A QUIRK OF NUMPY AND NOT PYTHON LISTS
    linePointB[linePointB==0]=epsilon # epsilon is used because dividing by zero is bad
    
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
        return False, intersection
    
    f = 1.0 / a

    s = linePointA - triPoint0
    u = f * np.dot(s, h)
    if (u<0.0 or u>1.0):
        return False, intersection
    q = np.cross(s, edge1)
    v = f * np.dot(rayVector, q)
    if (v<0.0 or u+v>1.0):
        return False, intersection
    t = f * np.dot(edge2,q)
    if t>epsilon:
        
        intersection = linePointA + rayVector * t

        return True, intersection
    else:
        return False, intersection





def zRotationMatrix(theta):
    return np.array([np.array([np.cos(theta),-np.sin(theta),0.0]),np.array([np.sin(theta),np.cos(theta), 0.0]),np.array([0.0,0.0,1.0])])
def yRotationMatrix(theta):
    return np.array([np.array([np.cos(theta),0.0,np.sin(theta)]),np.array([0.0,1.0,0.0]),np.array([-np.sin(theta),0.0,np.cos(theta)])])
def xRotationMatrix(theta):
    return np.array([np.array([1.0,0.0,0.0]),np.array([0.0,np.cos(theta),-np.sin(theta)]),np.array([0.0,np.sin(theta),np.cos(theta)])])

def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6): # deprecated
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

def distance(a, b):
    return np.sqrt(np.sum(np.power(a-b, 2)))

if __name__ == "__main__":
    print(distance(np.array([0,0,0]), np.array([1,1,1])))
    