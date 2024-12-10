"""AoC :: Day 10"""
import time
from typing import TextIO
DAY = 10
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))

class Topography(dict[complex, int]):
    """
    A topographical map
    
    the key is the map coordinate and its value is the height
    """

    @staticmethod
    def neighbours(position: complex):
        """return the neighbours of a point"""
        return (
            position + complex( 1, 0),
            position + complex(-1, 0),
            position + complex( 0, 1),
            position + complex( 0,-1),
        )

    def uphill(self, position: complex):
        """which neighbours are uphill with height += 1"""
        height = self[position] + 1
        return {
            neighbour for neighbour in self.neighbours(position) if self.get(neighbour, -1) == height
        }

    def count_summits(self, trailhead: complex, summit: int = 9):
        """Count the number of summits reachable from this trailhead"""
        # init
        cursors = {trailhead}
        summits = 0
        # This loop explores all possible paths
        while cursors:
            # init next cursors
            next_cursors = set()
            for cursor in cursors:
                # If path is at a summit add 1
                if self[cursor] == summit:
                    summits += 1
                # If path is isn't at a summit keep hiking
                else:
                    next_cursors.update(self.uphill(cursor))
            # repeat if there are trails that still need exploring
            cursors = next_cursors
        return summits

    def count_trails(self, trailhead: complex, summit: int = 9):
        """Count the number of distinct trails that can be taken"""
        def recurse(cursor: complex):
            """
            Recursively count distinct paths
            """
            # If we reach a summit, count this path
            if self[cursor] == summit:
                return 1
            # Recursively sum over all path branches
            return sum(recurse(c) for c in self.uphill(cursor))
        # Kick off recursion
        return recurse(trailhead)


def parse(file: TextIO, trailhead: int = 0):
    """Parse the plaintext input"""
    # init
    tmap = Topography()
    trailheads: set[complex] = set()

    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row.strip()):
            height = int(char)
            tmap[complex(x, y)] = height
            if height == trailhead:
                trailheads.add(complex(x, y))
    return tmap, trailheads


def part_one(tmap: Topography, trailheads: set[complex]):
    """Solution to part one"""
    return sum(tmap.count_summits(trailhead) for trailhead in trailheads)


def part_two(tmap: Topography, trailheads: set[complex]):
    """Solution to part two"""
    return sum(tmap.count_trails(trailhead) for trailhead in trailheads)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        tmap, trailheads = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(tmap, trailheads)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(tmap, trailheads)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
