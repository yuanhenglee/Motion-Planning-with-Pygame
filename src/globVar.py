import numpy as np

# state
mode = 'drag'
show_bitmap = False
show_path = False
show_animation = False

# global variables
pf = None
path = None
obstacles_bitmap = np.full((128, 128), 254)
animation_count = 0
movable_robot = None
robot_dat_path = "Dat/robot1.dat"
obstacle_dat_path = "Dat/obstacle1.dat"

# config
path_showing_step = 2
