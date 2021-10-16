import utils
import numpy as np


class PotentialField:
    def __init__(self):
        self.bitmap = [[0 for x in range(128)] for y in range(128)]

    def mark_obstacles(self, obstacles):
        for obstacle in obstacles:
            for c in obstacle.convex:
                # mark where obstacle are
                for point in utils.convex_boundaries(c):
                    self.bitmap[point[0]][point[1]] = 255

    # def show_bitmap(self):
        # np_bitmap = np.array(self.bitmap)
        # fig = plt.figure()
        # axe = fig.add_subplot()

        # # 生成隨機資料
        # data = np.random.randn(100).cumsum()

        # # 以 seaborn 呈現
        # sns.heatmap(data=np_bitmap)
        # plt.show()


obstacles_bitmap = PotentialField()
