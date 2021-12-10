import argparse
from typing import List


PART1_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
PART2_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}
OPEN = set("([{<")
CLOSE = set(")]}>")
TO_CLOSE = dict(zip("([{<", ")]}>"))


class Incomplete(Exception):
    def __init__(self, to_complete: List[str]):
        self.to_complete = to_complete


class Corrupt(Exception):
    def __init__(self, wrong_close: str):
        self.wrong_close = wrong_close


def check_line(line: str) -> None:
    """Raises a Incomplete/Corrupt error if line incomplete/correct.
    
    Examples:

        >>> line = '[<>({}){}[([])<>]]'
        >>> check_line(line)

        >>> line = '([<>]'
        >>> check_line(line)
        Traceback (most recent call last):
        ...
        main.Incomplete: [')']

        >>> line = '{([(<{}[<>[]}>{[]{[(<()>'
        >>> check_line(line)
        Traceback (most recent call last):
        ...
        main.Corrupt: }
    """
    stack = []
    for c in line:
        if c in OPEN:
            stack.append(TO_CLOSE[c])
        elif c in CLOSE:
            if c == stack[-1]:
                stack.pop()
            else:
                raise Corrupt(c)
    if len(stack) > 0:
        raise Incomplete(stack[::-1])
        

def complete_score(to_complete: List[str]) -> int:
    score = 0
    for c in to_complete:
        score = score*5 + PART2_SCORES[c]    
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    part1_scores = []
    part2_scores = []
    with open(args.path, 'r') as f:
        for line in f:
            line = line.strip()
            try:
                check_line(line)
            except Corrupt as err:
                part1_scores.append(PART1_SCORES[err.wrong_close])
            except Incomplete as err:
                part2_scores.append(complete_score(err.to_complete))
                                    
    print(sum(part1_scores))
    
    print(sorted(part2_scores)[len(part2_scores) // 2])