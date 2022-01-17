import utils
import pygame
import copy
import numpy as np
from color import *
import globals

cost = 1

def get_arbitration_potential( robot_init, config, pf1, pf2 ) -> float :
    control_points_pos = robot_init.get_abs_round_point( config = config )
    p1 = control_points_pos[0]
    p2 = control_points_pos[1]
    if not utils.valid_point(p1) or not utils.valid_point(p2):
        potential_val = 255*2
    # elif utils.collision_detect( config, robot_init ):
    #     potential_val = 255*2
    else:
        potential_val = pf1.get_potential_val(p1) + pf2.get_potential_val(p2)

    return potential_val


class PotentialField:
    def __init__(self):
        self.bitmap = np.full((128, 128), 0)

    def get_potential_val(self, point):
        return self.bitmap[point[0]][point[1]]

    def show_bitmap(self, gameDisplay):
        for i in range(128):
            for j in range(128):
                color = 255 - self.bitmap[i][j]
                color = 0 if color < 0 else color
                if color > 255:
                    color = RED
                else:
                    color = (color, color, color)
                x, y = utils.world2Canvas((i, j))
                pygame.draw.rect(gameDisplay, color, [
                                 x, y, utils.multiplier, utils.multiplier])

    def BFS(self, xinit, xgoal):
        openQ = [[]for i in range(256)]
        pf_score = int(self.bitmap[xinit[0]][xinit[1]])
        openQ[pf_score] = [xinit]
        n_openQ = 1
        min_PF_index = pf_score
        T_dict = {xinit: None}
        visited = np.full((128, 128), False, dtype=bool)
        success = False
        while n_openQ > 0 and not success:
            # pop best point from openQ
            x = openQ[min_PF_index].pop()
            n_openQ -= 1
            for neighbor in utils.findNeighbors(x):
                pf_score = int(self.bitmap[neighbor[0]][neighbor[1]])
                if pf_score < 254 and not visited[neighbor[0]][neighbor[1]]:
                    T_dict[neighbor] = x
                    openQ[pf_score].append(neighbor)
                    min_PF_index = min(min_PF_index, pf_score)
                    n_openQ += 1
                    visited[neighbor[0]][neighbor[1]] = True
                    if neighbor == xgoal:
                        print("Path Found")
                        success = True
        if success:
            next_point = T_dict[xgoal]
            while next_point != xinit:
                self.bitmap[next_point[0]][next_point[1]] = 0
                next_point = T_dict[next_point]
        else:
            print("Path Not Found ...")

    def mark_NF1(self, goal):
        bitmap = copy.deepcopy(globals.obstacles_bitmap)
        bitmap[goal[0]][goal[1]] = 0

        # BFS from goal
        l_configs = {0: [goal]}
        # for i, Li in l_configs.items():
        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if bitmap[neighbor[0]][neighbor[1]] == 254:
                        # prevent bimap excess 255
                        if i+cost > 255:
                            bitmap[neighbor[0]][neighbor[1]] = 255
                        else:
                            bitmap[neighbor[0]][neighbor[1]] = i+cost
                        if i+cost in l_configs:
                            l_configs[i+cost].append(neighbor)
                        else:
                            l_configs[i+cost] = [neighbor]
            i += cost
        self.bitmap += bitmap

    def mark_NF2(self, goal):
        # edge init
        distance = np.full((128, 128), 254)
        origin = {}
        l_configs = {0: []}
        S = set()
        for i in range(128):
            for j in range(128):
                if globals.obstacles_bitmap[i][j] == 255 or i == 0 or i == 127 or j == 0 or j == 127:
                    for neighbor in utils.findNeighbors((i, j)):
                        if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254:
                            distance[i][j] = 0
                            origin[(i, j)] = (i, j)
                            l_configs[0].append((i, j))
                            break

        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254:
                        if distance[neighbor[0]][neighbor[1]] == 254:
                            distance[neighbor[0]][neighbor[1]] = i+cost
                            origin[neighbor] = origin[q]
                            if i+cost in l_configs:
                                l_configs[i+cost].append(neighbor)
                            else:
                                l_configs[i+cost] = [neighbor]
                        elif utils.distance(origin[neighbor], origin[q]) > 5 and q not in S:
                            S.add(neighbor)
            i += cost

        bitmap = np.full((128, 128), 254)
        Sigma = set([goal])
        l_configs = {0: []}
        q = goal

        while q not in S:
            q_prime = utils.findBestNeighbor(q, distance)
            if q_prime == None:
                break
            Sigma.add(q_prime)
            q = q_prime
            # print(f"{q=} {distance[q[0]][q[1]]=}")
            # bitmap[q] = 0
        S = S.union(Sigma)

        bitmap[goal[0]][goal[1]] = 0
        Q = [goal]
        while len(Q) > 0:
            q = Q.pop(0)
            l_configs[0].append(q)
            for neighbor in utils.findNeighbors(q):
                if neighbor in S and bitmap[neighbor[0]][neighbor[1]] == 254:
                    bitmap[neighbor[0]][neighbor[1]] = 0
                    # bitmap[neighbor[0]][neighbor[1]] = bitmap[q[0]][q[1]] + 1
                    Q.append(neighbor)

        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254 and bitmap[neighbor[0]][neighbor[1]] == 254:
                        bitmap[neighbor[0]][neighbor[1]
                                            ] = bitmap[q[0]][q[1]] + 1
                        if i+cost in l_configs:
                            l_configs[i+cost].append(neighbor)
                        else:
                            l_configs[i+cost] = [neighbor]
            i += cost

        self.bitmap = bitmap

    def __add__(self, o):
        new_pf = PotentialField()
        new_pf.bitmap = (self.bitmap + o.bitmap)/2
        return new_pf
