import argparse
import re
from collections import namedtuple


Target = namedtuple("Target", ["x_min", "x_max", "y_min", "y_max"])


def parse_input(data: str) -> Target:
    pattern = re.compile(
        r"target area: "
        r"x=(-?[0-9]+)[.]{2}(-?[0-9]+), "
        r"y=(-?[0-9]+)[.]{2}(-?[0-9]+)"
    )
    match = pattern.fullmatch(data)
    if not match:
        raise ValueError(f"failed to parse: {repr(data)}")
    return Target(*[int(b) for b in match.groups()])


def max_height(target: Target) -> int:
    """Returns the max height reachable whilst landing in target.
    
    Example:

        >>> target = Target(20, 30, -10, -5)
        >>> max_height(target)
        45
    """
    if target.y_min <= 0 and target.y_max <= 0:
        velocity = -target.y_min - 1
    elif target.y_min >= 0 and target.y_max >= 0:
        velocity = target.y_max
    elif target.y_max >= -target.y_min:
        velocity = target.y_max
    else:
        velocity = -target.y_min - 1
    return (velocity*(velocity+1)) // 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        target = parse_input(f.readline().strip())

    print(max_height(target))