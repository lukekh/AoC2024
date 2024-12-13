"""AoC :: Day 13"""
from dataclasses import dataclass
import re
import time
from typing import TextIO
DAY = 13
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))

# Used in parsing a machine spec
re_machine = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")

@dataclass
class Machine:
    """
    A machine with two buttons.
    
    Pressing Button A costs 3 tokens, Pressing B costs 1 token
    """
    A: complex
    B: complex
    Prize: complex

    def solve(self, delta: complex = 0):
        """A crude solver, outputs the number of tokens"""
        # This delta arises in part two
        z = self.Prize + delta
        # Solve a 2x2 system for the number of A & B Button presses to reach Prize
        det = self.A.real * self.B.imag - self.B.real * self.A.imag
        k_A = (self.B.imag * z.real - self.B.real * z.imag) / det
        k_B = (self.A.real * z.imag - self.A.imag * z.real) / det

        # Check the number of button hits is integral
        if (int(k_A) == k_A) and (int(k_B) == k_B):
            return int(3*k_A + k_B)
        return 0

    @staticmethod
    def parse(s: str):
        """parse a string into a Machine"""
        m = re_machine.match(s)
        if m is None:
            raise ValueError("No machine match made")
        return Machine(
            complex(int(m.group(1)), int(m.group(2))),
            complex(int(m.group(3)), int(m.group(4))),
            complex(int(m.group(5)), int(m.group(6))),
        )


def parse(file: TextIO):
    """Parse the plaintext input"""
    return [Machine.parse(i.strip()) for i in file.read().split("\n\n")]


def part_one(inputs: list[Machine]):
    """Solution to part one"""
    return sum(i.solve() for i in inputs)


def part_two(inputs: list[Machine], delta: complex = complex(10_000_000_000_000, 10_000_000_000_000)):
    """Solution to part two"""
    return sum(i.solve(delta) for i in inputs)


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
