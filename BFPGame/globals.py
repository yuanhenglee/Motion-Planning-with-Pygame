import numpy as np
import utils

mode = 'drag'
show_bitmap = False
pf = None

path_showing_step = 3
show_path = False
path = None

obstacles_bitmap = np.full((128, 128), 254)


robot_dat_path = "Dat/robot1.dat"
obstacle_dat_path = "Dat/obstacle1.dat"