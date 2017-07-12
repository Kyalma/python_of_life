"""
Encapsulated pygame
"""

import pygame

from ui import labelbutton, colors, controlbar
from settings import *


class UIcontroller(object):
    """To display and control the program behaviour"""

    def __init__(self, **kwargs):
        pygame.init()
        pygame.font.init()
        self.loop_ms = 100
        self.screen = pygame.display.set_mode(
            (WIN_SX, WIN_SY))
        pygame.display.set_caption("Python of life")

        bar = controlbar.ControlBar(
            (WIN_SX, ACTION_BOX_H),
            bg_color=colors.HEXA['grey'])

        pause = labelbutton.LabelButton("Pause/Resume", font_size=15, margin=5, padding=10)
        reset = labelbutton.LabelButton("Reset", font_size=15, margin=5, padding=10)

        bar.add_object(pause)
        bar.add_object(reset)
        bar.generate()

        self.screen.blit(bar.box, (0, SANDBOX_SY))
        pygame.display.update()


    def display_life(self, board):
        self.screen.fill(colors.HEXA['black'], (0, 0, SANDBOX_SX, SANDBOX_SY))
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                if board[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        colors.LIFE_COLOR[board[y][x]],
                        (x * CELL_SPX, y * CELL_SPX, CELL_SPX, CELL_SPX),
                        0)
        pygame.display.update()


    def delay(self, **kwargs):
        if 's' in kwargs:
            pygame.time.delay(kwargs['s'] * 1000)
        elif 'ms' in kwargs:
            pygame.time.delay(kwargs['ms'])
        else:
            pygame.time.delay(self.loop_ms)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pygame.font.quit()
        pygame.quit()
