"""AoC :: Day 4"""
import time
from typing import TextIO
DAY = 4
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def parse(file: TextIO):
    """Parse the plaintext input"""
    return [i[:-1] for i in file.readlines()]


def part_one(inputs: list[str], search: str = "XMAS"):
    """Solution to part one"""
    N = len(search)
    count = 0
    # Right/Left
    for row in inputs:
        for i in range(len(row) - N + 1):
            word = row[i:i+N]
            count += word == search
            count += word[::-1] == search
    # Up/Down
    for i in range(len(inputs) - N + 1):
        for j, char in enumerate(inputs[i]):
            word = char + inputs[i+1][j] + inputs[i+2][j] + inputs[i+3][j]
            count += word == search
            count += word[::-1] == search
    # Diagonal Down
    for i in range(len(inputs) - N + 1):
        for j in range(len(inputs[i]) - N + 1):
            word = inputs[i][j] + inputs[i+1][j+1] + inputs[i+2][j+2] + inputs[i+3][j+3]
            count += word == search
            count += word[::-1] == search
    # Diagonal Up
    for i in range(len(inputs) - N + 1):
        for j in range(len(inputs[i]) - N + 1):
            word = inputs[i+3][j] + inputs[i+2][j+1] + inputs[i+1][j+2] + inputs[i][j+3]
            count += word == search
            count += word[::-1] == search

    return count


def part_two(inputs: list[str]):
    """Solution to part two"""
    counts = 0
    for i in range(len(inputs) - 2):
        for j in range(len(inputs[0]) - 2):
            # A must be in the middle
            if inputs[i+1][j+1] == "A":
                # Create a mask on the relevant characters and enumerate the possible configurations
                mask = inputs[i][j] + inputs[i][j+2] + inputs[i+2][j] + inputs[i+2][j+2]
                counts += mask in ("MMSS", "MSMS", "SSMM", "SMSM")
    return counts


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
