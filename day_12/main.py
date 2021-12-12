import argparse
import re
from collections import defaultdict
from copy import copy
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List


Node = str
Graph = Dict[Node, Node]


def parse_input(data: Iterable[str]) -> Graph:
    r"""Returns the Graph parsed from data.
    
    Example:

        >>> data = '''start-A
        ... start-b
        ... A-c
        ... A-b
        ... b-d
        ... A-end
        ... b-end'''.split('\n')
        >>> graph = parse_input(data)
        >>> sorted(list(graph.keys()))
        ['A', 'b', 'c', 'd', 'end', 'start']
        >>> sorted(list(graph["start"]))
        ['A', 'b']
        >>> sorted(list(graph["b"]))
        ['A', 'd', 'end', 'start']
    """
    pattern = re.compile("([a-zA-Z]+)-([a-zA-Z]+)")
    graph = defaultdict(set)
    for line in data:
        match = pattern.fullmatch(line.rstrip())
        if not match:
            raise ValueError(f"unable to parse line {repr(line)}")
        # undirected so add both directions
        graph[match[1]].add(match[2])
        graph[match[2]].add(match[1])
    return graph
    

def part1_skip_next(next: Node, lower_cnts: Dict[Node, int]) -> bool:
    return next.islower() and lower_cnts[next] == 1


def part2_skip_next(next: Node, lower_cnts: Dict[Node, int]) -> bool:
    return next.islower() and (
        (lower_cnts[next] == 2) or 
        (lower_cnts[next] == 1 and any([v == 2 for v in lower_cnts.values()]))
    )


def paths(graph: Graph, skip_next: Callable[[Node, Dict[Node, int]], bool]) -> List[List[Node]]:
    r"""Returns paths.

    Example:

        >>> data = '''start-A
        ... start-b
        ... A-c
        ... A-b
        ... b-d
        ... A-end
        ... b-end'''.split('\n')
        >>> graph = parse_input(data)
        >>> for p in sorted(list(paths(graph, part1_skip_next))):
        ...     print(p)
        ['start', 'A', 'b', 'A', 'c', 'A', 'end']
        ['start', 'A', 'b', 'A', 'end']
        ['start', 'A', 'b', 'end']
        ['start', 'A', 'c', 'A', 'b', 'A', 'end']
        ['start', 'A', 'c', 'A', 'b', 'end']
        ['start', 'A', 'c', 'A', 'end']
        ['start', 'A', 'end']
        ['start', 'b', 'A', 'c', 'A', 'end']
        ['start', 'b', 'A', 'end']
        ['start', 'b', 'end']
        >>> print(len(paths(graph, part2_skip_next)))
        36
    """
    stack = [('start', ['start'], defaultdict(int))]
    paths = []
    while stack:
        node, path, lower_cnts = stack.pop()
        if node == 'end':
            paths.append(list(path))
            continue
            
        for next in graph[node]:
            if next == 'start':
                continue   # prevent infinite loops
            elif next != 'end' and skip_next(next, lower_cnts):
                continue
            if next != 'end' and next.islower():
                next_lower_cnts = copy(lower_cnts)
                next_lower_cnts[next] += 1
            else:
                next_lower_cnts = lower_cnts
            stack.append((next, list(path) + [next], next_lower_cnts))
            
    return paths
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    
    with open(args.path, 'r') as f:
        graph = parse_input(f)

    for fn in [part1_skip_next, part2_skip_next]:
        ps = paths(graph, fn)
        if args.debug:
            for p in sorted(list(ps)):
                print(p)
            print()
        else:
            print(len(ps))