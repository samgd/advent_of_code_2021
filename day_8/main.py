"""
Probably the most verbous and difficult to parse AOC to date. Notes trying to work out what is going on:

The display contains *four* seven-segment displays.

Segments are identified through a-g. Signals turn segments on/off.

    --signal--> segment

Each of the 4 displays is mixed up differently, but they all use the same signals. In other words, signal b might be on, but this may turn different segments on in each display.

Input: Set of 10 signal patterns and a set of 4 segments.
"""
import argparse
import itertools
import re
from collections import defaultdict
from collections import namedtuple
from typing import Dict
from typing import Iterable
from typing import List


Pattern = str
Entry = namedtuple("Entry", ["signal", "output"])


def parse_input(data: Iterable[str]) -> List[Entry]:
    r"""Returns the list of entries parsed from input lines.

    Example:

        >>> lines = '''\
        ... be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
        ... edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc'''
        >>> for e in parse_input(lines.split('\n')):
        ...     print(e)
        Entry(signal=('be', 'cfbegad', 'cbdgef', 'fgaecd', 'cgeb', 'fdcge', 'agebfd', 'fecdb', 'fabcd', 'edb'), output=('fdgacbe', 'cefdb', 'cefbgd', 'gcbe'))
        Entry(signal=('edbfga', 'begcd', 'cbg', 'gc', 'gcadebf', 'fbgde', 'acbgfd', 'abcde', 'gfcbed', 'gfec'), output=('fcgedb', 'cgb', 'dgebacf', 'gc'))
    """
    pattern = re.compile(
        ("([a-g]+) " * 10) +
        "\| " +
        ("([a-g]+) ?" * 4)
    )
    entries = []
    for line in data:
        line = line.rstrip()
        p = pattern.fullmatch(line)
        if p is None:
            raise ValueError(f"failed to match {line}")
        groups = p.groups()
        entries.append(Entry(groups[:10], groups[10:]))

    return entries


def count_unique(entries: List[Entry]) -> int:
    """Returns the number of output entries that are a 1, 4, 7 or 8."""
    n = 0
    for entry in entries:
        for v in entry.output:
            if len(v) in [2, 4, 3, 7]:
                n += 1
    return n


def decode(entry: Entry) -> int:
    """Returns the decoded output int.
    
    Example:

        >>> entry = Entry(
        ...     signal=["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"],
        ...     output=["cdfeb", "fcadb", "cdfeb", "cdbaf"]
        ... )
        >>> decode(entry)
        5353
    """
    l = {len(s): set(s) for s in entry.signal} 
    num = ""
    for value in entry.output:
        n_segments = len(value)
        n_common_4 = len(l[4] & set(value))
        n_common_1 = len(l[2] & set(value))

        if n_segments == 2:
            num += "1"
        elif n_segments == 3:
            num += "7"
        elif n_segments == 4:
            num += "4"
        elif n_segments == 7:
            num += "8"
        elif n_segments == 5:
            if n_common_4 == 2:
                num += "2"
            elif n_common_4 == 3 and n_common_1 == 1:
                num += "5"
            elif n_common_4 == 3 and n_common_1 == 2:
                num += "3" 
            else:
                raise ValueError("fail 5", n_segments, n_common_4, n_common_1)
        elif n_segments == 6:
            if n_common_4 == 4:
                num += "9"
            elif n_common_4 == 3 and n_common_1 == 1:
                num += "6"
            elif n_common_4 == 3 and n_common_1 == 2:
                num += "0"
            else:
                raise ValueError("fail 6")
        else:
            raise ValueError("fail")
    return int(num)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        entries = parse_input(f)

    print(f"part 1: {count_unique(entries)}")

    print(f"part 2: {sum([decode(entry) for entry in entries])}")
