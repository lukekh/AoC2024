"""AoC :: Day 15"""
import time
from typing import TextIO
DAY = 15
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def move_from_char(char: str) -> complex:
    """Convert a character to a Move enum"""
    match char:
        case "^":
            return 0 - 1j
        case "v":
            return 0 + 1j
        case "<":
            return -1 + 0j
        case ">":
            return 1 + 0j
        case _:
            raise ValueError(f"Invalid move character: {char}")


class Warehouse:
    """A map of the warehouse"""
    def __init__(self, walls: set[complex], robot: complex, boxes: set[complex]):
        self.robot = robot
        self.boxes = boxes
        self.walls = walls

    def move(self, direction: complex):
        """Move the robot in the given direction if possible"""
        new_robot_position = self.robot + direction

        # If the new position is a wall, do nothing
        if new_robot_position in self.walls:
            return

        # If the new position is a box, check if it can be moved
        if new_robot_position in self.boxes:
            next_open_position = self.recursive_check_next_open_position(new_robot_position, direction)
            # If the next open position is None, the box cannot be moved
            # so we do nothing
            if next_open_position is None:
                return
            # Update the box positions to reflect the move
            self.boxes.remove(new_robot_position)
            self.boxes.add(next_open_position)

        # Move the robot to the new position
        self.robot = new_robot_position

    def recursive_check_next_open_position(self, position: complex, direction: complex) -> complex | None:
        """
        Check if the robot can move in the given direction recursively
        
        It will return None if it cannot move and the next open position if it can move,
        which will be the position the boxes are pushed to.
        (i.e. remove the box from the current position and place it at the new position).
        """
        new_position = position + direction

        if new_position in self.walls:
            return None
        if new_position in self.boxes:
            return self.recursive_check_next_open_position(new_position, direction)
        return new_position

    def GPS_sum(self) -> int:
        """Calculate the GPS sum of the warehouse"""
        return int(sum(box.real + 100 * box.imag for box in self.boxes))

    def print_grid(self):
        """Print the grid of the warehouse"""
        min_x = int(min(box.real for box in self.walls))
        max_x = int(max(box.real for box in self.walls))
        min_y = int(min(box.imag for box in self.walls))
        max_y = int(max(box.imag for box in self.walls))

        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                pos = complex(x, y)
                if pos == self.robot:
                    line += "@"
                elif pos in self.boxes:
                    line += "O"
                elif pos in self.walls:
                    line += "#"
                else:
                    line += "."
            print(line)

class Warehouse2:
    """A map of the warehouse for part two"""
    def __init__(self, walls: set[complex], robot: complex, boxes: set[complex]):
        self.robot = robot.real * 2 + robot.imag * 1j
        # This represents the lhs of the box and the rhs is inferred by adding 1
        self.boxes = {box.real * 2 + box.imag * 1j for box in boxes}
        self.walls = {wall.real * 2 + wall.imag * 1j for wall in walls} | {wall.real * 2 + 1 + wall.imag * 1j for wall in walls}

    def _move_ud(self, direction: complex):
        """Move the robot in the up/down direction if possible"""
        new_robot_position = self.robot + direction

        moving_boxes = set()
        cursors = {new_robot_position}
        while cursors:
            new_cursors = set()
            for cursor in cursors:
                # If the cursor hits a wall then it will halt movement
                if cursor in self.walls:
                    return

                # Check if the cursor is on the lhs of a box
                if cursor in self.boxes:
                    new_cursors.add(cursor + direction)
                    new_cursors.add(cursor + 1 + direction)  # Add the rhs of box into the new cursors
                    moving_boxes.add(cursor)
                # Check if the cursor is on the rhs of a box
                elif cursor - 1 in self.boxes:
                    new_cursors.add(cursor - 1 + direction)
                    new_cursors.add(cursor + direction)
                    moving_boxes.add(cursor - 1)
            cursors = new_cursors

        # If we reach here, move everything
        self.robot = new_robot_position
        for box in moving_boxes:
            self.boxes.remove(box)
        for box in moving_boxes:
            self.boxes.add(box + direction)

    def _move_r(self, direction: complex):
        """Move the robot in the right direction if possible"""
        new_robot_position = self.robot + direction

        moving_boxes = set()
        cursor = new_robot_position
        while True:
            # If the cursor hits a wall then it will halt movement
            if cursor in self.walls:
                return

            # If the cursor hits the lhs of a box, move the box and skip a square
            if cursor in self.boxes:
                moving_boxes.add(cursor)
                cursor += direction * 2
            else:
                break

        # Move the robot and boxes
        self.robot = new_robot_position
        for box in moving_boxes:
            self.boxes.remove(box)
            self.boxes.add(box + direction)

    def _move_l(self, direction: complex):
        """Move the robot in the left direction if possible"""
        new_robot_position = self.robot + direction

        moving_boxes = set()
        cursor = new_robot_position
        while True:
            # If the cursor hits a wall then it will halt movement
            if cursor in self.walls:
                return

            # If the cursor hits the rhs of a box, move the box and skip a square
            if cursor - 1 in self.boxes:
                moving_boxes.add(cursor - 1)
                cursor += direction * 2
            else:
                break

        # Move the robot and boxes
        self.robot = new_robot_position
        for box in moving_boxes:
            self.boxes.remove(box)
            self.boxes.add(box + direction)

    def move(self, direction: complex):
        """Move the robot in the given direction if possible"""
        match direction:
            case 0 - 1j | 0 + 1j:  # Up or Down
                self._move_ud(direction)
            case 1 + 0j:  # Right
                self._move_r(direction)
            case -1 + 0j:  # Left
                self._move_l(direction)
            case _:
                raise ValueError(f"Invalid move direction: {direction}")

    def GPS_sum(self) -> int:
        """Calculate the GPS sum of the warehouse"""
        return int(sum(box.real + 100 * box.imag for box in self.boxes))

    def print_grid(self):
        """Print the grid of the warehouse"""
        min_x = int(min(box.real for box in self.walls))
        max_x = int(max(box.real for box in self.walls))
        min_y = int(min(box.imag for box in self.walls))
        max_y = int(max(box.imag for box in self.walls))

        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                pos = complex(x, y)
                if pos == self.robot:
                    line += "@"
                elif pos in self.boxes:
                    line += "["
                elif pos - 1 in self.boxes:
                    line += "]"
                elif pos in self.walls:
                    line += "#"
                else:
                    line += "."
            print(line)

def parse(file: TextIO):
    """Parse the plaintext input"""
    grid, movements = file.read().split("\n\n")

    # Init constants
    robot_position = None
    boxes = set()
    walls = set()
    lines = grid.splitlines()

    # Parse the grid
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case "@":
                    robot_position = complex(x, y)
                case "O":
                    boxes.add(complex(x, y))
                case "#":
                    walls.add(complex(x, y))

    assert robot_position is not None, "Robot position not found in the grid"

    warehouse =  Warehouse(
        walls=walls,
        robot=robot_position,
        boxes=boxes
    )

    warehouse_pt2 = Warehouse2(
        walls=walls.copy(),
        robot=robot_position,
        boxes=boxes.copy()
    )

    # Parse the movements
    movements = [move_from_char(char) for char in movements if char in "^v<>"]

    return warehouse, movements, warehouse_pt2

def part_one(warehouse: Warehouse, movements: list[complex]):
    """Solution to part one"""
    for move in movements:
        warehouse.move(move)

    # Return the number of boxes left in the warehouse
    return warehouse.GPS_sum()


def part_two(warehouse: Warehouse2, movements: list[complex]):
    """Solution to part two"""
    for move in movements:
        warehouse.move(move)

    # Return the number of boxes left in the warehouse
    return warehouse.GPS_sum()


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        warehouse, movements, warehouse_pt2 = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(warehouse, movements)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(warehouse_pt2, movements)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
