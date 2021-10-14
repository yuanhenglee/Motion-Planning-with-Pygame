import math
from copy import deepcopy
import utils
import pygame
from color import *


class Abstract_Polygon:
    def __init__(self, _n_convex, _convex, _config, _color=BLACK):
        self.n_convex = _n_convex
        self.convex = _convex
        self.config = _config
        self.color = _color
        self.default_color = _color
        self.update_abs_vertices()

    def update_abs_vertices(self):
        for c in self.convex:
            c.abs_vertices = []
            for v in c.vertices:
                x = (v[0] + self.config.position[0])
                y = (v[1] + self.config.position[1])
                x, y = utils.rotate((x, y), self.config.position,
                                    self.config.rotation)
                y = 128 - y
                c.abs_vertices.append((x, y))

    def draw(self, gameDisplay):
        for c in self.convex:
            canvas_vertices = [utils.world2Canvas(v) for v in c.abs_vertices]
            pygame.draw.polygon(gameDisplay, self.color, canvas_vertices)

    def contain(self, point):

        return True

    def set_drag(self):
        self.color = GREEN

    def reset_drag(self):
        self.color = self.default_color

    def __repr__(self):
        return repr(self.convex)


class Robot(Abstract_Polygon):
    def __init__(self, _n_convex, _convex, _initial_config, _goal_config, _n_control_points, _control_points):
        super().__init__(_n_convex, _convex, _initial_config, RED)
        self.initial_config = _initial_config
        self.goal_config = _goal_config
        self.n_control_points = _n_control_points
        self.control_points = _control_points


class Obstacle(Abstract_Polygon):
    def __init__(self, _n_convex, _convex, _config):
        super().__init__(_n_convex, _convex, _config, BLUE)


class Convex:
    def __init__(self, _n_vertices, _vertices):
        self.n_vertices = _n_vertices
        self.vertices = _vertices

    def __repr__(self):
        return repr(self.vertices)


class Config:
    def __init__(self, _position, _rotation):
        self.position = _position
        self.rotation = _rotation

    def __repr__(self):
        return repr(self.position) + " " + repr(self.rotation)
