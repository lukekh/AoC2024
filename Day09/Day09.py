"""AoC :: Day 9"""
import time
from typing import TextIO
DAY = 9
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def parse(file: TextIO):
    """Parse the plaintext input"""
    return file.read().strip()


def triangle(start: int, stop: int):
    """return the triangle number starting and stopping somewhere"""
    n = stop - start
    return n * start + n * (n - 1) // 2


def part_one(diskmap: str):
    """Solution to part one"""
    # Init for loop
    checksum = 0
    position = file_id = backfill_size = 0
    backfill_id = (len(diskmap) + 1) // 2
    backfill_size = 0
    # Flip between File and Gap logic
    for i, char in enumerate(diskmap):
        # File logic
        if not i % 2:
            file_id = i // 2
            if file_id == backfill_id:
                k = triangle(position, position + backfill_size)
                checksum += k * backfill_id
                return checksum
            k = triangle(position, alloc := position + int(char))
            checksum += file_id * k
            position =  alloc
        # Gap logic
        else:
            # Skip if there is no gap to be filled
            gap = int(char)
            while gap:
                # If we're out of file to allocate from previous steps (or init) then
                # get the next file from the end
                while backfill_size == 0:
                    backfill_id -= 1
                    backfill_size = int(diskmap[backfill_id * 2])

                b = min(gap, backfill_size)
                k = triangle(position, position + b)
                checksum += backfill_id * k
                backfill_size -= b
                gap -= b
                position += b

    return checksum


def part_two(diskmap: str):
    """Solution to part two"""
    memory = sum(int(i) for i in diskmap)

    checksum = 0
    position = file_id = 0
    backfill_id = N = (len(diskmap) + 1) // 2
    backfill_size = 0
    allocated_files = set()

    for i, char in enumerate(diskmap):
        # File logic
        if not i % 2:
            file_id = i // 2
            if file_id in allocated_files:
                position += int(char)
                continue

            allocated_files.add(file_id)
            file_size = int(char)
            k = triangle(position, position + file_size)
            checksum += file_id * k
            position += file_size
        # Space filling logic
        else:
            gap = int(char)
            # Skip if there is no gap to be filled
            if int(char) == 0:
                continue

            while gap:
                if position > memory:
                    return checksum
                # This time iterate over all file_ids backwards until the gap is filled
                for backfill_id in range(N-1, -1, -1):
                    if (backfill_id not in allocated_files) and (int(diskmap[backfill_id * 2]) <= gap):
                        allocated_files.add(backfill_id)
                        backfill_size = int(diskmap[backfill_id * 2])

                        k = triangle(position, position + backfill_size)
                        checksum += backfill_id * k
                        position += backfill_size
                        gap -= backfill_size
                        break
                else:
                    position += gap
                    break

    return checksum


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
