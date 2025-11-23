import argparse

import math
from copy import deepcopy
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

def grow(steps: list, part: int) -> int | dict | tuple:
    x, y, z = 0, 0, 0
    plant = dict()
    max_height = 0
    for step in steps:
        direction = step[0]
        value = int(step[1:])
        for _ in range(value):
            match direction:
                case "U":
                    z += 1
                case "D":
                    z -= 1
                case "R":
                    x += 1
                case "L":
                    x-= 1
                case "B":
                    y += 1
                case "F":
                    y -= 1
            plant[(x, y, z)] = True
            max_height = max(max_height, z)
    if part == 1:
        return max_height
    if part == 2:
        return plant
    return plant, (x, y, z), max_height

def next_segment(plant: dict, position: tuple) -> list:
    candidates = []
    x, y, z = position
    for dx, dy, dz in (
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ):
        if plant.get((x + dx, y + dy, z + dz)):
            candidates.append((x + dx, y + dy, z + dz))
    return candidates

def search(plant: dict, leafs: dict, z: int) -> int:
    x, y = 0, 0
    queue = [(0, (x, y, z))]
    heapify(queue)
    shortest = {}
    while queue:
        distance, current = heappop(queue)
        if current in leafs:
            leafs[current] = distance
        if shortest.get(current):
            continue
        shortest[current] = distance
        for candidate in next_segment(plant, current):
            if shortest[current] + 1 < shortest.get(candidate, math.inf):
                heappush(queue, (shortest[current] + 1, candidate))
    return sum(leafs.values())

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        if args.part == 1:
            data = file.read().split(",")
        else:
            data = [row.strip().split(",") for row in file.readlines()]
    if args.part == 1:
        print(grow(data, 1))
    elif args.part == 2:
        segments = dict()
        for notes in data:
            segments = {
                **segments,
                **grow(notes, 2)
            }
        print(len(segments))
    else:
        segments = dict()
        leafs = dict()
        plant_height = 0
        for notes in data:
            seen, leaf, max_height = grow(notes, 3)
            segments = {
                **segments,
                **seen
            }
            leafs[leaf] = -1
            plant_height = max(plant_height, max_height)
        min_murkiness = math.inf
        for z in range(1, plant_height + 1):
            murkiness = search(segments, deepcopy(leafs), z) 
            if murkiness > 0:
                min_murkiness = min(min_murkiness, murkiness)
        print(min_murkiness)
    print(time() - t)
