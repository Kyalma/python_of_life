import pygame
import concurrent.futures
import time
import sys
import itertools

from gameoflife import pool
from ui import uicontroller, displayedobject, controlbar, colors, labelbutton

import entities
from settings import *


#LIFE_STATUS_CODE = {
#    'DEAD': 0,
#    'BORD': 1,
#    'LIVE': 2,
#    }

FOR_EVER_AND_EVER = True


def dump_board(board):
    print('\n'.join(''.join(str(x) for x in y) for y in board))


def loop():
    while FOR_EVER_AND_EVER:
        ui.get_mouse_event()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        while not ui.events.empty():
            event = ui.events.get_nowait()
            for object in itertools.chain(ui.pools, ui.controlbars):
                if object.is_in_range(event.pos):
                    object.interact(event.pos)
            ui.events.task_done()

        for pool in ui.pools:
            if not pool.obj.paused:
                pool.obj.populate()
            ui.display_life(pool.obj.map)
            
        #ui.delay()


if __name__ == "__main__":
    pool1 = pool.Pool(
        (CELLS_X, CELLS_Y),
        threads=THREADS,
        entities=[
            (entities.GOSPER_GLIDER_GUN, 0, 0),
        ])

    with uicontroller.UIcontroller() as ui:
        ui.add_pool(
            displayedobject.DisplayedObject(
                pool1,
                (0, 0),
                (CELLS_X * CELL_SPX, CELLS_Y * CELL_SPX)))
        ui.add_controlbar(
            displayedobject.DisplayedObject(
                controlbar.ControlBar(
                    (WIN_SX, ACTION_BOX_H),
                    bg_color=colors.HEXA['grey'],
                    content=[
                        labelbutton.LabelButton(
                            "Pause/Resume",
                            pool1.pause,
                            font_size=15,
                            margin=5,
                            padding=5),
                        labelbutton.LabelButton(
                            "Reset",
                            pool1.restore_seed,
                            font_size=15,
                            margin=5,
                            padding=5)
                        ]),
                (0, SANDBOX_SY),
                (WIN_SX, ACTION_BOX_H)))
        ui.generate()
        loop()
