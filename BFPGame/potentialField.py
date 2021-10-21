import utils
import pygame


class PotentialField:
    def __init__(self):
        self.bitmap = [[254 for x in range(128)] for y in range(128)]

    def mark_obstacles(self, obstacles):
        for obstacle in obstacles:
            for c in obstacle.convex:
                # mark where obstacle are
                for point in utils.convex_boundaries(c):
                    self.bitmap[point[0]][point[1]] = 0 # tmp

    def show_bitmap(self, gameDisplay):
        for i in range(128):
            for j in range(128):
                color = self.bitmap[i][j]
                color = (color, color, color)
                x, y = utils.world2Canvas((i, j))
                pygame.draw.rect(gameDisplay, color, [x, y, utils.multiplier, utils.multiplier], 1)

    def mark_NF1(self):
        ...
        
