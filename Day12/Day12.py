"""AoC :: Day 12"""
import time
from typing import TextIO
DAY = 12
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


class Garden(dict[complex, str]):
    """
    A Garden Plot
    
    keys are coordinates and values are crop codes
    """
    DIRECTIONS = (
        complex( 1, 0),
        complex( 0,-1),
        complex(-1, 0),
        complex( 0, 1),
    )

    def neighbours(self, pos: complex):
        """generate the neighbouring crops"""
        return ((pos + direction, self.get(pos + direction, None)) for direction in self.DIRECTIONS)

    def corners(self, position: complex, area: set[complex]):
        """Count the number of corners a position represents on a given an area"""
        corners = 0
        offset_directions = self.DIRECTIONS[1:] + self.DIRECTIONS[:1]
        for d1, d2 in zip(self.DIRECTIONS, offset_directions):
            if (position + d1 not in area) and (position + d2 not in area):
                corners += 1
            elif (position + d1 in area) and (position + d2 in area) and (position + d1 + d2 not in area):
                corners += 1
        return corners

    def flood_fill(self, position: complex):
        """Given a position, flood fill to find the connected component it belongs"""
        crop = self[position]
        connected_component = {position}
        new_positions = {position}
        while new_positions:
            new_positions = {
                p for pos in new_positions for p, c in self.neighbours(pos) if (c == crop) and (p not in connected_component)
            }
            connected_component |= new_positions
        return connected_component

    def prices(self):
        """Calculate the price and price with discount simultaneously"""
        # Init
        consider = set(self)
        price = price_with_discount = 0

        # Loop until all points in the Garden have been considered
        while consider:
            position = consider.pop()
            crop = self[position]
            connected_component = self.flood_fill(position)
            area = len(connected_component)
            # Calculate the perimeter and number of corners
            perimeter = sum(
                1 for pos in connected_component for _, c in self.neighbours(pos) if c != crop
            )
            corners = sum(self.corners(pos, connected_component) for pos in connected_component)
            # Update the price
            price += area * perimeter
            price_with_discount += area * corners
            # Remove the connected component from consideration
            consider -= connected_component

        # Return both answers for part one and two
        return price, price_with_discount


def parse(file: TextIO):
    """Parse the plaintext input"""
    garden = Garden()
    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row.strip()):
            garden[complex(x, y)] = char
    return garden

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        garden = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One + Two ::")
    t1 = -time.time()
    a1, a2 = garden.prices()
    t1 += time.time()
    print(f"Part One Answer: {a1}")
    print(f"Part Two Answer: {a2}")
    print(f"runtime: {t1: .4f}s")

    print(f":: total runtime: {t0+t1: .4f}s ::")


if __name__ == "__main__":
    main()
