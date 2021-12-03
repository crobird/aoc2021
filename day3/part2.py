#!/usr/bin/env python

"""
Advent of Code 2021
"""

import argparse
import re
import math
import collections
from copy import copy
from pathlib import Path
from shutil import copyfile, copymode
from dataclasses import dataclass
from datetime import datetime, timedelta

# Bad answer: 328329

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

def filter_binary_numbers_by_index_freq(nums, index, filter_by_most):
    one_count = [x[index] for x in nums].count('1')
    half_nums = len(nums) / 2
    if one_count == half_nums:
        filter_num = str(int(filter_by_most))
    else:
        most_common = int(one_count > half_nums)
        least_common = (most_common + 1) % 2
        filter_num = str(most_common) if filter_by_most else str(least_common)
    return [n for n in nums if n[index] == filter_num]


def main(args):
    log_start()
    # ---------

    things = parse_file(args.file)

    # oxygen generator
    o_nums = copy(things)
    print(f"starting oxygen process with {len(o_nums)} items...")
    for i in range(len(things[0])):
        o_nums = filter_binary_numbers_by_index_freq(o_nums, i, True)
        if len(o_nums) == 1:
            break

    assert len(o_nums) == 1

    # co2 scrubber
    c_nums = copy(things)
    print(f"starting co2 process with {len(c_nums)} items...")
    for i in range(len(things[0])):
        c_nums = filter_binary_numbers_by_index_freq(c_nums, i, False)
        if len(c_nums) == 1:
            break

    assert len(c_nums) == 1

    o_num = int(o_nums[0], 2)
    c_num = int(c_nums[0], 2)

    print(f"{o_num=}, {c_num=}, life support rating = {o_num * c_num}")

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