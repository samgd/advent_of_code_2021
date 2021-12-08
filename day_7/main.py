"""
Part 1: The first thing that comes to mind is taking the median. If 50% of the values are lower than or equal to this, and 50% are greater than or equal to this then shifting this position one to the left or right will cause the total distance moved to be >= 0.

Part 2: The mean will take into account outliers. 
"""
import argparse
from typing import List
from typing import Tuple


import numpy as np


def parse_input(data: str) -> List[int]:
    """Returns the input parsed from data.

    Example:

        >>> data = '16,1,2,0,4,2,7,1,2,14'
        >>> parse_input(data)
        [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    """
    return [int(i) for i in data.rstrip().split(',')]


def part_1_position_fuel(positions: List[int]) -> Tuple[int, int]:
    """Returns the (aligned position, total fuel).

    Example:
        
        >>> positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        >>> part_1_position_fuel(positions)
        (2, 37)
    """
    positions = np.array(positions)
    target = round(np.median(positions))
    fuel = np.sum(np.abs(positions - target))
    return target, fuel


def part_2_position_fuel(positions: List[int]) -> Tuple[int, int]:
    """Returns the (aligned position, total fuel).

    Example:

        >>> positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        >>> part_2_position_fuel(positions)
        (5, 168)
    """
    positions = np.array(positions)
    target = np.mean(positions)
    min_dist, min_fuel = None, None
    for int_tgt in [int(np.floor(target)), int(np.ceil(target))]:
        distances = np.abs(positions - int_tgt)
        fuel = np.sum((distances * (distances + 1)) // 2)
        if min_fuel is None or fuel < min_fuel:
            min_dist = int_tgt
            min_fuel = fuel
    return min_dist, min_fuel


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        positions = parse_input(f.readline())

    target, fuel = part_1_position_fuel(positions)
    print(f"part 1, total fuel to align to position {target}: {fuel}")
   
    target, fuel = part_2_position_fuel(positions)
    print(f"part 2, total fuel to align to position {target}: {fuel}")