import sys
from initialize import initialize
import utils
from color import *
import polygon

import pygame
from pygame.locals import QUIT


def update_display():
    gameDisplay.fill(WHITE)
    for obj in all_objects:
        obj.draw(gameDisplay)
    pygame.display.update()


pygame.init()
gameDisplay = pygame.display.set_mode(utils.world2Canvas((128, 0)))
running = True
dragging_obj = None
dragging_obj_start_pos = (0, 0)
dragging_mouse_start_pos = (0, 0)

robots, obstacles = initialize(gameDisplay)
all_objects = set(obstacles)
for r in robots:
    all_objects.add(r.robot_init)
    all_objects.add(r.robot_goal)


while running:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        #Drag & drop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            # print(f"{mousePosition=}")
            # print(f"{utils.canvas2World(mousePosition)=}")
            for polygon in all_objects:
                if polygon.contain(utils.canvas2World(mousePosition)):
                    dragging_obj_start_pos = polygon.config.position
                    dragging_mouse_start_pos = mousePosition
                    polygon.set_drag()
                    dragging_obj = polygon
                    break
            # if dragging_obj == None:
            #     for polygon in obstacles:
            #         if polygon.contain(utils.canvas2World(mousePosition)):
            #             dragging_obj_start_pos = polygon.config.position
            #             dragging_mouse_start_pos = mousePosition
            #             polygon.set_drag()
            #             dragging_obj = polygon
            #             break
        elif dragging_obj != None:
            if event.type == pygame.MOUSEBUTTONUP:
                dragging_obj.reset_drag()
                dragging_obj = None

            elif event.type == pygame.MOUSEMOTION:
                mousePosition = pygame.mouse.get_pos()
                movement = utils.formVector(utils.canvas2World(
                    dragging_mouse_start_pos), utils.canvas2World(mousePosition))
                new_pos = dragging_obj_start_pos[0] + \
                    movement[0], dragging_obj_start_pos[1] + movement[1]
                # print(f"{dragging_mouse_start_pos=}{mousePosition=}")
                # print(f"{dragging_obj_start_pos=}{new_pos=}")
                dragging_obj.config.set_config(position=new_pos)
                dragging_obj.update_abs_vertices()
                lastMousePosition = mousePosition

    update_display()
