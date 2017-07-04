"""
Test script for Travis CI
"""

import sys
import os

sys.path.append(os.path.abspath('./'))

from gameoflife import world
import entities


def dump_board(board):
    print('\n'.join(''.join(str(x) for x in y) for y in board))

def main_test():
    game = world.World()
    game.spawn([
        (entities.LINE_OF_20, 0, 10)
        ])
    for _ in range(10):
        game.populate()
        dump_board(game.map)
    return 0

if __name__ == '__main__':
    main_test()