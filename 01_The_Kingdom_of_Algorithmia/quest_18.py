import argparse

from heapq import heappop, heappush
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

def parse_input(area: dict, raw: str, i: int) -> int:
    p = 0
    for c, char in enumerate(raw):
        if char != "#":
            area[(c, i)] = char
            if char == "P":
                p += 1
    return p

def get_start(area: dict, col: int, row: int) -> set:
    starts = set()
    for c in range(col):
        if (c, 0) in area:
            starts.add((c, 0))
        if (c, row - 1) in area:
            starts.add((c, row - 1))
    for r in range(row):
        if (0, r) in area:
            starts.add((0, r))
        if (col - 1, r) in area:
            starts.add((col - 1, r))
    return starts

def next_steps(area: dict, step: tuple) -> list:
    steps = []
    x, y = step
    for delta in (1, -1):
        if area.get((x + delta, y)):
            steps.append((x + delta, y))
        if area.get((x, y + delta)):
            steps.append((x, y + delta))
    return steps

def irrigate(area: dict, start: set, nb_palms: int, *, is_part_three: bool = False) -> int:
    queue = []
    for st in start:
        heappush(queue, (0, st))
    seen = {}
    palms = 0
    total_minutes = 0
    while queue:
        minutes, step = heappop(queue)
        seen[step] = True
        if area[step] == "P":
            palms += 1
            total_minutes += minutes
        if palms == nb_palms:
            return total_minutes if is_part_three else minutes
        for candidate in next_steps(area, step):
            if not candidate in seen:
                heappush(queue, (minutes + 1, candidate))
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    trees = 0
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        row = 0
        while line := file.readline():
            trees += parse_input(data, line.strip(), row)
            row += 1
            col = len(line.strip())
    if args.part in (1, 2):
        start = get_start(data, col, row)
        print(irrigate(data, start, trees))
    else:
        min_minutes = 10000000000000000
        for start_candidate, val in data.items():
            if val == "P":
                continue
            min_minutes = min(irrigate(data, {start_candidate}, trees, is_part_three=True), min_minutes)
        print(min_minutes)
    print(time() - t)
