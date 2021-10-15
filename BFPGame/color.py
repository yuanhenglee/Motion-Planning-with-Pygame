def greyed_out(color):
    l = list(color)
    for i in range(len(l)):
        if l[i] < 128:
            l[i] = 128
    return tuple(l)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
