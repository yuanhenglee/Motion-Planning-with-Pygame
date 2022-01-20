from color import *
import copy
import globVar


class Path(list):
    def show_path(self, gameDisplay):
        for config in self[::globVar.path_showing_step]:
            robot = copy.deepcopy(globVar.movable_robot)
            robot.config = config
            robot.update_abs_vertices()
            robot.draw_skeleton(gameDisplay)

    def show_animation(self, gameDisplay):
        if globVar.animation_count >= len(self):
            globVar.show_animation = False
            globVar.animation_count = 0

        robot = globVar.movable_robot
        robot.config = self[-(globVar.animation_count+1)]
        print(robot.config)
        robot.update_abs_vertices()
        robot.draw(gameDisplay)

        globVar.animation_count += 1
