import argparse
import re
from collections import namedtuple
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple


Coord = namedtuple("Coord", ['x', 'y'])
Dots = Set[Coord]
Fold = namedtuple("Fold", ['axis', 'line'])


def parse_input(data: Iterable[str]) -> Tuple[Dots, List[Fold]]:
    r"""Parses Dots and Folds from input data.

    Example:
    
        >>> data = '''6,10
        ... 0,2
        ... 9,3
        ... 
        ... fold along y=7
        ... fold along x=5'''.split('\n')
        >>> dots, folds = parse_input(iter(data))
        >>> expected = {
        ...     Coord(x, y) for x, y in [(6, 10), (0, 2), (9, 3)]
        ... }
        >>> expected == dots
        True
        >>> folds == [Fold('y', 7), Fold('x', 5)]
        True
    """ 
    coord_pattern = re.compile("(\d+),(\d+)")
    fold_pattern = re.compile("fold along ([xy])=(\d+)")
    dots = set()
    folds = []
    while True:
        line = next(data).rstrip()
        if not line:
            break
        match = coord_pattern.fullmatch(line)
        if not match:
            raise ValueError(f"unknown line {line}")
        dots.add(Coord(int(match[1]), int(match[2])))
        
    for line in data:
        match = fold_pattern.fullmatch(line.rstrip())
        if not match:
            raise ValueError(f"unknown line {line}")
        folds.append(Fold(match[1], int(match[2])))
        
    return dots, folds


def fold(dots: Dots, fold: Fold) -> Dots:
    r"""Returns dots after performing fold.
    
    Example:
    
        >>> data = '''0,2
        ... 2,1
        ... 1,0
        ...
        ... fold along y=1
        ... fold along x=1'''.split('\n')
        >>> dots, folds = parse_input(iter(data))
        >>> print(folds)
        [Fold(axis='y', line=1), Fold(axis='x', line=1)]
        >>> dots = fold(dots, folds[0])
        >>> dots == {Coord(0, 0), Coord(1, 0), Coord(2, 1)}
        True
        >>> dots = fold(dots, folds[1])
        >>> dots == {Coord(0, 0), Coord(1, 0), Coord(0, 1)}
        True
    """
    new_dots = set()
    for dot in dots:
        x, y = dot.x, dot.y
        if fold.axis == 'x' and x > fold.line:
            x = fold.line - (dot.x - fold.line)
        elif fold.axis == 'y' and y > fold.line:
            y = fold.line - (dot.y - fold.line)
        new_dots.add(Coord(x, y))
    return new_dots
    

def display(dots: Dots) -> None:
    max_x = max([d.x for d in dots])
    max_y = max([d.y for d in dots])
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if Coord(x, y) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    
    with open(args.path, 'r') as f:
        dots, folds = parse_input(f)
        
    for i, f in enumerate(folds):
        dots = fold(dots, f)
        if i == 0:
            print(f"part 1: {len(dots)}")
            
    display(dots)