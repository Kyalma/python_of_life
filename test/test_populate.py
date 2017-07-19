"""
Test script for Travis CI
"""

import sys
import os
import argparse

sys.path.append(os.path.abspath('./'))

from gameoflife import pool
import entities


def dump_board(board):
    print('\n'.join(' '.join(str(x) for x in y) for y in board))
    print('-' * (len(board[0]) * 2 - 1))


def main_test(args):
    game = pool.Pool()
    game.spawn([
        (entities.LINE_OF_20, 0, 10)
        ])
    print("Seed:")
    dump_board(game.map)
    for iter in range(args.gen):
        game.populate()
        print("Generation n°{}:".format(iter + 1))
        dump_board(game.map)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="test_populate.py",
        description="Generate populations")
    parser.add_argument(
        "-gen",
        type=int,
        default=1,
        action="store")
    args = parser.parse_args()
    main_test(args)