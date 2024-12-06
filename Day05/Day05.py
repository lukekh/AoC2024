"""AoC :: Day 5"""
import time
from typing import TextIO
DAY = 5
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))


def parse(file: TextIO):
    """Parse the plaintext input"""
    page_ordering_rules, update_spec = file.read().split("\n\n")

    rules: dict[int, set] = {}

    for line in page_ordering_rules.split("\n"):
        x, y = line.split("|")
        if int(x) in rules:
            rules[int(x)].add(int(y))
        else:
            rules[int(x)] = {int(y)}
    updates = [[int(n) for n in line.split(",")] for line in update_spec.split("\n") if line]

    return rules, updates


def valid(rules: dict[int, set[int]], update: list[int]):
    """Check if an update is correctly ordered"""
    for i, n in enumerate(update[1:], start=1):
        if rules.get(n, set()) & set(update[:i]):
            return False
    return True

def part_one(rules: dict[int, set], updates: list[list[int]]):
    """
    Solution to part one
    
    Return the invalid updates since they're relevant to part two
    """
    s, invalid_updates = 0, []
    for update in updates:
        if valid(rules, update):
            s += update[len(update)//2]
        else:
            invalid_updates.append(set(update))
    return s, invalid_updates


def median(rules: dict[int, set[int]], update: set[int], k: int):
    """
    Return the k_th ordered element of this set given the rules
    """
    candidate = update.pop()
    # If this was the last element in update, it must be the k_th element by elimination
    if not update:
        return candidate
    # Else, find the elements that are greater than the candidate using rules
    gt_candidate = update - rules.get(candidate, set())
    # The elements less that the candidate are whatever remains from the update
    lt_candidate = update - gt_candidate

    N = len(lt_candidate)
    # If there are exactly N elements less than the candidate, we've found the median
    if N == k:
        return candidate
    # If there are too many elements less than the candidate, we look for the k_th element of lt_candidate
    if k < N:
        return median(rules, lt_candidate, k)
    # Otherwise, the k_th element is in gt_candidate
    # We subtract N + 1 from k since they're out of consideration
    return median(rules, gt_candidate, k - N - 1)


def part_two(rules: dict[int, set], invalid_updates: list[set[int]]):
    """Solution to part two"""
    return sum(median(rules, update, len(update)//2) for update in invalid_updates)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        rules, updates = parse(f)
    t0 += time.time()
    print(f"runtime: {t0: .4f}s")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, invalid_updates = part_one(rules, updates)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(rules, invalid_updates)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t0+t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
