"""
AoC :: Day 16 - Abandoned attempt

I abandoned this attempt after realizing that my graph representation
was not capable of handling the turn costs properly for part two. I 
shortcut the calculation by incorporating the cost of turning into the 
distance between nodes, but in part two this causes problems since there
are multiple paths to the same node that incur the turn cost before or after
reaching the node.
"""
from dataclasses import dataclass
import math
import re
import time
from heapq import heappop, heappush
from typing import Literal, Optional, TextIO
DAY = 16
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))

# Constants
## Grid constants
START_TILE = "S"
END_TILE = "E"
WALL_TILE = "#"
FACING = complex(1, 0) # Facing east
## Movement penalties
FORWARD_PENALTY = 1
TURN_PENALTY = 1_000


@dataclass()
class Cursor:
    """A cursor in a maze"""
    position: complex
    direction: complex
    cost: int

    def __hash__(self):
        return hash((self.position, self.direction))

    def __lt__(self, other: "Cursor"):
        return self.cost < other.cost

    def move(self, direction: complex):
        """move cursor in a direction"""
        # Moving forwards
        if direction == self.direction:
            return Cursor(
                self.position + direction,
                self.direction,
                self.cost + FORWARD_PENALTY
            )
        # Else change direction and incur extra penalty
        return Cursor(
            self.position + direction,
            direction,
            self.cost + FORWARD_PENALTY + TURN_PENALTY
        )

class Maze:
    """The maze to be navigated"""

    DIRECTIONS = [
        complex(1, 0),  # Right
        complex(-1, 0),  # Left
        complex(0, 1),  # Down
        complex(0, -1)  # Up
    ]

    def __init__(self, adjacency: dict[complex, list[complex]], start: complex, end: complex):
        self.adjacency = adjacency
        self.path: dict[complex, int] = {}
        self.start = start
        self.end = end

    @staticmethod
    def heuristic(end: complex):
        """Heuristic for A* search"""
        def func(position: complex):
            base = int(abs(position.real - end.real) + abs(position.imag - end.imag))
            # Add penalty for direction change
            if position.real != end.real and position.imag != end.imag:
                return base + TURN_PENALTY
            return base
        return func

    def solve(self, start: Optional[complex] = None, end: Optional[complex] = None):
        """Use A* to solve the maze"""
        # Init
        start = start if start else self.start
        end = start if end else self.end
        self.path[start] = -1
        # If start and end are the same, no cost
        if start == end:
            return 0
        # Define heuristic function
        h = self.heuristic(end)
        # Priority queue for A* search
        queue: list[tuple[int, Cursor]] = [(0, Cursor(start, FACING, 0))]

        # A* Search
        while queue:
            _, cursor = heappop(queue)
            for adj in self.adjacency[cursor.position]:
                new_cursor = cursor.move(adj - cursor.position)
                if adj not in self.path or new_cursor.cost < self.path[adj]:
                    self.path[adj] = new_cursor.cost
                    heappush(queue, (new_cursor.cost + h(adj), new_cursor))

        return self.path.get(end, math.inf)



def parse(file: TextIO):
    """Parse the plaintext input"""
    # Get set of vacant spaces as complex numbers
    vacant_spaces = []
    start = None
    end = None

    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            if char == START_TILE:
                start = complex(x, y)
            if char == END_TILE:
                end = complex(x, y)
            if char != WALL_TILE:
                vacant_spaces.append(complex(x, y))

    # If start or end are not found, raise an error
    assert start is not None, "Start tile not found"
    assert end is not None, "End tile not found"

    # Create adjacency dict for the maze
    adjacency = {}

    for pos in vacant_spaces:
        adjacency[pos] = [pos + d for d in Maze.DIRECTIONS if pos + d in vacant_spaces]

    return Maze(adjacency, start, end)



def part_one(maze: Maze):
    """Solution to part one"""
    return maze.solve()


def part_two(maze: Maze):
    """
    Solution to part two
    
    TODO: The problem here is that the cost stored in maze.path[position] fails to account
    for the fact that you may turn to continue along the optimal path. E.g.

    ```
    ######
    #..X..
    #.#.##
    ....#
    #####
    ```

    After the X, both paths are optimal, but the cost of the leftmost path will be higher
    since the rightmost path only incurs the cost of the second turn after the X.
    """
    tiles = set()
    cursors = {maze.end}
    # Get all tiles in optimal path(s) from start to end
    while cursors:
        tiles.update(cursors)
        cursors = {
            adj for cursor in cursors for adj in maze.adjacency[cursor] if maze.path.get(adj, math.inf) < maze.path[cursor]
        }
    return len(tiles)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        maze = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(maze)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(maze)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
