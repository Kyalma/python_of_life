import pygame
import time
import sys
import numpy

GLIDER = [
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1]
    ]

GOSPER_GLIDER_GUN = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

LIFE_STATUS_CODE = {
    'DEAD': 0,
    'BORD': 1,
    'LIVE': 2,
    'DIED': 3
    }

LIFE_COLOR = {
    0: (0, 0, 0),
    1: (0, 255, 0),
    2: (255, 255, 0),
    3: (255, 0, 0)
    }

CELLS_X = 80
CELLS_Y = 80

CELL_SIZE_PX = 10

WIN_SIZE_X = CELLS_X * CELL_SIZE_PX
WIN_SIZE_Y = CELLS_Y * CELL_SIZE_PX

FOR_EVER_AND_EVER = True


def draw_board(board):
    screen.fill((0, 0, 0))
    for y in range(CELLS_Y):
        for x in range(CELLS_X):
            if board[y][x]:
                pygame.draw.rect(
                    screen,
                    LIFE_COLOR[board[y][x]],
                    (x * CELL_SIZE_PX, y * CELL_SIZE_PX, CELL_SIZE_PX,  \
                     CELL_SIZE_PX),
                    0)
    pygame.display.update()


def dump_board(board):
    print('\n'.join(''.join(str(x) for x in y) for y in board))


def insert_figure(board, figure, x1, y1) -> None:
    for y2 in range(len(figure)):
        for x2 in range(len(figure[y2])):
            board[y1 + y2][x1 + x2] = figure[y2][x2]


def is_alive(cell) -> int:
    return (1 if cell in (1, 2) else 0)

def get_nb_neighbours(board, x, y) -> int:
    total = 0
    total += is_alive(board[(y - 1 if y - 1 >= 0 else CELLS_Y - 1)][(x - 1 if x - 1 >= 0 else CELLS_X - 1)])
    total += is_alive(board[(y - 1 if y - 1 >= 0 else CELLS_Y - 1)][x])
    total += is_alive(board[(y - 1 if y - 1 >= 0 else CELLS_Y - 1)][(x + 1 if x + 1 < CELLS_X else 0)])

    total += is_alive(board[y][(x - 1 if x - 1 >= 0 else CELLS_X - 1)])
    total += is_alive(board[y][(x + 1 if x + 1 < CELLS_X else 0)])

    total += is_alive(board[(y + 1 if y + 1 < CELLS_Y else 0)][(x - 1 if x - 1 >= 0 else CELLS_X - 1)])
    total += is_alive(board[(y + 1 if y + 1 < CELLS_Y else 0)][x])
    total += is_alive(board[(y + 1 if y + 1 < CELLS_Y else 0)][(x + 1 if x + 1 < CELLS_X else 0)])
    return total


def main():
    board = [[0 for x in range(CELLS_X)] for y in range(CELLS_Y)]

    insert_figure(board, GOSPER_GLIDER_GUN, 0, 0)
    insert_figure(board, GOSPER_GLIDER_GUN, 0, 40)
    #insert_figure(board, GLIDER, 0, 0)
    iteration = 0

    while FOR_EVER_AND_EVER:
        new_board = [[0 for x in range(CELLS_X)] for y in range(CELLS_Y)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        loop_start = time.time()
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                neighbours = get_nb_neighbours(board, x, y)

                if not board[y][x] and not neighbours:
                    pass
                elif board[y][x] in (1, 2) and (neighbours < 2 or neighbours > 3):
                    new_board[y][x] = 3
                elif board[y][x] in (1, 2) and neighbours in (2, 3):
                    new_board[y][x] = 2
                elif board[y][x] in (0, 3) and neighbours == 3:
                    new_board[y][x] = 1
                elif board[y][x] == 3:
                    new_board[y][x] = 0

        draw_board(new_board)
        screen.blit(font.render("Iteration {}".format(iteration), False, (255, 255, 255)), (0, 0))
        pygame.display.update()
        print("Iteration {}. Took {:2f}s".format(iteration, time.time() - loop_start))
        board = list(new_board)
        iteration += 1

if __name__ == "__main__":
    pygame.init()
    #clock = pygame.time.Clock()
    #clock.tick(30)
    pygame.font.init()
    font = pygame.font.SysFont("monospace", 12)
    screen = pygame.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))
    main()
    pygame.font.quit()
    pygame.quit()