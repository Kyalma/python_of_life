"""
Functions used in a ProcessPool
"""

def insert_figure(board, figure, x1, y1) -> None:
    for y2 in range(len(figure)):
        for x2 in range(len(figure[y2])):
            board[y1 + y2][x1 + x2] = figure[y2][x2]


def local_is_alive(cell_status: int):
    return (1 if cell_status in (1, 2) else 0)


def local_apply_rule(board, x: int, y: int) -> None:
    ## Reset for the current generation ##
    total = 0

    ## Upper neighbours ##
    total += local_is_alive(board[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
    total += local_is_alive(board[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][x])
    total += local_is_alive(board[(y - 1 if y - 1 >= 0 else settings.CELLS_Y - 1)][(x + 1 if x + 1 < settings.CELLS_X else 0)])

    ## Left and Right neighbours ##
    total += local_is_alive(board[y][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
    total += local_is_alive(board[y][(x + 1 if x + 1 < settings.CELLS_X else 0)])

    ## Lower neighbours ##
    total += local_is_alive(board[(y + 1 if y + 1 < settings.CELLS_Y else 0)][(x - 1 if x - 1 >= 0 else settings.CELLS_X - 1)])
    total += local_is_alive(board[(y + 1 if y + 1 < settings.CELLS_Y else 0)][x])
    total += local_is_alive(board[(y + 1 if y + 1 < settings.CELLS_Y else 0)][(x + 1 if x + 1 < settings.CELLS_X else 0)])

    ## Original Conway's Game of Life rules ##
    if board[y][x] != 0 and (total < 2 or total > 3):
        return 0
    elif board[y][x] != 0 and total in (2, 3):
        return 2
    elif board[y][x] == 0 and total == 3:
        return 1

    ## if there is no rules to apply ##
    return board[y][x]


def process_main():
    ## In progress ##
    tmp = [[0 for x in range(settings.CELLS_X)] for y in range(settings.CELLS_Y)]

    insert_figure(tmp, GOSPER_GLIDER_GUN, 0, 0)
    insert_figure(tmp, GOSPER_GLIDER_GUN, 0, 20)

    process_executor = concurrent.futures.ProcessPoolExecutor(max_workers=settings.PROCESS)
    
    while FOR_EVER_AND_EVER:
        
        loop_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        process_start = time.time()
        tasks = [
            process_executor.submit(local_apply_rule, tmp, x, y) for x in range(settings.CELLS_X) for y in range(settings.CELLS_Y)
            ]
        concurrent.futures.wait(tasks)
        print(time.time() - process_start)

        for y in range(settings.CELLS_Y):
            for x in range(settings.CELLS_X):
                tmp[x][y] = tasks[y * settings.CELLS_X + x]._result

        draw_board(tmp)

        print("Iteration {}. Took {:2f}s".format(0, time.time() - loop_start))

