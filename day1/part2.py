#!/usr/bin/env python

"""
Advent of Code 2021
"""

import argparse
import re
import math
import collections
from pathlib import Path
from shutil import copyfile
from dataclasses import dataclass
from datetime import datetime, timedelta

SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_INPUT_FILE = "input/" + SCRIPT_PATH.name.replace(".py", ".txt")
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
    things = []
    for line in lines:
        things.append(int(line.strip()))

    return things


def main(args):
    log_start()
    # ---------

    things = parse_file(args.file)

    larger = 0
    for i in range(len(things)):
        if i + 3 < len(things):
            i1 = i + 1
            i3 = i + 3
            i4 = i + 4
            current_three = sum(things[i:i3])
            next_three = sum(things[i1:i4])
            if next_three > current_three:
                larger += 1

    print(f"larger: {larger}")

    # ---------
    log_end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part2', default=False, action="store_true", help="Copy part1 to part2")
    parser.add_argument('-f', '--file', help='Input file, default: {}'.format(DEFAULT_INPUT_FILE), default=DEFAULT_INPUT_FILE, required=True)
    parser.add_argument('-v', '--verbose', help="Verbose output", default=False, action="store_true")
    args = parser.parse_args()

    if args.part2:
        if SCRIPT_PATH.name != "part1.py":
            print("Error: Only part1.py can be copied to part2.py")
            exit(1)
        part2 = SCRIPT_PATH.replace("part1", "part2")
        if part2.exists():
            print("Error: part2.py already exists. Delete first in order to copy part1.py again.")
            exit(1)
        copyfile(SCRIPT_PATH, part2)
        print(f"Created {part2}.")

    main(args)