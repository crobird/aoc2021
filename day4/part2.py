#!/usr/bin/env python

"""
Advent of Code 2021
"""

import argparse
import re
import math
import collections
from pathlib import Path
from shutil import copyfile, copymode
from dataclasses import dataclass
from datetime import datetime, timedelta

SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_INPUT_FILE = SCRIPT_PATH.parent / "input" / SCRIPT_PATH.name.replace(".py", ".txt")
STARTED_AT = None

class Board:
    BOARD_SIZE = 5

    def __init__(self, input_lines):
        self.board = [re.split(r'\s+', l) for l in input_lines]
        self.marked = [[False]*Board.BOARD_SIZE for n in range(Board.BOARD_SIZE)]
        self.winner = False
        self.lookup = {}
        self.winning_number = None
        self._create_lookup()

    def __repr__(self):
        lines = []
        for r in range(len(self.board)):
            row = []
            for c in range(len(self.board[0])):
                row.append(self._get_val(r, c))
            lines.append(f" ".join(row))
        return "\n".join(lines)

    def _get_val(self, r, c):
        marked = '*' if self.marked[r][c] else ' ' 
        return f"{self.board[r][c]:>2}{marked}"

    def _create_lookup(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                self.lookup[self.board[r][c]] = (r,c)        

    def check_number(self, num):
        if num in self.lookup:
            r,c = self.lookup[num]
            self.marked[r][c] = True
            if all(self.marked[r]) or all([x[c] for x in self.marked]):
                self.winning_number = int(num)
                print(f"Winning number: {num}")
                print(self)
                self.winner = True
        return self.winner

    @property
    def score(self):
        if not self.winner:
            raise Exception("This board is not a winner.")

        unmarked_sum = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if not self.marked[r][c]:
                    unmarked_sum += int(self.board[r][c])

        return unmarked_sum * self.winning_number
    

def log_start():
    global STARTED_AT
    STARTED_AT = datetime.now()
    print(f"[{STARTED_AT}]")

def log_end():
    global STARTED_AT
    duration = datetime.now() - STARTED_AT
    print(f"[execution time: {duration}]")

def file_contents(filepath, strip_empty_lines=True):
    empty_lines = not strip_empty_lines
    with open(filepath, "r") as fh:
        lines = [l.strip() for l in fh if (empty_lines or l.strip())]
    return lines


def parse_file(filepath):
    lines = file_contents(filepath, strip_empty_lines=False)
    things = []
    turns = None
    board_lines = []
    for line in lines:
        if not turns:
            turns = line.strip().split(',')
            continue

        if line.strip() == '':
            if not board_lines:
                continue
            things.append(Board(board_lines))
            board_lines = []
        else:
            board_lines.append(line.strip())

    things.append(Board(board_lines))
    return (turns,things)


def main(args):
    log_start()
    # ---------

    turns,things = parse_file(args.file)

    winning_board = None

    for turn in turns:
        print(f"++++ {turn} ++++")
        for board in things:
            if board.winner:
                continue
            if board.check_number(turn):
                winning_board = board

    print(f"Score of winning board: {winning_board.score}")

    # ---------
    log_end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part2', default=False, action="store_true", help="Copy part1 to part2")
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    if args.part2:
        if SCRIPT_PATH.name != "part1.py":
            print("Error: Only part1.py can be copied to part2.py")
            exit(1)
        part2 = SCRIPT_PATH.with_name(SCRIPT_PATH.name.replace("part1", "part2"))
        if part2.exists():
            print("Error: part2.py already exists. Delete part2.py first in order to copy again.")
            exit(1)
        copyfile(SCRIPT_PATH, part2)
        copymode(SCRIPT_PATH, part2)
        print(f"Created {part2}.")
        exit(0)

    main(args)