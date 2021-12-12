import argparse
from collections import defaultdict
from collections import namedtuple
from typing import Iterable
from typing import List
from typing import Set


Position = namedtuple("Position", ['x', 'y'])


class State:
    def __init__(self, xmax, ymax):
        self.xmax = xmax
        self.ymax = ymax
        self.energy_positions = defaultdict(set)
        self.positions_energy = dict()

    def set_energy(self, position: Position, energy_level: int) -> None:
        if position in self.positions_energy:
            prev_energy = self.positions_energy[position]
            self.energy_positions[prev_energy].remove(position)
        self.energy_positions[energy_level].add(position)
        self.positions_energy[position] = energy_level
        
    def get_energy(self, position: Position) -> int:
        return self.positions_energy[position]
        
    def get_positions(self, energy_level: int) -> Set[Position]:
        return self.energy_positions[energy_level]
        
    def get_energy_levels(self) -> List[int]:
        return [k for k, v in self.energy_positions.items() if len(v) > 0]
        
    def pop_last(self, energy_level: int) -> Position:
        pos = self.energy_positions[energy_level].pop()
        del self.positions_energy[pos]
        return pos
        
    def __iter__(self):
        # copy to allow writes during iteration
        p_e = dict(self.positions_energy)   
        for position, energy in p_e.items():
            yield position, energy
            
    def step(self) -> int:
        """Returns the # of flashes after stepping state."""
        for position, energy_level in self:
            self.set_energy(position, energy_level + 1)
        
        flashed = set()
        while len(self.get_positions(energy_level=10)) > 0:
            flash = self.pop_last(energy_level=10)
            if flash in flashed:
                self.set_energy(flash, 10)
                continue
            self.set_energy(flash, 0)
            flashed.add(flash)
            for neighbour in neighbours(flash, self.xmax, self.ymax):
                if neighbour in flashed:
                    continue
                self.set_energy(neighbour, min(10, self.get_energy(neighbour) + 1))
        return len(flashed)
        
    def __repr__(self) -> str:
        r = []
        for y in range(self.ymax):
            for x in range(self.xmax):
                r.append(str(self.get_energy(Position(x, y))))
            r.append('\n')
        return ''.join(r)


def parse_input(data: List[str]) -> State:
    r"""Returns the State parsed from data."""
    state = State(xmax=len(data), ymax=len(data[0].strip()))
    for y, line in enumerate(data):
        for x, c in enumerate(line.strip()):
            state.set_energy(Position(x, y), int(c))
    return state
    

def neighbours(position: Position, xmax: int, ymax: int) -> Iterable[Position]:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = position.x + dx, position.y + dy
            if nx >= xmax or nx < 0 or ny >= ymax or ny < 0:
                continue
            yield Position(nx, ny)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        state = parse_input(f.readlines())

    total_flashes = 0
    sync_step = 0
    step = 0
    while sync_step == 0 or step < 100:
        total_flashes += state.step()
        step += 1
        if step == 100:
            print(total_flashes)
        if len(state.get_energy_levels()) == 1:
            sync_step = step

    print(sync_step) 