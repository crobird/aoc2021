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
    things = []
    for line in lines:
        # Parse with regex
        mobj = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
        if mobj:
            things.append(list(map(int, mobj.groups())))

    return things

def line_points(n1, n2):
    if n1 > n2:
        r = list(range(n2, n1+1))
        r.reverse()
        return r
    return list(range(n1, n2+1))

def get_line_points(x1, y1, x2, y2):
    if x1 != x2:
        x_points = line_points(x1, x2)
    if y1 != y2:
        y_points = line_points(y1, y2)
    if x1 == x2:
        x_points = [x1]*len(y_points)
    if y1 == y2:
        y_points = [y1]*len(x_points)
    points = []
    for i in range(len(x_points)):
        points.append([x_points[i], y_points[i]])
    return points

def place_line(ocean, points):
    new_overlaps = 0
    for x,y in get_line_points(*points):
        if ocean[y][x] == '.':
            ocean[y][x] = 1
        else:
            ocean[y][x] += 1
            if ocean[y][x] == 2:
                new_overlaps += 1
    return new_overlaps

def main(args):
    log_start()
    # ---------

    things = parse_file(args.file)

    max_x = 0
    max_y = 0
    for t in things:
        biggest_x = max([t[0], t[2]])
        biggest_y = max([t[1], t[3]])
        if biggest_x > max_x:
            max_x = biggest_x
        if biggest_y > max_y:
            max_y = biggest_y

    max_x += 1
    max_y += 1

    print(f"Building an ocean that is {max_x} x {max_y}.")
    ocean = [['.']*max_x for n in range(max_y)]

    overlap_count = 0
    for t in things:
        overlapped = place_line(ocean, t)
        overlap_count += overlapped

    for r in ocean:
        print("".join(map(str,r)))

    print(f"There are {overlap_count} points of overlap.")

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