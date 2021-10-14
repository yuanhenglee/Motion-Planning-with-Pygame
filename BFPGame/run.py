import sys
from initialize import initialize
import utils
from color import *

import pygame
from pygame.locals import QUIT


def sample():
    pygame.init()
    # 建立 window 視窗畫布，大小為 800x600
    window_surface = pygame.display.set_mode((800, 600))
    # 設置視窗標題為 Hello World:)
    pygame.display.set_caption('Hello World:)')
    # 清除畫面並填滿背景色
    window_surface.fill((255, 255, 255))

    # 宣告 font 文字物件
    head_font = pygame.font.SysFont(None, 60)
    # 渲染方法會回傳 surface 物件
    text_surface = head_font.render('Hello World!', True, (0, 0, 0))
    # blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗
    window_surface.blit(text_surface, (10, 10))

    # 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現）
    pygame.display.update()

    # 事件迴圈監聽事件，進行事件處理
    while True:
        # 迭代整個事件迴圈，若有符合事件則對應處理
        for event in pygame.event.get():
            # 當使用者結束視窗，程式也結束
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def update_display():
    gameDisplay.fill(WHITE)
    for robot in robots:
        robot.draw(gameDisplay)
    for obstacle in obstacles:
        obstacle.draw(gameDisplay)
    pygame.display.update()


pygame.init()
gameDisplay = pygame.display.set_mode(utils.world2Canvas((128, 128)))
running = True
dragging = False

robots, obstacles = initialize(gameDisplay)

while running:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            print(mousePosition)
            for polygon in robots+obstacles:
                if polygon.contain(utils.canvas2World(mousePosition)):
                    polygon.set_drag()
                    dragging = True
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                ...

    update_display()

# sample()
