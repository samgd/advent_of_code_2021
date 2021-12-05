import argparse
import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int


@dataclass
class Line:
    start: Position
    end: Position

    def __iter__(self) -> Iterable[Position]:
        """Returns an Iterable over all Positions on the line.

        Example:

            >>> line = Line(
            ...     start=Position(0, 2), end=Position(0, 4)
            ... )
            >>> list(iter(line))
            [Position(x=0, y=2), Position(x=0, y=3), Position(x=0, y=4)]
            >>> line = Line(Position(1, 1), Position(1, 1))
            >>> list(iter(line))
            [Position(x=1, y=1)]

        """
        if self.start == self.end:
            yield self.start
            return

        if self.start.x == self.end.x:
            x_iter = itertools.repeat(self.start.x)
        else:
            x_dir = 1 if self.start.x <= self.end.x else -1
            x_iter = range(self.start.x, self.end.x + x_dir, x_dir)

        if self.start.y == self.end.y:
            y_iter = itertools.repeat(self.start.y)
        else:
            y_dir = 1 if self.start.y <= self.end.y else -1
            y_iter = range(self.start.y, self.end.y + y_dir, y_dir)
        
        for (x, y) in zip(x_iter, y_iter):
            yield Position(x, y)


def parse_lines(data: Iterable[str]) -> Iterable[Line]:
    r"""Returnes Lines parsed from data.

    Example:
        >>> data = '''0,9 -> 5,9
        ... 8,0 -> 0,8
        ... 9,4 -> 3,4'''
        >>> data = data.split('\n')
        >>> expected = [
        ...     Line(Position(0, 9), Position(5, 9)),
        ...     Line(Position(8, 0), Position(0, 8)),
        ...     Line(Position(9, 4), Position(3, 4))
        ... ]
        >>> list(parse_lines(data)) == expected
        True
    """
    pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)\n?")
    lines = []
    for line in data:
        match = pattern.fullmatch(line)
        if not match:
            raise ValueError(f"failed to parse {repr(line)}")
        yield Line(
            start=Position(int(match[1]), int(match[2])), 
            end=Position(int(match[3]), int(match[4]))
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        lines = parse_lines(f)
        is_hor_vert = lambda l: l.start.x == l.end.x or l.start.y == l.end.y
        counts = defaultdict(int)
        hor_vert_counts = defaultdict(int)
        for line in lines:
            hor_vert = is_hor_vert(line)
            for pos in line:
                counts[pos] += 1
                if hor_vert:
                    hor_vert_counts[pos] += 1

        n_hor_vert_overlap = len([
            p for p, cnt in hor_vert_counts.items()
            if cnt >= 2
        ])
        print(f"overlapping horzontal or vertical line positions: {n_hor_vert_overlap}")

        n_overlap = len([
            p for p, cnt in counts.items()
            if cnt >= 2
        ])
        print(f"overlapping positions: {n_overlap}")