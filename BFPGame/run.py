import sys
from initialize import initialize
import utils
from color import *
import polygon
import gui
import globals
import potentialField

import pygame
from pygame.locals import QUIT


def update_display():
    gameDisplay.fill(WHITE)

    for obj in all_objects:
        obj.draw(gameDisplay)

    if globals.show_bitmap:
        obstacles_bitmap.show_bitmap(gameDisplay)

    pygame.display.update()


def set_mode_drag():
    globals.mode = 'drag'
    # print("SET DRAG")


def set_mode_rotate():
    globals.mode = 'rotate'
    # print("SET ROTATION")

def toggle_show_obstacle_bitmap():
    globals.show_bitmap = not globals.show_bitmap


# init ppygame window
pygame.init()
gameDisplay = pygame.display.set_mode(
    (178*utils.multiplier, 128*utils.multiplier))
pygame.display.set_caption('BFP Demo')

# init variables
running = True
dragging_obj = None
dragging_obj_start_pos = (0, 0)
dragging_obj_start_rotation = 0
dragging_mouse_start_pos = (0, 0)
robots, obstacles = initialize(gameDisplay)
all_objects = set(obstacles)
for r in robots:
    all_objects.add(r.robot_init)
    all_objects.add(r.robot_goal)
all_dragging_objects = set(all_objects)

# BUTTON
# x: 128+200
# Y: 128 = 20*6
# button size: 192, 36
# button space: 200, 40
all_objects.add(gui.Button('DRAGGING MODE', 192, 36,
                utils.world2Canvas((129, 10)), 5, set_mode_drag))
all_objects.add(gui.Button('ROTATING MODE', 192, 36,
                utils.world2Canvas((129, 21)), 5, set_mode_rotate))
all_objects.add(gui.Button('OBSTACLE BITMAP', 192, 36,
                utils.world2Canvas((129, 32)), 5, toggle_show_obstacle_bitmap))



while running:

    # update bitmap
    # constructing bitmap
    obstacles_bitmap = potentialField.PotentialField()
    obstacles_bitmap.mark_obstacles(obstacles)


    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        # Drag & drop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            # print(f"{mousePosition=}")
            # print(f"{utils.canvas2World(mousePosition)=}")
            for polygon in all_dragging_objects:
                if polygon.contain(utils.canvas2World(mousePosition)):
                    dragging_obj_start_pos = polygon.config.position
                    dragging_obj_start_rotation = polygon.config.rotation
                    dragging_mouse_start_pos = mousePosition
                    polygon.set_moving()
                    dragging_obj = polygon
                    break
        elif dragging_obj != None:
            if event.type == pygame.MOUSEBUTTONUP:
                dragging_obj.reset_moving()
                dragging_obj = None

            elif event.type == pygame.MOUSEMOTION:
                mousePosition = pygame.mouse.get_pos()

                if globals.mode == 'drag':
                    movement = utils.formVector(utils.canvas2World(
                        dragging_mouse_start_pos), utils.canvas2World(mousePosition))
                    new_pos = dragging_obj_start_pos[0] + \
                        movement[0], dragging_obj_start_pos[1] + movement[1]
                    dragging_obj.config.set_config(position=new_pos)
                elif globals.mode == 'rotate':
                    new_rotation = utils.mouse2Rotation(
                        dragging_mouse_start_pos, mousePosition, dragging_obj.convex[0].abs_vertices[0]) + dragging_obj_start_rotation
                    dragging_obj.config.set_config(rotation=new_rotation)
                dragging_obj.update_abs_vertices()
                lastMousePosition = mousePosition

    update_display()
