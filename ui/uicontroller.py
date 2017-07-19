"""
Encapsulated pygame
"""

import pygame
import queue

from ui import displayedobject, labelbutton, colors, controlbar
from gameoflife import pool
from settings import *


class UIcontroller(object):
    """To display and control the program behaviour"""

    def __init__(self, **kwargs):
        pygame.init()
        pygame.font.init()
        self.loop_ms = 100
        self.controlbars = list()
        self.pools = list()
        self.events = queue.Queue()


    def add_controlbar(self, object: displayedobject.DisplayedObject):
        self.controlbars.append(object)

    def add_pool(self, object: displayedobject.DisplayedObject):
        self.pools.append(object)

    def generate(self):
        self.screen = pygame.display.set_mode(
            (WIN_SX, WIN_SY))
        pygame.display.set_caption("Python of life")
        for cbar in self.controlbars:
            cbar.obj.generate()
            self.screen.blit(cbar.obj.box, cbar.pos)
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


    def get_mouse_event(self):
        for event in pygame.event.get(
            [
                pygame.MOUSEBUTTONDOWN,
                #pygame.MOUSEBUTTONUP
            ]):
            self.events.put(event)


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
