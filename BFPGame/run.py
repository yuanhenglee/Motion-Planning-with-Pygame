from initialize import initialize
import utils
from color import *
import polygon
import gui
import globals
from potentialField import PotentialField

import pygame
from pygame.locals import QUIT


def update_display():
    gameDisplay.fill(WHITE)

    for obj in all_objects:
        obj.draw(gameDisplay)

    if globals.show_bitmap and globals.pf != None:
        globals.pf.show_bitmap(gameDisplay)

    pygame.display.update()


def set_mode_drag():
    globals.mode = 'drag'
    print("SET DRAG")


def set_mode_rotate():
    globals.mode = 'rotate'
    print("SET ROTATION")

def toggle_drag_rotate():
    if globals.mode == 'drag':
        set_mode_rotate()
    else:
        set_mode_drag()

def set_NF1_PF(BFS = False):
    globals.obstacles_bitmap = utils.new_obstacles_bitmap( obstacles )
    pf1 = PotentialField()
    pf2 = PotentialField() 
    pf1.mark_NF1( robots[0].robot_goal.get_abs_round_point()[0] ) 
    pf2.mark_NF1( robots[0].robot_goal.get_abs_round_point()[1] ) 
    if BFS:
        pf1.BFS( robots[0].robot_init.get_abs_round_point()[0], robots[0].robot_goal.get_abs_round_point()[0]  )
        pf1.BFS( robots[0].robot_init.get_abs_round_point()[0], robots[0].robot_goal.get_abs_round_point()[0]  )
    globals.pf = pf1 + pf2
    globals.show_bitmap = not globals.show_bitmap

def set_NF2_PF(BFS = False):
    globals.obstacles_bitmap = utils.new_obstacles_bitmap( obstacles )
    pf1 = PotentialField()
    pf2 = PotentialField() 
    pf1.mark_NF2( robots[0].robot_goal.get_abs_round_point()[0] ) 
    pf2.mark_NF2( robots[0].robot_goal.get_abs_round_point()[1] ) 
    if BFS:
        pf1.BFS( robots[0].robot_init.get_abs_round_point()[0], robots[0].robot_goal.get_abs_round_point()[0]  )
        pf2.BFS( robots[0].robot_init.get_abs_round_point()[1], robots[0].robot_goal.get_abs_round_point()[1] ) 
    globals.pf = pf1 + pf2
    globals.show_bitmap = not globals.show_bitmap

def set_BFS_PF():
    # globals.pf.BFS( robots[0].robot_init, robots[0].robot_goal ) 
    # globals.show_bitmap = not globals.show_bitmap
    set_NF1_PF(BFS=True)

# init pygame window
pygame.init()
gameDisplay = pygame.display.set_mode(
    (178*utils.multiplier, 128*utils.multiplier))
pygame.display.set_caption('GRA Demo')

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
all_objects.add(gui.Button('Toggle Drag/Rotate', 192, 36,
                utils.world2Canvas((129, 10)), 5, toggle_drag_rotate))
all_objects.add(gui.Button('Show NF1 PF', 192, 36,
                utils.world2Canvas((129, 32)), 5, set_NF1_PF))
all_objects.add(gui.Button('Show NF2 PF', 192, 36,
                utils.world2Canvas((129, 43)), 5, set_NF2_PF))
all_objects.add(gui.Button('Show BFS Path', 192, 36,
                utils.world2Canvas((129, 54)), 5, set_BFS_PF))



while running:

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        # Drag & drop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            # print(f"{mousePosition=}")
            print(f"mouse click: {utils.canvas2World(mousePosition)}")
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
