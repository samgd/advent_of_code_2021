import argparse
import enum
import re
from pathlib import Path
from typing import Iterable
from typing import Tuple


class CommandType(enum.Enum):
    FORWARD = enum.auto()
    DOWN = enum.auto()
    UP = enum.auto()


class Command:
    _pattern = re.compile(r"(forward|down|up) (\d+)")

    def __init__(self, direction: CommandType, distance: int):
        self.direction = direction
        self.distance = distance

    @staticmethod
    def fromstring(val: str):
        """Returns a Command parsed from val.

            Example:
                >>> Command.fromstring("forward 10")
                Command('forward', 10)
        """
        match = Command._pattern.fullmatch(val)
        if not match:
            raise ValueError(f"failed, {val}")
        return Command(
            direction=CommandType[match[1].upper()],
            distance=int(match[2])
        )

    def __repr__(self) -> str:
        return f"Command('{self.direction.name.lower()}', {self.distance})"


def navigate_part1(commands: Iterable[Command]) -> Tuple[int, int]:
    """Returns a tuple of (horizontal position, depth) based on part 1 rules.
    
    Example:
        >>> cmds = map(Command.fromstring, [
        ...     "forward 5", "down 5", "forward 8", "up 3",
        ...     "down 8", "forward 2"
        ... ])
        >>> navigate_part1(cmds)
        (15, 10)
    """
    hor_pos, depth = 0, 0
    for cmd in commands:
        if cmd.direction == CommandType.FORWARD:
            hor_pos += cmd.distance
        elif cmd.direction == CommandType.DOWN:
            depth += cmd.distance
        elif cmd.direction == CommandType.UP:
            depth -= cmd.distance
        else:
            raise ValueError(f"unknown command {cmd}")
    return hor_pos, depth


def navigate_part2(commands: Iterable[Command]) -> Tuple[int, int]:
    """Returns a tuple of (horizontal position, depth) based on part 2 rules.
    
    Example:
        >>> cmds = map(Command.fromstring, [
        ...     "forward 5", "down 5", "forward 8", "up 3",
        ...     "down 8", "forward 2"
        ... ])
        >>> navigate_part2(cmds)
        (15, 60)
    """
    hor_pos, depth, aim = 0, 0, 0
    for cmd in commands:
        if cmd.direction == CommandType.FORWARD:
            hor_pos += cmd.distance
            depth += aim * cmd.distance
        elif cmd.direction == CommandType.DOWN:
            aim += cmd.distance
        elif cmd.direction == CommandType.UP:
            aim -= cmd.distance
        else:
            raise ValueError(f"unknown command {cmd}")
    return hor_pos, depth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    commands = [
        Command.fromstring(line.strip("\n"))
        for line in open(args.path).readlines()
        if line # skip whitespace
    ]
    
    hor_pos, depth = navigate_part1(commands)
    print(f"part 1: {hor_pos * depth}")

    hor_pos, depth = navigate_part2(commands)
    print(f"part 2: {hor_pos * depth}")