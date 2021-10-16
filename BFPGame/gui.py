import pygame
from color import *


class Button:

    def __init__(self, text, width, height, pos, elevation, operation, color=RED):
        self.operation = operation
        self.default_color = color
        self.gui_font = pygame.font.Font(None, 30)
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = greyed_out(color)

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = GREY
        # text
        self.text_surf = self.gui_font.render(
            text=text, antialias=True, color=BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.default_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.operation()
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    # print('click')
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = greyed_out(self.default_color)
