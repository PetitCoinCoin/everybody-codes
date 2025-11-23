from pathlib import Path
from time import time

from utils.parsers import parse_args, parse_grid_of_char

class Floor:
    DIAG = ((1, 1), (-1, 1), (1, -1), (-1, -1))

    def __init__(self, pattern: dict, max_r: int, max_c: int) -> None:
        self.pattern = set(pattern.keys())
        self.r = max_r + 1
        self.c = max_c + 1
    
    def activate(self) -> None:
        new_pattern = set()
        for r in range(self.r):
            for c in range(self.c):
                if (r, c) in self.pattern:
                    if len([(dr, dc) for dr, dc in self.DIAG if (r + dr, c + dc) in self.pattern]) % 2:
                        new_pattern.add((r, c))
                else:
                    if not len([(dr, dc) for dr, dc in self.DIAG if (r + dr, c + dc) in self.pattern]) % 2:
                        new_pattern.add((r, c))
        self.pattern = new_pattern
    
    def match(self, center_pattern: set) -> bool:
        center = {
            (r - 13, c - 13)
            for r, c in self.pattern
            if 12 < r < 21 and 12 < c < 21
        }
        return center == center_pattern

    @property
    def active(self) -> int:
        return len(self.pattern)

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data, max_r, max_c = parse_grid_of_char(file.read().strip().split("\n"), "#")
    if args.part != 3:
        floor = Floor(data, max_r, max_c)
        active_tiles = 0
        rounds = 10 if args.part == 1 else 2025
        for _ in range(rounds):
            floor.activate()
            active_tiles += floor.active
        print(active_tiles)
    else:
        # The trick is to see that there is a loop
        floor = Floor({}, 33, 33)
        pattern = set(data.keys())
        matched_rounds = []
        active_tiles = []
        rounds = 1000000000
        for r in range(rounds):
            floor.activate()
            if floor.match(pattern):
                if active_tiles and floor.active == active_tiles[0]:
                    end = r + 1
                    break
                matched_rounds.append(r + 1)
                active_tiles.append(floor.active)
        start = matched_rounds[0]
        rounds -= start
        loops, remaining = divmod(rounds, end - start)
        result = active_tiles[0]
        result += loops * sum(active_tiles)
        i = 1
        while remaining >= matched_rounds[i] - matched_rounds[i - 1]:
            result += active_tiles[i]
            remaining -= matched_rounds[i] - matched_rounds[i - 1]
            i += 1
        print(result)
    print(time() - t)
