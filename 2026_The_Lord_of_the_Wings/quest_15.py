from collections import Counter
from heapq import heappush, heappop
from pathlib import Path
from time import time

from utils.parsers import parse_args

DELTA = (1, 1j, -1j)


def parse_input(lines: list[str]) -> tuple:
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != "#":
                grid[(r, c)] = char
            if char == "S":
                start = (r, c)
            elif char == "E":
                end = (r, c)
            elif char == "@":
                deposits.add((r, c))
    return start, end


def collect_shortest(start: tuple, end: tuple) -> int:
    queue = []
    heappush(queue, (0, start, (0, 1), set()))
    seen = set()
    while queue:
        dist, position, direction, dep = heappop(queue)
        if len(dep) == len(deposits) and position == end:
            return dist
        if (position, direction, str(dep)) in seen:
            continue
        seen.add((position, direction, str(dep)))
        direction = complex(*direction)
        for d in DELTA:
            complex_pos = complex(*position) + d * direction
            next_pos = (int(complex_pos.real), int(complex_pos.imag))
            if next_pos in grid:
                new_dir = d * direction
                if next_pos in deposits:
                    heappush(queue, (dist + 1, next_pos, (new_dir.real, new_dir.imag), dep | {next_pos}))
                else:
                    heappush(queue, (dist + 1, next_pos, (new_dir.real, new_dir.imag), dep))
    return 0


def collect_at_least(start: tuple, end: tuple, quantity: int) -> int:
    """I should compact the grid to be faster. Tried this, didn't work, gave up."""
    queue = []
    heappush(queue, (0, start, (0, 1), 0, str(start)))
    seen = set()
    while queue:
        dist, position, direction, dep, str_pos = heappop(queue)
        if dep >= quantity and position == end:
            return dist
        if (position, direction, dep) in seen:
            continue
        seen.add((position, direction, dep))
        direction = complex(*direction)
        for d in DELTA:
            complex_pos = complex(*position) + d * direction
            next_pos = (int(complex_pos.real), int(complex_pos.imag))
            if next_pos in grid:
                new_dir = d * direction
                heappush(
                    queue,
                    (
                        dist + 1,
                        next_pos,
                        (new_dir.real, new_dir.imag),
                        dep + int(next_pos in deposits),
                        str_pos + "-" + str(next_pos),
                    ),
                )
    return 0


if __name__ == "__main__":
    args = parse_args()
    t = time()
    grid = {}
    deposits = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        start, end = parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        print(collect_shortest(start, end))
    elif args.part == 2:
        print(collect_at_least(start, end, quantity=2026))
    else:
        # From observation, I have a main loop to collect 2 * 29 items, and one adds 76 distance
        main_loop = ((202620262026 // 29) - 2) // 2
        quantity = 202620262026 - (main_loop * 29 * 2)
        print(main_loop * 76 + collect_at_least(start, end, quantity=quantity))
    print(time() - t)
