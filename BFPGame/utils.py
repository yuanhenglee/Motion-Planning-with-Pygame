import math
s


# scale from 128*128 to 6 times bigger
multiplier = 4


def world2Canvas(vertex):
    return round(vertex[0]*multiplier), round(vertex[1]*multiplier)


def canvas2World(vertex):
    return (vertex[0]/multiplier), (vertex[1]/multiplier)


def distance(v1, v2):
    return math.hypot(v1[0]-v2[0], v1[1]-v2[1])


def rotate(v, center=(0, 0), degree=0):
    angle = math.radians(degree)
    xr = math.cos(angle)*(v[0]-center[0]) - \
        math.sin(angle)*(v[1]-center[1]) + center[0]
    yr = math.sin(angle)*(v[0]-center[0]) + \
        math.cos(angle)*(v[1]-center[1]) + center[1]
    return xr, yr


def convexContains(vertices, point):


if __name__ == '__main__':
    print(rotate((1, 1), (0, 0), 45))
