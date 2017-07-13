import pygame
import concurrent.futures
import time
import sys

from gameoflife import world
from ui import uicontroller, controlbar, colors, labelbutton
import entities
from settings import *


#LIFE_STATUS_CODE = {
#    'DEAD': 0,
#    'BORD': 1,
#    'LIVE': 2,
#    }

OPPOSITE_STATE = {
    0: 1,
    1: 0,
    2: 0
    }

FOR_EVER_AND_EVER = True


def dump_board(board):
    print('\n'.join(''.join(str(x) for x in y) for y in board))


def thread_main():
    game = world.World()
    game.spawn(
        [
            (entities.GLIDER, 8, 8),
            #(entities.GOSPER_GLIDER_GUN, 0, 0),
            #(entities.GOSPER_GLIDER_GUN, 0, 10)
            #(entities.LINE_OF_20, 0, 10)
        ])
    ui.display_life(game.map)

    while FOR_EVER_AND_EVER:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(0, SANDBOX_SX) and\
                    event.pos[1] in range(0, SANDBOX_SY):

                    curr_y = int(event.pos[1] / settings.CELL_SPX)
                    curr_x = int(event.pos[0] / settings.CELL_SPX)
                    game.map[curr_y][curr_x] =  \
                        OPPOSITE_STATE[game.map[curr_y][curr_x]]
                    ui.display_life(game.map)
                else:
                    game.paused = not game.paused
            if event.type == pygame.QUIT:
                return
        
        if not game.paused:
            game.populate()
            ui.display_life(game.map)
            
        ui.delay()


if __name__ == "__main__":
    with uicontroller.UIcontroller() as ui:
        ui.add_controlbars(
            [
                {
                    'object':
                        controlbar.ControlBar(
                            (WIN_SX, ACTION_BOX_H),
                            bg_color=colors.HEXA['grey'],
                            content=[
                                labelbutton.LabelButton(
                                    "Pause/Resume",
                                    font_size=15,
                                    margin=5,
                                    padding=5),
                                labelbutton.LabelButton(
                                    "Reset",
                                    font_size=15,
                                    margin=5,
                                    padding=5)
                                ]),
                    'pos': (0, SANDBOX_SY)
                }
            ])
        ui.generate()
        thread_main()
