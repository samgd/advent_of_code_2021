"""
Planning notes:

Given a number, we'll want a way to find out the [(board, position)] to mark it.

Given a board, we'll want an efficient way to test if any of the rows or columns are marked.

Suggests two data structures:

    1. A dict of `number -> (board, pos)` for O(1) lookups.
    2. A bit-board to represent the board. We can use int32, numpy and wrap in a class to hide implementation.
"""
import argparse
import re
from collections import defaultdict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Tuple

import numpy as np


class Board:
    def __init__(self, board: List[List[int]]):
        # each board entry maps to bit at pos 2**i, where i is:
        #
        #  0  1  2  3  4
        #  5  6  7  8  9
        # 10 11 12 13 14
        # 15 16 17 18 19
        # 20 21 22 23 24
        self._marked = np.int32(0)
        self.board = board

    def mark(self, row: int, col: int) -> None:
        """
        Example:

            >>> b = Board(range(5*i, 5*(i+1)) for i in range(5))
            >>> b.is_marked(row=3, col=2)
            False
            >>> b.mark(row=3, col=2)
            >>> b.is_marked(row=3, col=2)
            True
        """
        self._marked |= 2**(5*row + col)

    def is_marked(self, row: int, col: int) -> bool:
        return bool(self._marked & 2**(5*row + col))

    def win(self) -> bool:
        """Returns True if the board has won.

        Example:

            >>> b = Board(list(range(5*i, 5*(i+1)) for i in range(5)))
            >>> b.win()
            False
            >>> for i in range(5):
            ...     b.mark(row=0, col=i)
            >>> b.win()
            True
        """
        row = 0b11111
        col = 0b00_00000_00001_00001_00001_00001_00001
        return np.any([
            (self._marked & row) == row,
            (self._marked & (row << 5)) == (row << 5),
            (self._marked & (row << 10)) == (row << 10),
            (self._marked & (row << 15)) == (row << 15),
            (self._marked & (row << 20)) == (row << 20),
            (self._marked & col) == col,
            (self._marked & (col << 1)) == (col << 1),
            (self._marked & (col << 2)) == (col << 2),
            (self._marked & (col << 3)) == (col << 3),
            (self._marked & (col << 4)) == (col << 4)
        ])

    def __repr__(self) -> str:
        """
        
        Example:

            >>> b = Board([list(range(5*i, 5*(i + 1))) for i in range(5)])
            >>> b.mark(row=4, col=1)
            >>> b
            [0, 1, 2, 3, 4]
            [5, 6, 7, 8, 9]
            [10, 11, 12, 13, 14]
            [15, 16, 17, 18, 19]
            [20, 21, 22, 23, 24]
            <BLANKLINE>
            [0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0]
            [0, 1, 0, 0, 0]
        """
        s = []

        for row in self.board:
            s.append(str(row))
        s.append('')
        for row_idx in range(5):
            s_row = ['[']
            for col_idx in range(5):
                s_row.append(str(int((self.is_marked(row_idx, col_idx)))))
                if col_idx < 4:
                    s_row.append(', ')
            s_row.append("]")
            s.append(''.join(s_row))

        return "\n".join(s)


def parse_input(data: Iterable[str]) -> Tuple[List[int], List[Board]]:
    """Returns the game draws and boards parsed from data."""
    line_pattern = re.compile(("[ ]*(\d+)" * 5) + '\s*')
    boards = []
    draws = [int(n) for n in data.readline().split(',')]
    while data.readline():
        rows = []
        for i in range(5):
            row_str = data.readline()
            match = line_pattern.fullmatch(row_str)
            rows.append([int(match[i]) for i in range(1, 6)])
        assert len(rows) == 5
        boards.append(Board(rows))
    return draws, boards


def gen_boards_with(boards: List[Board]) -> Mapping[int, Tuple[Board, Tuple[int, int]]]:
    """Returns a list of (board, (row, col)) containing a number."""
    boards_with = defaultdict(list)
    for board in boards:
        for row_idx, row in enumerate(board.board):
            for col_idx, val in enumerate(row):
                boards_with[val].append((board, (row_idx, col_idx)))
    return boards_with


def score(board: Board) -> int:
    return sum([
        n 
        for row_idx, row in enumerate(board.board)
        for col_idx, n in enumerate(row)
        if not board.is_marked(row_idx, col_idx)
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        draws, boards = parse_input(f)
        
    boards_with = gen_boards_with(boards)
    has_won = set()
    for n in draws:
        for board, (row, col) in boards_with[n]:
            board.mark(row, col)
            if board.win():
                if len(has_won) == 0:
                    print(f"part 1: {score(board) * n}")
                has_won.add(board)
                if len(has_won) == len(boards):
                    print(f"part 2: {score(board) * n}")
                    exit()
        del boards_with[n]   # duplicate draws are a noop

