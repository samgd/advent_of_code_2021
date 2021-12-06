import argparse
from collections import defaultdict
from typing import Dict

State = Dict[int, int]


def step(state: State) -> State:
    """Returns the new State after updating all laternfish timers.

    Example:

        >>> state = {3: 2, 4: 1, 1: 1, 2: 1}
        >>> state = step(state)
        >>> state
        {2: 2, 3: 1, 0: 1, 1: 1}
        >>> step(state)
        {1: 2, 2: 1, 6: 1, 8: 1, 0: 1}
    """
    new_state = defaultdict(int)
    for days_left, cnt in state.items():
        if days_left == 0:
            new_state[6] += cnt
            new_state[8] += cnt
        else:
            new_state[days_left - 1] += cnt
    return dict(new_state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--days", type=int, default=80)
    args = parser.parse_args()

    with open(args.path, "r") as f:
        day_strs = f.readline().rstrip().split(",")
    state = defaultdict(int)
    for day in day_strs:
        state[int(day)] += 1

    for _ in range(args.days):
        state = step(state)
        
    print(sum(state.values()))