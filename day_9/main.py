import argparse
import itertools
from collections import deque
from functools import reduce
from operator import mul
from typing import Iterable
from typing import List
from typing import Tuple


def parse_input(data: Iterable[str]) -> List[List[int]]:
    r"""Returns the heightmap for data.

    Example:

        >>> data = '''2199943210
        ... 3987894921'''.split('\n')
        >>> parse_input(data)
        [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0], [3, 9, 8, 7, 8, 9, 4, 9, 2, 1]]

    """
    return [[int(h) for h in line.rstrip()] for line in data]


def neighbours(height_map: List[List[int]], position: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    """Returns all neighbours at position in height_map."""
    x, y = position
    for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        if not any([dx == 0, dy == 0]):
            # skip diagonals
            continue
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= len(height_map[0]):
            continue
        if ny < 0 or ny >= len(height_map):
            continue
        yield (nx, ny), height_map[ny][nx]


def low_points(height_map: List[List[int]]) -> List[Tuple[Tuple[int, int], int]]:
    r"""Returns the low points ((x, y), height) in height_map.

    Example:

        >>> height_map = parse_input('''2199943210
        ... 3987894921
        ... 9856789892
        ... 8767896789
        ... 9899965678'''.split('\n'))
        >>> low_points(height_map)
        [((1, 0), 1), ((9, 0), 0), ((2, 2), 5), ((6, 4), 5)]
    """
    points = []
    for y, row in enumerate(height_map):
        for x, col in enumerate(row):
            low_point = True
            for _, val in neighbours(height_map, (x, y)): 
                low_point &= val > col
            if low_point:
                points.append(((x, y), col))
    return points
    

def basin_size(height_map: List[List[int]], low_point: Tuple[Tuple[int, int], int]) -> int:
    r"""Returns the size of the basin at low_point.

    Example:

        >>> height_map = parse_input('''2199943210
        ... 3987894921
        ... 9856789892
        ... 8767896789
        ... 9899965678'''.split('\n'))
        >>> lps = low_points(height_map)
        >>> [basin_size(height_map, lp) for lp in lps]
        [3, 9, 14, 9]
    """
    # do a BFS out from low_point
    visited = set()
    frontier = deque([low_point])
    while len(frontier) != 0:
        current = frontier.popleft()
        visited.add(current)
        for neighbour in neighbours(height_map, current[0]):
            (x, y), val = neighbour
            if neighbour in visited or val == 9 or val <= current[1]:
                continue
            frontier.append(neighbour)
    return len(visited)
            
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        height_map = parse_input(f)

    lps = low_points(height_map)
    print(f"risk sum: {sum([lp[1] + 1 for lp in lps])}")
    
    basin_sizes = [basin_size(height_map, lp) for lp in lps] 
    top_three = sorted(basin_sizes)[-3:]
    print(f"largest 3 basin product: {reduce(mul, top_three, 1)}")