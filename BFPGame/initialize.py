import os
import sys
import pygame
from polygon import *
import utils
import globals


def loadRobots():
    file_lines_cleaned = []
    with open(globals.robot_dat_path) as f:
        file_lines = f.readlines()
        for l in file_lines:
            if l != '\n' and l[0] != '#':
                file_lines_cleaned.append(l.rstrip("\n"))
    # print(file_lines_cleaned)

    n_robots = int(file_lines_cleaned[0])
    robots = []
    index = 1
    for i in range(n_robots):
        n_convex = int(file_lines_cleaned[index])
        index += 1
        parts = []
        for j in range( n_convex ):
            n_vertices = int(file_lines_cleaned[index])
            index += 1
            vertices = []
            for k in range(n_vertices):
                v = file_lines_cleaned[index].split(' ')
                index += 1
                vertices.append((float(v[0]),float(v[1])))
            parts.append(Convex(n_vertices, vertices))
        c = file_lines_cleaned[index].split(' ')
        initial_config = Config((float(c[0]), float(c[1])), float(c[2]))
        index += 1
        # goal configuration
        c = file_lines_cleaned[index].split(' ')
        goal_config = Config((float(c[0]), float(c[1])), float(c[2]))
        index += 1
        # number of control points
        n_control_points = int(file_lines_cleaned[index])
        index += 1
        control_points = []
        for _ in range(n_control_points):
            v = file_lines_cleaned[index].split(' ')
            v = (float(v[0]), float(v[1]))
            control_points.append(v)
            index += 1
        robots.append(Robot(n_convex, parts, initial_config,
                        goal_config, n_control_points, control_points))
    return robots

def loadObstacle():
    file_lines_cleaned = []
    with open(globals.obstacle_dat_path) as f:
        file_lines = f.readlines()
        for l in file_lines:
            if l != '\n' and l[0] != '#':
                file_lines_cleaned.append(l.rstrip("\n"))
    # print(file_lines_cleaned)

    n_obstacles= int(file_lines_cleaned[0])
    obstacles = []
    index = 1
    for i in range(n_obstacles):
        n_convex = int(file_lines_cleaned[index])
        index += 1
        parts = []
        for j in range( n_convex ):
            n_vertices = int(file_lines_cleaned[index])
            index += 1
            vertices = []
            for k in range(n_vertices):
                v = file_lines_cleaned[index].split(' ')
                index += 1
                vertices.append((float(v[0]),float(v[1])))
            parts.append(Convex(n_vertices, vertices))
        c = file_lines_cleaned[index].split(' ')
        config = Config((float(c[0]), float(c[1])), float(c[2]))
        index += 1
        obstacles.append(Obstacle(n_convex, parts, config))
    return obstacles 

def initialize():
    robots = loadRobots()
    obstacles = loadObstacle()
    return robots, obstacles


if __name__ == "__main__":
    initialize()
