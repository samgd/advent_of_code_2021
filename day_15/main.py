"""
Dijkstra's algorithm!

Pythons heap misses the change operation so lets write our own for fun.

On reflection you could probably dynamically generate the grid when searching to speed things up but it's working and correct so moving on.
"""
import argparse
from collections import namedtuple
from copy import copy
from typing import Hashable
from typing import Iterable
from typing import List


Position = namedtuple("Position", ['x', 'y'])


class MinPriorityQueue:
    """A min priority queue with O(logn) insert, pop and change.
    
    Example:

        >>> pq = MinPriorityQueue()
        >>> len(pq)
        0
        >>> vals = list("abcdefgh")
        >>> priorities = [10, 5, 9, 15, 8, 1, 2, 3]
        >>> for v, p in zip(vals, priorities):
        ...     pq.insert(v, p)
        >>> len(pq)
        8
        >>> pq.find('c')
        9
        >>> pq.pop()
        ('f', 1)
        >>> len(pq)
        7
        >>> pq.find('c')
        9
        >>> pq.change('a', 100)
        >>> len(pq)
        7
        >>> [pq.pop() for _ in range(4)]
        [('g', 2), ('h', 3), ('b', 5), ('e', 8)]
        >>> pq.find('a')
        100
        >>> [pq.pop() for _ in range(3)] 
        [('c', 9), ('d', 15), ('a', 100)]
    """
    class _Entry:
        __slots__ = ('priority', 'item')
        def __init__(self, priority, item):
            self.priority = priority
            self.item = item               
    
    def __init__(self):
        self._queue = [] 
        self._pos = {}
        
    def __contains__(self, item) -> bool:
        return item in self._pos
        
    def __len__(self) -> int:
        return len(self._queue)
        
    def _perculate_up(self, index: int) -> int:
        entry = self._queue[index]
        while True:
            if index == 0:
                break   # at root
            parent_idx = (index - 1) // 2
            parent = self._queue[parent_idx]
            if parent.priority <= entry.priority:
                break
            self._queue[parent_idx], self._queue[index] = entry, parent
            self._pos[entry.item] = parent_idx
            self._pos[parent.item] = index
            index = parent_idx
        
    def _perculate_down(self, index: int) -> int:
        while True:
            l_idx, r_idx = 2*index + 1, 2*index + 2
            if len(self._queue) - 1 < l_idx:
                # no children
                break
            min_child, min_idx = self._queue[l_idx], l_idx
            if len(self._queue) - 1 >= r_idx:
                right = self._queue[r_idx]
                if right.priority < min_child.priority:
                    min_child, min_idx = right, r_idx
            if min_child.priority >= self._queue[index].priority:
                break
            entry = self._queue[index]
            self._queue[index], self._queue[min_idx] = min_child, entry
            self._pos[min_child.item], self._pos[entry.item] = index, min_idx
            index = min_idx
        
    def insert(self, item: Hashable, priority: int):
        index = len(self._queue)
        entry = self._Entry(priority, item)
        self._queue.append(entry)
        self._pos[item] = index
        self._perculate_up(index)
            
    def pop(self):
        entry = self._queue[0]
        del self._pos[entry.item]

        if len(self._queue) == 1:
            self._queue.pop()
        else:
            self._queue[0] = self._queue.pop()
            self._pos[self._queue[0].item] = 0
            self._perculate_down(0)
        return entry.item, entry.priority
        
    def change(self, item: Hashable, new_priority: int):
        if item not in self._pos:
            return self.insert(item, new_priority)
        current = self._queue[self._pos[item]]
        prev_priority = current.priority
        current.priority = new_priority
        if new_priority < prev_priority:
            self._perculate_up(self._pos[item])
        elif new_priority > prev_priority:
            self._perculate_down(self._pos[item])
            
    def find(self, item: Hashable) -> int:
        return self._queue[self._pos[item]].priority


def parse_input(data: Iterable[str]) -> List[List[int]]:
    r"""Returns the risk level map from data.
    
    Example:

        >>> data = iter('''123
        ... 456
        ... 789'''.split('\n'))
        >>> parse_input(data)
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [[int(l) for l in line.strip()] for line in data]


def neighbours(p: Position, maxx: int, maxy: int) -> Iterable[Position]:
    """Returns neighbouring positions of p.
    
    Example:

        >>> p = Position(0, 0)
        >>> sorted(list(neighbours(p, 5, 5)))
        [Position(x=0, y=1), Position(x=1, y=0)]
        >>> p = Position(3, 3)
        >>> sorted(list(neighbours(p, 5, 5)))
        [Position(x=2, y=3), Position(x=3, y=2), Position(x=3, y=4), Position(x=4, y=3)]
        >>> p = Position(5, 5)
        >>> sorted(list(neighbours(p, 5, 5)))
        [Position(x=4, y=5), Position(x=5, y=4)]
    """
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not (dx == 0 or dy == 0):
                continue   # skip diagonals
            if dx == 0 and dy == 0:
                continue   # neighbours only
            nx, ny = p.x + dx, p.y + dy
            if nx < 0 or nx > maxx or ny < 0 or ny > maxy:
                continue   # out of bounds
            yield Position(nx, ny)


def lowest_risk(grid: List[List[int]], start: Position, end: Position) -> int:
    r"""Returns the risk of the path of lowest risk.

    Example:

        >>> grid = parse_input(iter(
        ... '''123
        ... 119
        ... 311'''.split('\n')))
        >>> start = Position(0, 0)
        >>> end = Position(2, 2)
        >>> lowest_risk(grid, start, end)
        4
    """
    maxx, maxy = len(grid[0]) - 1, len(grid) - 1
    pq = MinPriorityQueue()
    pq.change(start, 0)
    visited = set()

    while pq:
        pos, risk = pq.pop()
        visited.add(pos)
        if pos == end:
            return risk
        for neighbour in neighbours(pos, maxx, maxy):
            if neighbour in visited:
                continue
            path_risk = risk + grid[neighbour.y][neighbour.x]
            if neighbour not in pq or path_risk < pq.find(neighbour):
                pq.change(neighbour, path_risk)

    raise ValueError("failed to find path to end")
    

def expand(grid: List[List[int]], n: int = 5) -> List[List[int]]:
    new_grid = []
    # extend horizontally
    for row in grid:
        new_row = copy(row)
        for i in range(1, n):
            for e in row:
                new_row.append(1 + ((e + i - 1) % 9))
        new_grid.append(new_row)

    # extend vertically
    ext_grid = []
    for i in range(0, n):
        for row in new_grid:
            ext_grid.append([1 + ((e + i - 1) % 9) for e in row])

    return ext_grid
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    
    with open(args.path, 'r') as f:
        grid = parse_input(f)
        
    start = Position(0, 0)
    end = Position(len(grid[0]) - 1, len(grid) - 1)

    print(lowest_risk(grid, start, end))

    grid = expand(grid)
    end = Position(len(grid[0]) - 1, len(grid) - 1)
    print(lowest_risk(grid, start, end))