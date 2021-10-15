import math
import numpy as np
from numpy.core.numeric import cross


# scale from 128*128 to 6 times bigger
multiplier = 4


def world2Canvas(vertex):
    return round(vertex[0]*multiplier), round((128-vertex[1])*multiplier)


def canvas2World(vertex):
    return (vertex[0]/multiplier), (128-vertex[1]/multiplier)


def distance(v1, v2):
    return math.hypot(v1[0]-v2[0], v1[1]-v2[1])


def rotate(v, center=(0, 0), degree=0):
    angle = math.radians(degree)
    xr = math.cos(angle)*(v[0]-center[0]) - \
        math.sin(angle)*(v[1]-center[1]) + center[0]
    yr = math.sin(angle)*(v[0]-center[0]) + \
        math.cos(angle)*(v[1]-center[1]) + center[1]
    return xr, yr

# form vector from points


def formVector(v1, v2):
    return [v2[0] - v1[0], v2[1] - v1[1]]


def convexContains(vertices, point):
    crossProduct = np.cross(formVector(
        vertices[-1], vertices[0]), formVector(vertices[-1], point))
    for i in range(1, len(vertices)):
        nextCrossProduct = np.cross(formVector(
            vertices[i-1], vertices[i]),
            formVector(vertices[i-1], point))
        if (crossProduct * nextCrossProduct < 0):
            return False
    # print(f"{point=}")
    # print(f"{vertices=}")
    return True


if __name__ == '__main__':
    print(
        convexContains([(0, 0), (5, 0), (5, 5), (0, 5)], (1, 6))
    )
