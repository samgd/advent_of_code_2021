import argparse
from typing import Iterable
from typing import List
from typing import Tuple


TEST_REPORT = [
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 1, 1, 0],
    [1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0]
]


def parse_report(report: Iterable[str]) -> Iterable[List[int]]:
    """
    Example:

        >>> report = ["00100", "11110", "10110"]
        >>> list(parse_report(report))
        [[0, 0, 1, 0, 0], [1, 1, 1, 1, 0], [1, 0, 1, 1, 0]]
    """
    for line in report:
        yield [int(b) for b in line.rstrip()]


def to_int(binary: List[int]) -> int:
    """Returns integer represented by list of binary digits.

    Example:
        >>> to_int([1, 0, 1])
        5
        >>> to_int([0, 0, 1, 0, 1])
        5
    """
    n = 0
    for b in binary:
        n = (n * 2) + b
    return n


def bit_cnt(report: Iterable[List[int]], pos: int = None) -> Tuple[int, List[int]]:
    """Returns # report entries and # of bits set to 1 in each position.

    Example:

        >>> bit_cnt(TEST_REPORT)
        (12, [7, 5, 8, 7, 5])
        >>> bit_cnt(TEST_REPORT, 1)
        (12, 5)
        >>> [bit_cnt(TEST_REPORT, i)[1] for i in range(5)]
        [7, 5, 8, 7, 5]
    """
    counts = None
    n = 0
    for parameter in report:
        n += 1
        if counts is None:
            counts = parameter if pos is None else parameter[pos]
        else:
            if pos is None:
                counts = [c + p for c, p in zip(counts, parameter)]
            else:
                counts += parameter[pos]
    return n, counts


def power_consumption(report: Iterable[List[int]]) -> int:
    """Returns the power consumption given the report.

    Example:

        >>> power_consumption(TEST_REPORT)
        198
    """
    n, counts = bit_cnt(report)
    gamma_rate = to_int([c >= n // 2 for c in counts])
    epsilon_rate = to_int([c <= n // 2 for c in counts])
    return gamma_rate * epsilon_rate


def rating(report: List[List[int]], mcv: bool = True) -> int:
    """Returns the rating using Part 2 rules.

    Example:

        >>> rating(TEST_REPORT, mcv=True)
        23
        >>> rating(TEST_REPORT, mcv=False)
        10
    """
    i = 0
    while len(report) > 1:
        n, cnt = bit_cnt(report, i)
        target = cnt >= (n / 2)
        target = int(target if mcv else not target)
        report = [p for p in report if p[i] == target]
        i += 1
    return to_int(report[0])


def life_support_rating(report: List[List[int]]) -> int:
    """Returns the life support rating of the submarine.

    Example:

        >>> life_support_rating(TEST_REPORT)
        230
    """
    oxygen = rating(report, mcv=True)
    co2 = rating(report, mcv=False)
    return oxygen * co2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, "r") as f:
        report = list(parse_report(f))

    pc = power_consumption(report)
    print(f"power consumption: {pc}")

    lsr = life_support_rating(report)
    print(f"life support rating: {lsr}")