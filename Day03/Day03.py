"""AoC :: Day 3"""
import re
import time
from typing import TextIO
DAY = 3
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def parse(file: TextIO):
    """Parse the plaintext input"""
    return file.read()[:-1]

# helpful pattern for catching a valid multiplication operation
re_mul = re.compile(r"mul\(\d+,\d+\)")

def part_one(inputs: str):
    """Solution to part one"""
    # Find all valid mul(X,Y) pairs and split them up
    pairs = [str(s)[4:-1].split(",") for s in re_mul.findall(inputs)]
    return sum(int(x)*int(y) for x, y in pairs)


def part_two(inputs: str):
    """Solution to part two"""
    # Get the valid do blocks of code
    do_blocks = []
    for block in inputs.split("do()"):
        # try to find the index of where a don't() command lives and trim block
        try:
            i = block.index("don't()")
            do_blocks.append(block[:i])
        # else the whole block is valid code
        except ValueError:
            do_blocks.append(block)

    # Now sum part one for each do block
    return sum(part_one(d) for d in do_blocks)


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
