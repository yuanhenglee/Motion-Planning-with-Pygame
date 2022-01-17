import pygame
from color import *
import utils
import copy
import settings

class Path(list):
    def show_path(self, gameDisplay, robot_init ):
        for config in self[::settings.path_showing_step]:
            color = RED
            robot = copy.deepcopy(robot_init)
            robot.config = config
            robot.update_abs_vertices()
            robot.draw_skeleton( gameDisplay )

            x, y = utils.world2Canvas(config.position)
            pygame.draw.rect(gameDisplay, color, [x, y, utils.multiplier, utils.multiplier])