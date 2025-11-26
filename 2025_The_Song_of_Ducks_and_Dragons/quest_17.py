import math
from heapq import heappop, heappush
from pathlib import Path
from time import time

from utils.parsers import parse_args

ALL_DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))

def parse_input(lines: list) -> tuple:
    start = None
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val == "@":
                volcano = r, c
                val = 0
            elif val == "S":
                start = r, c
                val = 0
            data[(r, c)] = int(val)
            max_c = c
        max_r = r
    return max_r + 1, max_c + 1, volcano, start

def is_in_circle(radius: int, position: tuple) -> bool:
    r, c = position
    return (rv - r) * (rv - r) + (cv - c) * (cv - c) <= radius * radius

def recurlia_loop(radius: int) -> int:
    total_cost = math.inf
    total_position = None
    heap = []
    heappush(heap, (0, start, 0, 0, 0))
    seen = {}
    while heap:
        cost, position, prev_dr, prev_dc, from_left = heappop(heap)
        r, c = position

        # Cost is too big, radius is no longer relevant
        if radius <= cost // 30 - 1:
            return 0

        # Position already seen, coming from the other side of the volcano
        if from_left and (position, -from_left) in seen:
            current_cost = cost + seen[(position, -from_left)] - data[position]
            # Cost is too big, radius is no longer relevant
            if radius <= current_cost // 30 - 1:
                continue
            # Cost is not minimal
            if current_cost > total_cost:
                continue

            if current_cost < total_cost:
                total_cost = current_cost
                total_position = position
            # We have already seen this minimal cost, so we won't find any lower cost
            if total_position == (r - prev_dr, c - prev_dc):
                return radius * total_cost
        if (position, from_left) in seen:
            continue
        seen[(position, from_left)] = cost
    
        for dr, dc in ALL_DIRS:
            # No direct go back
            if dr == -prev_dr and dc == -prev_dc:
                continue
            new_position = r + dr, c + dc
            if new_position not in data or is_in_circle(radius, new_position):
                continue
            if from_left:
                new_from_left = from_left
            else:
                if r + dr > rv:
                    new_from_left = 1 if c + dc < cv else - 1
                else:
                    new_from_left = 0
            heappush(heap, (cost + data[new_position], new_position, dr, dc, new_from_left))
    return 0

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        max_r, max_c, volcano, start = parse_input(file.read().strip().split("\n"))
    rv, cv = volcano
    if args.part == 1:
        print(sum(
            value
            for position, value in data.items()
            if is_in_circle(10, position)
        ))
    elif args.part == 2:
        result = 0
        max_destruction = 0
        cumulated = 0
        destroyed = set()
        for radius in range(1, min(max_r, max_c)):
            destruction = 0
            for position, value in data.items():
                if position in destroyed:
                    continue
                if is_in_circle(radius, position):
                    destruction += value
                    destroyed.add(position)
            if destruction > max_destruction:
                result = radius * destruction
                max_destruction = destruction
        print(result)
    else:
        rs, cs = start
        for rad in range(1, min(rv, cv)):
            result = recurlia_loop(rad)
            if result:
                print(result)
                break
    print(time() - t)
