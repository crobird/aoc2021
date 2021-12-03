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

@dataclass
class Tile:
    x: int
    y: int

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
    lines = file_contents(filepath)
    return [x.strip() for x in lines]

def main(args):
    log_start()
    # ---------

    things = parse_file(args.file)

    gamma_bits = ""
    freq = [0]*len(things[0])
    for t in things:
        for i,c in enumerate(t):
            if c == '1':
                freq[i] += 1

    for n in freq:
        gamma_bits += '1' if n > len(things) / 2 else '0'

    gamma_num = int(gamma_bits, 2)
    epsilon_num = gamma_num ^ int('1'*len(gamma_bits), 2)
    print(f"gamma_num * epsilon_num = {gamma_num * epsilon_num}")
        

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