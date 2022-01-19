from potentialField import get_arbitration_potential
from initialize import initialize
import utils
from color import *
from polygon import * 
import gui
import settings
from potentialField import PotentialField
import numpy as np
from path import Path
import time
import sys
import pygame
import pygame.locals


def update_display():
    gameDisplay.fill(WHITE)

    for obj in all_objects:
        obj.draw(gameDisplay)

    if settings.show_bitmap and settings.pf != None:
        settings.pf.show_bitmap(gameDisplay)

    if settings.show_path and settings.path != None:
        settings.path.show_path(gameDisplay, robots[0].robot_init)


    pygame.display.update()


def set_mode_drag():
    settings.mode = 'drag'
    print("SET DRAG")


def set_mode_rotate():
    settings.mode = 'rotate'
    print("SET ROTATION")

def toggle_drag_rotate():
    if settings.mode == 'drag':
        set_mode_rotate()
    else:
        set_mode_drag()

def set_NF1_PF():
    if settings.show_bitmap:
        settings.show_bitmap = False
        return
    update_PF( "NF1" )
    settings.show_bitmap = not settings.show_bitmap


def set_NF2_PF():
    if settings.show_bitmap:
        settings.show_bitmap = False
        return
    update_PF( "NF2" )
    settings.show_bitmap = not settings.show_bitmap

def update_PF( method = "NF1"):
    # PF timer
    start_time = time.time()

    settings.obstacles_bitmap = utils.new_obstacles_bitmap(obstacles)
    pf1 = PotentialField()
    pf2 = PotentialField()
    if method == "NF1":
        pf1.mark_NF1( robots[0].robot_goal.get_abs_round_point()[0] ) 
        pf2.mark_NF1( robots[0].robot_goal.get_abs_round_point()[1] ) 
    elif method == "NF2":
        pf1.mark_NF2( robots[0].robot_goal.get_abs_round_point()[0] ) 
        pf2.mark_NF2( robots[0].robot_goal.get_abs_round_point()[1] ) 
    settings.pf = pf1 + pf2
    print( method,"PF Time Cost:", time.time() - start_time, "seconds")
    
    return pf1,pf2


def toggle_BFS_path():
    if settings.show_path:
        settings.show_path = False
        return
    caculate_BFS_path()
    settings.show_path = not settings.show_path


def caculate_BFS_path():
    pf1, pf2 = update_PF(method="NF2")

    xinit = robots[0].robot_init.config
    xgoal = robots[0].robot_goal.config
    robot_init = robots[0].robot_init

    # start bfs timer
    start_time = time.time()

    openQ = [[]for i in range(255*2+1)]
    pf_score = int(get_arbitration_potential(robot_init, xinit, pf1, pf2))
    openQ[pf_score] = [xinit]
    # n_openQ = 1
    min_PF_index = pf_score
    T_dict = {xinit: None }
    visited = np.full((128,128,360), False, dtype = bool)
    success = False
    while not success:
        # pop best point from openQ
        if not 0 <= min_PF_index < 255*2 or not openQ[min_PF_index] :
            print("Fail")
            break
        else:
            x = openQ[min_PF_index].pop()
            if not openQ[min_PF_index]:
                while min_PF_index<255*2 and not openQ[min_PF_index]: min_PF_index+=1
        # n_openQ -= 1
        for neighbor in utils.findNeighbors(x):
            neighbor_x = int(neighbor.position[0])
            neighbor_y = int(neighbor.position[1])
            neighbor_r = int(neighbor.rotation)
            pf_score = int(get_arbitration_potential(robot_init, neighbor, pf1, pf2))
            if pf_score < 254*2 and not visited[neighbor_x][neighbor_y][neighbor_r] and not utils.collision_detect( neighbor, robot_init , obstacles ):
                if pf_score < 5 and abs(neighbor_r-xgoal.rotation) < 20:
                    # print(pf_score)
                    # print(neighbor)
                    # print(xgoal)
                    print("Path Found")
                    success = True
                    T_dict[xgoal] = x
                    break
                else:
                    T_dict[neighbor] = x
                    openQ[pf_score].append(neighbor)
                    min_PF_index = min( min_PF_index, pf_score)
                    # n_openQ += 1
                    visited[neighbor_x][neighbor_y][neighbor_r] = True
                # if neighbor == xgoal :
    settings.path = Path()
    settings.path.append(xgoal)
    if success:
        next_point = T_dict[xgoal]
        while next_point!=xinit:
            x = int(next_point.position[0])
            y = int(next_point.position[1])
            settings.path.append(next_point)
            next_point = T_dict[next_point]
    else:
        print( "Path Not Found ...")

    print("BFS Time Cost:", time.time() - start_time, "seconds")


def toggle_animation():
    if settings.show_path:
        settings.show_path = False

    if not settings.path:
        caculate_BFS_path()






# init pygame window
pygame.init()
gameDisplay = pygame.display.set_mode(
    (178*utils.multiplier, 128*utils.multiplier))
pygame.display.set_caption('GRA Demo')

# init variables
try:
    settings.robot_dat_path = sys.argv[1]
    print("load data...", settings.robot_dat_path)
    settings.obstacle_dat_path = sys.argv[2]
    print("load data...", settings.obstacle_dat_path)
except:
    raise Exception("Usage: python3 run.py [robot_dat] [obstacle_dat]")
running = True
dragging_obj = None
dragging_obj_start_pos = (0, 0)
dragging_obj_start_rotation = 0
dragging_mouse_start_pos = (0, 0)
robots, obstacles = initialize()
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
                utils.world2Canvas((129, 54)), 5, toggle_BFS_path))
all_objects.add(gui.Button('Animation', 192, 36,
                utils.world2Canvas((129, 65)), 5, toggle_animation))

clock = pygame.time.Clock()

while running:
    clock.tick(60)
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

                if settings.mode == 'drag':
                    movement = utils.formVector(utils.canvas2World(
                        dragging_mouse_start_pos), utils.canvas2World(mousePosition))
                    new_pos = dragging_obj_start_pos[0] + \
                        movement[0], dragging_obj_start_pos[1] + movement[1]
                    dragging_obj.config.set_config(position=new_pos)
                elif settings.mode == 'rotate':
                    new_rotation = utils.mouse2Rotation(
                        utils.canvas2World(dragging_mouse_start_pos), utils.canvas2World(mousePosition), dragging_obj.center) + dragging_obj_start_rotation
                    center_before_rotate = dragging_obj.center
                    dragging_obj.config.set_config(rotation=new_rotation)
                    dragging_obj.update_abs_vertices()
                    dragging_obj.recenter( center_before_rotate )

                dragging_obj.update_abs_vertices()
                lastMousePosition = mousePosition

        update_display()
