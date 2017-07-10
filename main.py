import pygame
import concurrent.futures
import time
import sys

from gameoflife import world
from ui import uicontroller
import entities
import settings


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
            #(entities.GOSPER_GLIDER_GUN, 0, 0),
            #(entities.GOSPER_GLIDER_GUN, 0, 20)
            #(entities.LINE_OF_20, 0, 10)
        ])
    ui.display_life(game.map)

    while FOR_EVER_AND_EVER:
        
        loop_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(0, settings.SANDBOX_SX) and\
                    event.pos[1] in range(0, settings.SANDBOX_SY):

                    curr_y = int(event.pos[1] / settings.CELL_SIZE_PX)
                    curr_x = int(event.pos[0] / settings.CELL_SIZE_PX)
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
            
            #screen.blit(font.render("Iteration {}".format(game.ticks), False, (255, 255, 255)), (0, 0))
        time.sleep(0.1)

        #print("Iteration {}. Took {:2f}s".format(game.ticks, time.time() - loop_start))



def vanilla_pygame():

    all_events = list()

    while FOR_EVER_AND_EVER:
        all_events.append(pygame.event.get())
        time.sleep(0.2)
        print(all_events)


if __name__ == "__main__":
    ui = uicontroller.UIcontroller()

    #vanilla_pygame()

    thread_main()
