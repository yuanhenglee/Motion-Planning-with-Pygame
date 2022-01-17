import math
import numpy as np
from numpy.core.numeric import cross
from polygon import *
import copy
import globals

# scale from 128*128 to 4 times bigger
multiplier = 4

# radius resolution
n_angle_seg = 20

# min move step
min_step = 1

# check collision by edge intersection
def collision_detect( config, robot_init, obstacles ) -> bool:
    robot = copy.deepcopy(robot_init)
    robot.config = config
    robot.update_abs_vertices()
    robot_lines = []
    for c in robot.convex:
        for line in c.abs_lines:
            robot_lines.append(line)
    
    for o in obstacles:
        # skip obstacles too far away from robot
        if not rect_bound_overlap( o.rect_bound, robot.rect_bound):
            continue
        for c in o.convex:
            for line in c.abs_lines:
                for r_line in robot_lines:
                    p1, p2 = line
                    p3, p4 = r_line
                    if line_cross( p1, p2, p3, p4 ):
                        # print( "LINE CROSS:", line, r_line)
                        return True
    return False

# check collision by bitmap
# def collision_detect( config, robot_init, obstacles ) -> bool:
#     robot = copy.deepcopy(robot_init)
#     robot.config = config
#     robot.update_abs_vertices()
#     for c in robot.convex:
#         for point in convex_boundaries(c):
#             if globals.obstacles_bitmap[point[0]][point[1]] == 255:
#                 return True
#     return False

def orientation( p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
 
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def line_cross( p1, q1, p2, q2):
    if max(p1[0], q1[0]) < min(p2[0], q2[0]) or max(p2[0], q2[0]) < min(p1[0], q1[0]) or max(p1[1], q1[1]) < min(p2[1], q2[1]) or max(p2[1], q2[1]) < min(p1[1], q1[1]) :
        return False

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
 
    if (o1 != o2 and o3 != o4):
        return True 
 
    if (o1 == 0 and onSegment(p1, p2, q1)): return True
    if (o2 == 0 and onSegment(p1, q2, q1)): return True
    if (o3 == 0 and onSegment(p2, p1, q2)): return True
    if (o4 == 0 and onSegment(p2, q1, q2)): return True
 
    return False

def onSegment( p, q, r ):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
 
    return False 

# def line_cross( p1, p2, p3, p4 ) -> bool:
#     v12 = formVector( p1, p2)
#     v13 = formVector( p1, p3)
#     v14 = formVector( p1, p4)
#     v31 = formVector( p3, p1)
#     v32 = formVector( p3, p2)
#     v34 = formVector( p3, p4)
#     v12_v = rotate90(v12)
#     v34_v = rotate90(v34)
#     return (np.inner(v12_v,v13) * np.inner(v12_v,v14)) < 0\
#         and (np.inner(v34_v,v31) * np.inner(v34_v,v32)) < 0


# def rotate90( vector ):
#     x = -1 * vector[1]
#     y = vector[0]
#     return x,y


def valid_point( p ):
    if 0 <= p[0] < 128 and 0<= p[1] < 128:
        return True
    return False

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
    rotation =  math.degrees(theta)
    # print( f"{v1=} {v2=} {center=} {rotation=}")
    return rotation



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
    d = (max(abs(v1[0]-v2[0]), abs(v1[1]-v2[1])))
    d = round(d*2) if d > 0 else 1 # deal with rounding error
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
    if isinstance( point, Config ):
        x, y = point.position[0], point.position[1]
    else:
        x, y = point[0], point[1]
    if x+min_step < 128:
        neighbors.append((x+min_step, y))
    if x-min_step >= 0:
        neighbors.append((x-min_step, y))
    if y+min_step < 128:
        neighbors.append((x, y+min_step))
    if y-min_step >= 0:
        neighbors.append((x, y-min_step))
    if isinstance( point, Config ):
        neighbors3d = []
        for n in neighbors:
            neighbors3d.append( Config( n, point.rotation ))
        neighbors3d.append( Config( point.position, (point.rotation+360/n_angle_seg)%360 ))
        neighbors3d.append( Config( point.position, (point.rotation-360/n_angle_seg+360)%360 ))
        return neighbors3d
    else:
        return neighbors

def findBestNeighbor( point, distance ):
    bestNeighbor = None
    d = 999
    # print(f"{point=} {distance[point]=}")
    for n in findNeighbors(point):
        if distance[n] < d and distance[n] < distance[point]:
            # print(f"{n=} {distance[n]=}")
            d = distance[n]
            bestNeighbor = n
    return bestNeighbor

def new_obstacles_bitmap( obstacles = [] ):
    obstacles_bitmap = np.full((128, 128), 254)
    if obstacles:
        for obstacle in obstacles:
            for c in obstacle.convex:
                # mark where obstacle are
                for point in convex_boundaries(c):
                    # print(point)
                    obstacles_bitmap[point[0]][point[1]] = 255 
    return obstacles_bitmap

def rect_bound_overlap( rb1:tuple, rb2:tuple )->bool:
    if rb1[0] < rb2[2] or rb1[1] < rb2[3] or rb1[2] > rb2[0] or rb1[3] > rb2[1]:
        return False
    return True

if __name__ == '__main__':
    print(
        line_cross( (0,0), (5,5), (5,0), (2.49,2.5))
    )
