"""AoC :: Day XX"""
from dataclasses import dataclass
import math
import re
import time
from typing import Dict, List, Literal, Set, TextIO
DAY = XX
INPUT_FILE = f'Day{DAY}/Day{DAY}.in'
OUTPUT_FILE = f'Day{DAY}/Day{DAY}.out'


def parse(file: TextIO):
    """Parse the plaintext input"""
    return [i[:-1] for i in file.readlines()]


def part_one(inputs: list[str]):
    """Solution to part one"""
    return 1


def part_two(inputs: list[str]):
    """Solution to part two"""
    return 2


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        inputs = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
