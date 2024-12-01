"""AoC :: Day 1"""
import time
from typing import TextIO
DAY = 1
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def parse(file: TextIO):
    """Parse the plaintext input"""
    return tuple(zip(*[(int(x), int(y)) for x, y in [i[:-1].split("   ") for i in file.readlines()]]))



def part_one(inputs: tuple[list[int], list[int]]):
    """Solution to part one"""
    x_list, y_list = inputs
    return sum(abs(x - y) for x, y in zip(sorted(x_list), sorted(y_list)))


def part_two(inputs: tuple[list[int], list[int]]):
    """Solution to part two"""
    x_list, y_list = inputs
    y_ref = {y: y_list.count(y) for y in set(y_list)}
    return sum(x * y_ref.get(x, 0) for x in x_list)


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
