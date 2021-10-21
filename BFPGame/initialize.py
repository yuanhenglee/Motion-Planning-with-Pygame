import os
import sys
import pygame
from polygon import *
import utils

# robot_dat_path = "Dat/bfp-data/robot1.dat"
robot_dat_path = "Dat/robot.dat"
# obstacle_dat_path = "Dat/bfp-data/obstacle1.dat"
obstacle_dat_path = "Dat/obstacle.dat"


def loadRobots():
    with open(robot_dat_path) as f:
        f.readline()
        # number of robots
        n_robots = int(f.readline())
        robots = []
        for i in range(n_robots):
            f.readline()
            f.readline()
            # number of convex parts
            n_convex = int(f.readline())
            parts = []
            for j in range(n_convex):
                f.readline()
                f.readline()
                # number of vertices
                n_vertices = int(f.readline())
                f.readline()
                vertices = []
                for k in range(n_vertices):
                    v = f.readline().split(' ')
                    v = (float(v[0]), float(v[1]))
                    vertices.append(v)
                parts.append(Convex(n_vertices, vertices))
            # initial configuraion
            f.readline()
            c = f.readline().split(' ')
            initial_config = Config((float(c[0]), float(c[1])), float(c[2]))
            # goal configuration
            f.readline()
            c = f.readline().split(' ')
            goal_config = Config((float(c[0]), float(c[1])), float(c[2]))
            # number of control points
            f.readline()
            n_control_points = int(f.readline())
            control_points = []
            for j in range(n_control_points):
                f.readline()
                v = f.readline().split(' ')
                v = (float(v[0]), float(v[1]))
                control_points.append(v)
            robots.append(Robot(n_convex, parts, initial_config,
                          goal_config, n_control_points, control_points))
    return robots


def loadObstacle():
    with open(obstacle_dat_path) as f:
        f.readline()
        # number of obstacles
        n_obstacles = int(f.readline())
        obstacles = []
        for i in range(n_obstacles):
            f.readline()
            f.readline()
            # number of convex parts
            n_convex = int(f.readline())
            parts = []
            for j in range(n_convex):
                f.readline()
                f.readline()
                # number of vertices
                n_vertices = int(f.readline())
                f.readline()
                vertices = []
                for k in range(n_vertices):
                    v = f.readline().split(' ')
                    v = (float(v[0]), float(v[1]))
                    vertices.append(v)
                parts.append(Convex(n_vertices, vertices))
            # configuraion
            f.readline()
            c = f.readline().split(' ')
            config = Config((float(c[0]), float(c[1])), float(c[2]))

            obstacles.append(Obstacle(n_convex, parts, config))
    return obstacles


def initialize(gameDisplay):
    robots = loadRobots()
    obstacles = loadObstacle()
    return robots, obstacles


if __name__ == "__main__":
    initialize()
