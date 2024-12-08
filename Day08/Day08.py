"""AoC :: Day 8"""
from itertools import combinations
import time
from typing import TextIO
DAY = 8
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


class Antennae(dict[str, set[complex]]):
    """
    The antennae of a certain frequency
    
    Keys are the frequencies and values are the locations of the antennae of those frequencies
    """

    @staticmethod
    def pairwise_antinodes(a1: complex, a2: complex):
        """
        return the two antinode locations given a pair of antennae
        
        N.B. we do not consider the boundary in this calculation
        """
        return 2*a2 - a1, 2*a1 - a2

    @staticmethod
    def pairwise_resonance(a1: complex, a2: complex, bounds: complex):
        """
        return all antinodes including resonance, taking into account the bounds
        """
        # Init new set
        antinodes: set[complex] = set()
        # First start at a1 and walk in the direciton of a1 - a2 until you hit the boundary
        r = a1
        while (0 <= r.real < bounds.real) and (0 <= r.imag < bounds.imag):
            antinodes.add(r)
            r += a1 - a2

        # Now walk in the other direction
        r = a2
        while (0 <= r.real < bounds.real) and (0 <= r.imag < bounds.imag):
            antinodes.add(r)
            r += a2 - a1

        return antinodes

    def antinodes(self, bounds: complex):
        """Given bounds, return the antinode locations"""
        # Copy the locs so we can use pop
        antinodes: set[complex] = set()
        for freq in self:
            for a1, a2 in combinations(self[freq], 2):
                for n in self.pairwise_antinodes(a1, a2):
                    if (0 <= n.real < bounds.real) and (0 <= n.imag < bounds.imag):
                        antinodes.add(n)
        return antinodes

    def resonance(self, bounds: complex):
        """
        Given bounds, return the antinode locations including resonance effects
        """
        # Copy the locs so we can use pop
        antinodes: set[complex] = set()
        for freq in self:
            for a1, a2 in combinations(self[freq], 2):
                antinodes |= self.pairwise_resonance(a1, a2, bounds)
        return antinodes


def parse(file: TextIO):
    """Parse the plaintext input"""
    # init
    antennae = Antennae()
    x, y = 0, 0

    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row.strip()):
            if char != ".":
                if char not in antennae:
                    antennae[char] = set()
                antennae[char].add(complex(x, y))

    bounds = complex(x + 1, y + 1)

    return antennae, bounds


def part_one(antennae: Antennae, bounds: complex):
    """Solution to part one"""
    return len(antennae.antinodes(bounds))


def part_two(antennae: Antennae, bounds: complex):
    """Solution to part two"""
    return len(antennae.resonance(bounds))


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        antennae, bounds = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(antennae, bounds)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(antennae, bounds)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
