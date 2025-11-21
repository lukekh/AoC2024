"""
AoC :: Day 16 - AI Assisted

I lazily (sorry Eric) got AI to assist in refactoring my solution to Day 16.
"""
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import heapq
import logging
import time
from typing import Literal, Optional, TextIO
DAY = 16
INPUT_FILE = 'Day{day}/Day{day}.in'.format(day=str(DAY).zfill(2))

logging.basicConfig(level=logging.INFO)

class Direction(Enum):
    """Cardinal directions"""
    NORTH = 0-1j
    EAST = 1+0j
    SOUTH = 0+1j
    WEST = -1+0j

    __order__ = 'NORTH EAST SOUTH WEST'

    def left(self):
        """Turn left 90 degrees"""
        return Direction(self.value * -1j)
    
    def right(self):
        """Turn right 90 degrees"""
        return Direction(self.value * 1j)

@dataclass
class Vertex:
    """
    A vertex within the maze
    
    Each vertex has a position (x,y) but we need to also track
    the direction from which we arrived at this vertex
    """
    z: complex
    direction: Direction
    char: Literal[".", "S", "E"]

    def __hash__(self):
        return hash((self.z, self.direction))
    
    @classmethod
    def parse_char(cls, x: int, y: int, char: str):
        """parse a char into vertices"""
        match char:
            case "." | "E":
                return (
                    cls(complex(x, y), d, char) for d in Direction
                )
            case "S":
                ds_nuts = (".", "S", ".", ".")
                return (
                    cls(complex(x, y), d, c) for d, c in zip(Direction, ds_nuts)
                )
            case _:
                raise ValueError(f"Invalid char for vertex: {char}")


@dataclass
class Edge:
    """
    An edge between two junctions in the maze
    """
    start: complex
    end: complex
    weight: int
    start_dir: Direction
    end_dir: Direction
    tiles: set[complex]

    def __hash__(self):
        return hash((self.start, self.end, self.start_dir, self.end_dir))

class Maze:
    """A maze of vertices and edges"""

    def __init__(self, turn_cost: int = 1000, step_cost: int = 1):
        self.grid: set[complex] = set()
        self.start: Optional[complex] = None
        self.end: Optional[complex] = None
        
        # Graph: node -> list[Edge]
        self.adj: dict[complex, list[Edge]] = defaultdict(list)

        self.TURN_COST = turn_cost
        self.STEP_COST = step_cost

    def __contains__(self, pos: complex):
        return pos in self.grid
    
    def build_graph(self):
        """Build the graph by walking from junctions"""
        # 1. Identify all junctions (nodes)
        # A junction is S, E, or any point with > 2 neighbors
        junctions = set()
        if self.start: junctions.add(self.start)
        if self.end: junctions.add(self.end)

        for pos in self.grid:
            neighbors = 0
            for d in (1, -1, 1j, -1j):
                if (pos + d) in self.grid:
                    neighbors += 1
            if neighbors > 2:
                junctions.add(pos)
        
        logging.debug(f"Found {len(junctions)} junctions")

        # 2. Walk from each junction in each direction
        for start_node in junctions:
            for start_dir in Direction:
                # Check if we can move in this direction
                if (start_node + start_dir.value) not in self.grid:
                    continue
                
                # Walk until next junction or dead end
                curr = start_node + start_dir.value
                dist = 1
                turns = 0
                curr_dir = start_dir
                path_tiles = {start_node, curr}

                while curr not in junctions:
                    # Find next step
                    # We can't reverse, so check 3 directions
                    # Actually, since it's a corridor (neighbors <= 2), there is only one way forward
                    # unless it's a dead end.
                    
                    # Check straight
                    if (curr + curr_dir.value) in self.grid:
                        curr += curr_dir.value
                        dist += 1
                        path_tiles.add(curr)
                        continue
                    
                    # Check turns
                    found_next = False
                    for turn in (curr_dir.left(), curr_dir.right()):
                        if (curr + turn.value) in self.grid:
                            curr += turn.value
                            dist += 1
                            turns += 1
                            curr_dir = turn
                            path_tiles.add(curr)
                            found_next = True
                            break
                    
                    if not found_next:
                        # Dead end
                        break
                
                if curr in junctions:
                    # We found a connection
                    # Edge: start_node -> curr
                    # We record the arrival direction so we can calculate turn cost at the next node
                    # We also need the departure direction (start_dir) to calculate the turn cost at THIS node
                    weight = (dist * self.STEP_COST) + (turns * self.TURN_COST)
                    self.adj[start_node].append(Edge(start_node, curr, weight, start_dir, curr_dir, path_tiles))
                    # Wait, Edge definition needs update to store start_dir if we want to be explicit,
                    # but actually we can infer it? No, we iterate over edges.
                    # Let's add start_dir to Edge.

    @classmethod
    def parse(cls, file: TextIO):
        """Parse a maze from a file"""
        maze = cls()
        grid = [list(line.strip()) for line in file.readlines()]

        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char != "#":
                    z = complex(x, y)
                    maze.grid.add(z)
                    if char == "S":
                        maze.start = z
                    elif char == "E":
                        maze.end = z
        
        maze.build_graph()
        return maze


def solve(inputs: Maze):
    """Solve the maze using Dijkstra and return min_cost and parents map"""
    # Dijkstra
    # State: (cost, position, direction)
    # Start facing East
    start_z = inputs.start
    start_dir = Direction.EAST

    import itertools
    counter = itertools.count()
    
    pq = [(0, next(counter), start_z, start_dir)]
    visited = {} # (pos, dir) -> cost
    parents = defaultdict(list) # (pos, dir) -> list[(prev_pos, prev_dir, edge)]

    min_cost = float('inf')
    end_states = []

    while pq:
        cost, _, curr, d = heapq.heappop(pq)

        if cost > visited.get((curr, d), float('inf')):
            continue
        visited[(curr, d)] = cost

        if curr == inputs.end:
            if cost < min_cost:
                min_cost = cost
                end_states = [(curr, d)]
            elif cost == min_cost:
                end_states.append((curr, d))
            continue
        
        # Explore edges
        if curr in inputs.adj:
            for edge in inputs.adj[curr]:
                turn_cost = 0
                if d == edge.start_dir:
                    turn_cost = 0
                elif d.left() == edge.start_dir or d.right() == edge.start_dir:
                    turn_cost = inputs.TURN_COST
                else:
                    # 180 degree turn
                    turn_cost = inputs.TURN_COST * 2
                
                new_cost = cost + turn_cost + edge.weight
                
                # If we found a better path, clear parents
                if new_cost < visited.get((edge.end, edge.end_dir), float('inf')):
                    visited[(edge.end, edge.end_dir)] = new_cost
                    parents[(edge.end, edge.end_dir)] = [(curr, d, edge)]
                    heapq.heappush(pq, (new_cost, next(counter), edge.end, edge.end_dir))
                # If we found an equal path, add parent
                elif new_cost == visited.get((edge.end, edge.end_dir), float('inf')):
                    parents[(edge.end, edge.end_dir)].append((curr, d, edge))

    return min_cost, parents, end_states

def part_one(inputs: Maze):
    """Solution to part one"""
    print(f"Graph has {len(inputs.adj)} junctions")
    min_cost, _, _ = solve(inputs)
    return min_cost


def part_two(inputs: Maze):
    """Solution to part two"""
    min_cost, parents, end_states = solve(inputs)
    
    # Backtrack
    tiles = set()
    queue = end_states[:]
    seen_states = set(end_states)
    
    while queue:
        curr, d = queue.pop(0)
        tiles.add(curr)
        
        if (curr, d) in parents:
            for prev_pos, prev_dir, edge in parents[(curr, d)]:
                tiles.update(edge.tiles)
                if (prev_pos, prev_dir) not in seen_states:
                    seen_states.add((prev_pos, prev_dir))
                    queue.append((prev_pos, prev_dir))
                    
    return len(tiles)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2024 -- Day {DAY} ::")

    # Parse inputs
    print(":: Parsing Inputs ::")
    t0 = -time.time()
    with open(INPUT_FILE, encoding="utf8") as f:
        inputs = Maze.parse(f)
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
