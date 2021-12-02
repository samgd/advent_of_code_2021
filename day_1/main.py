import argparse
from itertools import islice
from pathlib import Path
from typing import Any, Iterable, Tuple


def read_depths(path: Path) -> Iterable[int]:
    with open(path, "r") as f:
        for line in f:
            yield int(line)


def n_larger(depths: Iterable[int]) -> int:
    larger = 0
    d_iter = iter(depths)
    try:
        current = next(d_iter)
    except StopIteration:
        return larger
    for n in d_iter:
        larger += int(n > current)
        current = n
    return larger


def window(seq: Iterable[Any], n: int = 2) -> Iterable[Tuple[Any]]:
    """Returns a sliding window (of width n) over data from the iterable.

    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...        
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    print(f"part 1: {n_larger(read_depths(args.file))}")

    smoothed = [sum(w) for w in window(read_depths(args.file), 3)]

    print(f"part 2: {n_larger(smoothed)}")