"""AoC :: Day 2"""
import time
from typing import TextIO
DAY = 2
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))

class Report(list[int]):
    """A list of levels"""

    @staticmethod
    def parse(line: str):
        """parse a row into a Report"""
        return Report([int(n) for n in line.strip().split(" ")])

    def safe_increasing(self, tol: int = 0):
        """Determine safety assuming that the report is increasing"""
        for i, (r1, r2) in enumerate(zip(self, self[1:])):
            if not 1 <= r2 - r1 <= 3:
                # This seq fails, remove either r1 or r2 and test again
                if tol > 0:
                    return Report(self[:i]+self[i+1:]).safe_increasing() or Report(self[:i+1]+self[i+2:]).safe_increasing()
                return False
        return True

    def safe(self, tol: int = 0) -> bool:
        """determine if report is safe"""
        return self.safe_increasing(tol) or Report(reversed(self)).safe_increasing(tol)

def parse(file: TextIO):
    """Parse the plaintext input"""
    return [Report.parse(i) for i in file.readlines()]


def part_one(inputs: list[Report]):
    """Solution to part one"""
    return sum(1 for i in inputs if i.safe())


def part_two(inputs: list[Report]):
    """Solution to part two"""
    return sum(1 for i in inputs if i.safe(tol=1))


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
