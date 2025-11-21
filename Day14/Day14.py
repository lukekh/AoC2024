"""AoC :: Day 14"""
from dataclasses import dataclass
import math
import re
import time
from typing import TextIO
DAY = 14
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


# Constants defined in the problem description
LOBBY_DIMS = 101 + 103j  # (width, height)

# Regular expression to match the robot's position and velocity
re_robot = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

@dataclass
class Robot:
    """
    A robot with a position and velocity, each represented as a complex number
    """
    position: complex
    velocity: complex

    @staticmethod
    def complex_mod(z: complex, mod: complex) -> complex:
        """Return the complex number z modulo mod"""
        return complex(z.real % mod.real, z.imag % mod.imag)

    @staticmethod
    def sign(n: float) -> float:
        """Return the sign of an integer n or 0 if n is zero"""
        return (n > 0) - (n < 0)

    def move(self, steps: int = 1):
        """Move the robot by its velocity, returns a new Robot instance"""
        position = self.complex_mod(self.position + self.velocity * steps, LOBBY_DIMS)
        return Robot(position, self.velocity)

    def update(self, steps: int = 1):
        """Move the robot by its velocity, returns a new Robot instance"""
        self.position = self.complex_mod(self.position + self.velocity * steps, LOBBY_DIMS)

    def quadrant(self) -> complex:
        """Return the quadrant of the robot's position, excluding the center axes"""
        real = self.sign(self.position.real - ((LOBBY_DIMS.real - 1) / 2))
        im = self.sign(self.position.imag - ((LOBBY_DIMS.imag - 1) / 2))
        return complex(real, im) if (real * im) else 0

    @classmethod
    def parse(cls, string: str) -> 'Robot':
        """Parse a string into a Robot instance"""
        match = re_robot.match(string)
        if not match:
            raise ValueError(f"Invalid robot string: {string}")
        position = complex(int(match.group(1)), int(match.group(2)))
        velocity = complex(int(match.group(3)), int(match.group(4)))
        return cls(position, velocity)


def parse(file: TextIO):
    """Parse the plaintext input"""
    return [Robot.parse(i[:-1]) for i in file.readlines()]

def part_one(inputs: list[Robot]):
    """Solution to part one"""
    quadrants = [quadrant for r in inputs if (quadrant := r.move(100).quadrant())]
    counts = {q: quadrants.count(q) for q in set(quadrants)}
    return math.prod(counts.values())


def part_two(inputs: list[Robot]):
    """
    Solution to part two
    
    I guessed that the solution would occur when all the robots
    occupied unique positions and got lucky.
    """
    N = len(inputs)
    i = 0
    while True:
        if N == len({r.position for r in inputs}):
            return i
        for r in inputs:
            r.update()
        i += 1


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
