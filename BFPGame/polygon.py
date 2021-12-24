import math
from copy import deepcopy
import utils
import pygame
from color import *
import copy
import numpy as np


class Abstract_Polygon:
    def __init__(self, _n_convex, _convex, _config, _color=BLACK):
        self.n_convex = _n_convex
        self.convex = _convex
        self.config = _config
        self.color = _color
        self.default_color = _color
        self.update_abs_vertices()

    def update_abs_vertices(self):
        max_x = -1
        max_y = -1
        min_x = 129
        min_y = 129
        for c in self.convex:
            c.abs_vertices = []
            for v in c.vertices:
                abs_v = utils.to_abs_pos(self.config, v)
                c.abs_vertices.append(abs_v)
                max_x = max(max_x, abs_v[0])
                max_y = max(max_y, abs_v[1])
                min_x = min(min_x, abs_v[0])
                min_y = min(min_y, abs_v[1])
            c.abs_lines = list(zip(c.abs_vertices[:-1], c.abs_vertices[1:]))
            c.abs_lines.append((c.abs_vertices[-1], c.abs_vertices[0]))
        self.rect_bound = ( max_x, max_y, min_x, min_y )
        self.center = ( (max_x+min_x)/2, (max_y+min_y)/2)

    def draw_skeleton(self, gameDisplay):
        for c in self.convex:
            canvas_vertices = [utils.world2Canvas(v) for v in c.abs_vertices]
            pygame.draw.polygon(gameDisplay, self.color, canvas_vertices, 1)

    def draw(self, gameDisplay):
        for c in self.convex:
            canvas_vertices = [utils.world2Canvas(v) for v in c.abs_vertices]
            pygame.draw.polygon(gameDisplay, self.color, canvas_vertices)

    def contain(self, point):
        for c in self.convex:
            if utils.convexContains(c.abs_vertices, point):
                return True
        return False

    def set_moving(self):
        self.color = greyed_out(self.default_color)

    def reset_moving(self):
        self.color = self.default_color

    def __repr__(self):
        return repr(self.convex)


class Robot():
    def __init__(self, _n_convex, _convex, _initial_config, _goal_config, _n_control_points, _control_points):
        self.robot_init = Robot_init(
            _n_convex, _convex, _initial_config, _n_control_points, _control_points)

        convex_copy = copy.deepcopy(_convex)
        control_points_copy = copy.deepcopy(_control_points)

        self.robot_goal = Robot_goal(
            _n_convex, convex_copy, _goal_config, _n_control_points, control_points_copy)

    def draw(self, gameDisplay):
        self.robot_init.draw(gameDisplay)
        self.robot_goal.draw(gameDisplay)



class Robot_goal(Abstract_Polygon):
    def __init__(self, _n_convex, _convex, _config, _n_control_points, _control_points):
        super().__init__(_n_convex, _convex, _config, YELLOW)
        self.n_control_points = _n_control_points
        self.control_points = _control_points
    
    def get_abs_round_point(self , config = None):
        if config == None:
            config = self.config
        abs_pos_goal = []
        for control_point in self.control_points:
            point = utils.to_abs_pos(config, control_point)
            point = round(point[0]), round(point[1])
            abs_pos_goal.append(point)
        return abs_pos_goal


class Robot_init(Abstract_Polygon):
    def __init__(self, _n_convex, _convex, _config, _n_control_points, _control_points):
        super().__init__(_n_convex, _convex, _config, RED)
        self.n_control_points = _n_control_points
        self.control_points = _control_points
    def get_abs_round_point(self , config = None):
        if config == None:
            config = self.config
        abs_pos_goal = []
        for control_point in self.control_points:
            point = utils.to_abs_pos(config, control_point)
            point = round(point[0]), round(point[1])
            abs_pos_goal.append(point)
        return abs_pos_goal


class Obstacle(Abstract_Polygon):
    def __init__(self, _n_convex, _convex, _config):
        super().__init__(_n_convex, _convex, _config, BLUE)


class Convex:
    def __init__(self, _n_vertices, _vertices):
        self.n_vertices = _n_vertices
        self.vertices = _vertices

    def __repr__(self):
        return repr(self.abs_vertices)


class Config:
    def __init__(self, _position, _rotation):
        self.position = _position
        self.rotation = _rotation

    # def move(self, offset):
    #     self.position = (self.position[0] +
    #                      offset[0], self.position[1] + offset[1])

    def set_config(self, position=None, rotation=None):
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation

    def __repr__(self):
        return repr(self.position) + " " + repr(self.rotation)

    def __add__(self, other):
        position = (self.position[0] + other.position[0],
                    self.position[1] + other.position[1])
        rotation = self.rotation + other.rotation
        return Config(position, rotation)
