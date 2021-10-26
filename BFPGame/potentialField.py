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
                    self.bitmap[point[0]][point[1]] = 255 

    def show_bitmap(self, gameDisplay):
        for i in range(128):
            for j in range(128):
                color = 255 - self.bitmap[i][j]
                color = 0 if color<0 else color
                color = (color, color, color)
                x, y = utils.world2Canvas((i, j))
                pygame.draw.rect(gameDisplay, color, [x, y, utils.multiplier, utils.multiplier])

    def mark_NF1(self, robot_goal ):
        # mark destination
        cost = 0.5
        abs_pos_goal = []
        for control_point in robot_goal.control_points:
            point = utils.to_abs_pos(robot_goal.config, control_point)
            point = round(point[0]), round(point[1])
            abs_pos_goal.append(point)
            self.bitmap[point[0]][point[1]] = 0

            # BFS from goal
            l_configs = {0:[point]}
            # for i, Li in l_configs.items():
            i = 0
            while True:
                if i not in l_configs:
                    break

                Li = l_configs[i]
                for q in Li:
                    for neighbor in utils.findNeighbors(q):
                        if self.bitmap[neighbor[0]][neighbor[1]] == 254:
                            self.bitmap[neighbor[0]][neighbor[1]] = i+cost
                            if i+cost in l_configs:
                                l_configs[i+cost].append(neighbor)
                            else:
                                l_configs[i+cost] = [neighbor]
                i+=cost



    