"""AoC :: Day 11"""
import time
from typing import TextIO
DAY = 11
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


class Pebbles(dict[int, int]):
    """
    Plutonian pebbles
    
    keys are the engraved numbers, values are the number of pebbles
    """
    def increase(self, item: int, val: int):
        """
        increase the value for a given item
        """
        self[item] = self.get(item, 0) + val


    def blink(self):
        """
        Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:
        - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        - If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
          The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. 
          (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
        """
        next_state = Pebbles()
        for key, val in self.items():
            if key == 0:
                next_state.increase(1, self[0])
            elif not (i := len(digits := str(key))) % 2:
                next_state.increase(int(digits[:i//2]), val)
                next_state.increase(int(digits[i//2:]), val)
            else:
                next_state.increase(key * 2024, val)
        return next_state


def parse(file: TextIO):
    """Parse the plaintext input"""
    stones = file.read().strip().split(" ")
    return Pebbles({
        int(i): stones.count(i) for i in set(stones)
    })


def part_one(pebbles: Pebbles, blinks: int = 25):
    """Solution to part one"""
    for _ in range(blinks):
        pebbles = pebbles.blink()
    return sum(pebbles.values()), pebbles


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
    a1, outputs = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    # Do 50 more steps on top of part one
    a2, _ = part_one(outputs, 50)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
