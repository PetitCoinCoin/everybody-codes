import argparse
import math

from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from pathlib import Path
from time import time

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p",
        type=int,
        choices={1, 2, 3},
        help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args

@dataclass
class KPath:
    time: int
    position: complex

    def __gt__(self, other_path):
        return self.time > other_path.time

def parse_input(lines: list, *, is_part_three: bool = False) -> tuple:
    res = {}
    if is_part_three:
        end = []
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char in "# ":
                continue
            if char == "S":
                res[complex(c, -r)] = 0
                if is_part_three:
                    end.append(complex(c, -r))
                else:
                    start = complex(c, -r)
            elif char == "E":
                res[complex(c, -r)] = 0
                if is_part_three:
                    start = complex(c, -r)
                else:
                    end = complex(c, -r)
            else:
                res[complex(c, -r)] = int(char)
    return res, start, end

def next_candidates(area: dict, path: KPath) -> list:
    candidates = []
    for delta in (1, -1, 1j, -1j):
        if area.get(path.position + delta) is not None:
            candidates.append(path.position + delta)
    return candidates

def shortest_path(data: list, start: complex, end: complex | list) -> int:
    if isinstance(end, complex):
        end = [end]
    queue = [KPath(0, start)]
    heapify(queue)
    shortest = {}
    while queue:
        current = heappop(queue)
        if current.position in end:
            return current.time
        if shortest.get(current.position):
            continue
        shortest[current.position] = current.time
        for candidate in next_candidates(data, current):
            delta = min(abs(data[candidate] - data[current.position]), 10 - abs(data[candidate] - data[current.position]))
            if shortest[current.position] + delta + 1 < shortest.get(candidate, math.inf):
                heappush(queue, KPath(shortest[current.position] + delta + 1, candidate))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data, start, end = parse_input(file.read().split("\n"), is_part_three=args.part == 3)
    print(shortest_path(data, start, end))
    print(time() - t)
