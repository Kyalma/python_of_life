"""
Encapsulated pygame
"""

import pygame

from ui import colors
from settings import *


class UIcontroller(object):
    """To display and control the program behaviour"""

    def __init__(self, **kwargs):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 15)
        self.screen = pygame.display.set_mode(
            (WIN_SX, WIN_SY))
        pygame.display.set_caption("Python of life")
        pygame.draw.rect(
            self.screen,
            0xAAAAAA,
            (0, SANDBOX_SY,
             WIN_SX, ACTION_BOX_H),
            0)
        pygame.display.update()
        text = self.font.render("Click here to pause/resume",
                                False,
                                colors.RGBA['black'])
        self.screen.blit(
            text,
            (int(WIN_SX / 2 - text.get_width() / 2),
             int(SANDBOX_SX + ACTION_BOX_H / 2 - text.get_height() / 2)))
        pygame.display.update()


    def display_life(self, board):
        self.screen.fill(0x00000, (0, 0, SANDBOX_SX, SANDBOX_SY))
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                if board[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        colors.LIFE_COLOR[board[y][x]],
                        (x * CELL_SPX, y * CELL_SPX, CELL_SPX,  \
                            CELL_SPX),
                        0)
        pygame.display.update()


    def __del__(self):
        pygame.font.quit()
        pygame.quit()