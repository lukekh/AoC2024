"""AoC :: Day 7"""
from dataclasses import dataclass
import time
from typing import TextIO
DAY = 7
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


@dataclass
class Equation:
    """
    A test_value and list of numbers
    """
    test_value: int
    numbers: list[int]

    @classmethod
    def parse(cls, s: str):
        """parse an Equation from a string input"""
        test_value, numbers = s.split(": ")
        return cls(int(test_value), [int(n) for n in numbers.split(" ")])

    def valid(self):
        """determine if a test value is achievable"""
        N = len(self.numbers)
        def recurse(goal: int, cur: int, idx: int):
            """Recursively apply operations, pruning branches that are infeasible"""
            if cur > goal:
                return False
            if idx < N:
                # Possible operations are + or * or ||
                n = self.numbers[idx]
                return (
                    recurse(goal, cur * n, idx+1)
                    or recurse(goal, cur + n, idx+1)
                )
            # If there are no numbers remaining then check for equality
            return goal == cur

        return recurse(self.test_value, self.numbers[0], 1)

    def valid2(self):
        """determine if a test value is achievable, now including a concatenation operation"""
        N = len(self.numbers)
        def recurse(goal: int, cur: int, idx: int):
            """Recursively apply operations, pruning branches that are infeasible"""
            if cur > goal:
                return False
            if idx < N:
                # Possible operations are + or * or ||
                n = self.numbers[idx]
                return (
                    recurse(goal, cur * n, idx+1)
                    or recurse(goal, int(str(cur) + str(n)), idx+1)
                    or recurse(goal, cur + n, idx+1)
                )
            # If there are no numbers remaining then check for equality
            return goal == cur

        return recurse(self.test_value, self.numbers[0], 1)

def parse(file: TextIO):
    """Parse the plaintext input"""
    return [Equation.parse(i[:-1]) for i in file.readlines()]


def part_one(inputs: list[Equation]):
    """Solution to part one"""
    return sum(eq.test_value for eq in inputs if eq.valid())


def part_two(inputs: list[Equation]):
    """Solution to part two"""
    return sum(eq.test_value for eq in inputs if eq.valid2())


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
