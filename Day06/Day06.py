"""AoC :: Day 6"""
from dataclasses import dataclass
from enum import Enum
import time
from typing import TextIO
DAY = 6
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


class Direction(Enum):
    """A direction of travel as represented by a complex number"""
    UP    = complex( 0,-1)
    DOWN  = complex( 0, 1)
    RIGHT = complex( 1, 0)
    LEFT  = complex(-1, 0)

    def turn(self):
        """Turn 90 degrees clockwise"""
        return Direction(self.value * 1j)

    def cast(self, position: complex, obstacles: set[complex]):
        """cast a ray to find the closest obstacle is in the direction of travel"""
        match self:
            case Direction.UP:
                return any(
                    (obstacle.real == position.real) and (obstacle.imag < position.imag) for obstacle in obstacles
                )
            case Direction.DOWN:
                return any(
                    (obstacle.real == position.real) and (obstacle.imag > position.imag) for obstacle in obstacles
                )
            case Direction.LEFT:
                return any(
                    (obstacle.imag == position.imag) and (obstacle.real < position.real) for obstacle in obstacles
                )
            case Direction.RIGHT:
                return any(
                    (obstacle.imag == position.imag) and (obstacle.real > position.real) for obstacle in obstacles
                )

@dataclass
class Guard:
    """A guard with position and direction"""
    position: complex
    direction: Direction

    def last_step(self):
        """convenience method to make a copy of the guard at the last step"""
        return Guard(
            self.position - self.direction.value,
            self.direction
        )

    def patrol(self, obstacles: set[complex]):
        """the very strict patrol protocol"""
        while (next_position := self.position + self.direction.value) in obstacles:
            self.direction = self.direction.turn()
        self.position = next_position

    def patrol_for_candidates(self, obstacles: set[complex]):
        """patrol but also check if there are any obstacles to your right"""
        while (next_position := self.position + self.direction.value) in obstacles:
            self.direction = self.direction.turn()
        # Cast a ray out in the direction the guard will turn and search for obstacles
        if self.direction.turn().cast(self.position, obstacles):
            self.position = next_position
            return True
        self.position = next_position
        return False


def parse(file: TextIO):
    """Parse the plaintext input"""
    obstacles: set[complex] = set()
    # init some vars
    guard = None
    x, y = 0, 0

    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row):
            if char == "#":
                obstacles.add(complex(x, y))
            elif char == "^":
                guard = Guard(complex(x, y), Direction.UP)

    assert guard is not None, "No guard found in map"

    return guard, obstacles, complex(x, y)


def part_one(guard: Guard, obstacles: set[complex], bounds: complex):
    """
    Solution to part two
    
    Strategy is to do part one, but each time there is a candidate, explore that branch for a loop.
    That way, we're not repeating the whole search from the beginning for each candidate.
    """
    # Direction is important for part two so keep a dict
    visited: dict[complex, Direction] = {}
    loops = 0

    def detect_loop(guard: Guard, visited: dict[complex, Direction], obstacles_: set[complex]):
        """Return True if a loop occurs"""
        # Copy visited so that it isn't corrupted
        exploration = visited.copy()
        # Explore in new configuration
        while (0 <= guard.position.real < bounds.real) and (0 <= guard.position.imag < bounds.imag):
            guard.patrol(obstacles_)
            if guard.position in exploration:
                if guard.direction == exploration[guard.position]:
                    return True
            exploration[guard.position] =  guard.direction
        return False

    while (0 <= guard.position.real < bounds.real) and (0 <= guard.position.imag < bounds.imag):
        visited[guard.position] = guard.direction
        if guard.patrol_for_candidates(obstacles) and (guard.position not in visited):
            loops += detect_loop(
                guard.last_step(),
                visited, obstacles | {guard.position}
            )

    return len(visited), loops


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        guard, obstacles, bounds = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One + Two ::")
    t1 = -time.time()
    a1, a2 = part_one(guard, obstacles, bounds)
    t1 += time.time()
    print(f"Part One Answer: {a1}")
    print(f"Part Two Answer: {a2}")
    print(f"runtime: {t1: .4f}s")

    print(f":: total runtime: {t0+t1: .4f}s ::")


if __name__ == "__main__":
    main()
