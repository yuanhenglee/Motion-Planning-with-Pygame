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


def mouse2Rotation(v1, v2, center):
    vector1 = formVector(center, v1)
    vector2 = formVector(center, v2)
    theta = math.atan2(vector2[1], vector2[0]) - \
        math.atan2(vector1[1], vector1[0])
    return math.degrees(theta)


def to_abs_pos(config, vertice):
    x = (vertice[0] + config.position[0])
    y = (vertice[1] + config.position[1])
    x, y = rotate((x, y), config.position, config.rotation)
    return (x, y)
    # form vector from points


def formVector(v1, v2):
    return [v2[0] - v1[0], v2[1] - v1[1]]


def convexContains(vertices, point):
    minX = min(v[0] for v in vertices)
    minY = min(v[1] for v in vertices)
    maxX = max(v[0] for v in vertices)
    maxY = max(v[1] for v in vertices)
    if not(minX < point[0] < maxX and minY < point[1] < maxY):
        return False
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


def fit_grid(v1, v2):
    d = round(max(abs(v1[0]-v2[0]), abs(v1[1]-v2[1])))
    d = d if d > 0 else 1
    d*=2
    dx = (v2[0]-v1[0])/d
    dy = (v2[1]-v1[1])/d
    line = []
    for i in range(d+1):
        x = round(v1[0]+i*dx)
        y = round(v1[1]+i*dy)
        if 0 <= x < 128 and 0 <= y < 128:
            line.append((x, y))
    return line


def convex_boundaries(convex):
    boundaries = set()
    for i in range(1, len(convex.abs_vertices)+1):
        line = fit_grid(convex.abs_vertices[i-1], convex.abs_vertices[i%len(convex.abs_vertices)])
        boundaries.update(line)
    return boundaries

def findNeighbors(point):
    neighbors = []
    x, y = point[0], point[1]
    # for offset_x in range(-1,2):
    #     if 0 <= x + offset_x < 128:
    #         for offset_y in range(-1,2):
    #             if 0 <= y + offset_y < 128 and (offset_x!=0 or offset_y!=0):
    #                 neighbors.append((x+offset_x, y+offset_y))
    if x+1 < 128:
        neighbors.append((x+1, y))
    if x-1 >= 0:
        neighbors.append((x-1, y))
    if y+1 < 128:
        neighbors.append((x, y+1))
    if y-1 >= 0:
        neighbors.append((x, y-1))
    return neighbors




if __name__ == '__main__':
    print(
        fit_grid((1,1), (1,9))
    )
