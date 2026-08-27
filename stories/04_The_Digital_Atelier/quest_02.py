import math
import random
import re

from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_input(raw: list[str]) -> tuple:
    pattern = r"=\[(-?\d+),(-?\d+)]"
    start_match = re.findall(pattern, raw[0])
    a_match = re.findall(pattern, raw[1])
    b_match = re.findall(pattern, raw[2])
    c_match = re.findall(pattern, raw[3])
    return (
        tuple([int(x) for x in start_match[0]]),
        tuple([int(x) for x in a_match[0]]),
        tuple([int(x) for x in b_match[0]]),
        tuple([int(x) for x in c_match[0]]),
        raw[-1].split("=")[-1],
    )


def illuminate() -> set:
    illuminated = {start}
    x, y = start
    for move in moves:
        match move:
            case "A":
                beacon = a
            case "B":
                beacon = b
            case "C":
                beacon = c
            case _:
                raise KeyError
        x += (beacon[0] - x) / 2
        y += (beacon[1] - y) / 2
        illuminated.add((math.floor(x), math.floor(y)))
    return illuminated


def illuminate_randomly() -> set:
    illuminated = set()
    new_illuminated = {start}
    old_length = -1
    while len(illuminated) != old_length:
        old_length = len(illuminated)
        illuminated |= new_illuminated
        to_add = set()
        while new_illuminated:
            x, y = new_illuminated.pop()
            for beacon in (a, b, c):
                nx = x + (beacon[0] - x) / 2
                ny = y + (beacon[1] - y) / 2
                to_add.add((math.floor(nx), math.floor(ny)))
        new_illuminated = to_add
    return illuminated


def count_fireflies(beacons: set[tuple], with_print: bool) -> int:
    fireflies = {
        firefly
        for beacon in beacons
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if (firefly := (beacon[0] + dx, beacon[1] + dy)) not in beacons
    }
    if with_print:
        pprint(beacons | fireflies)
    return len(fireflies)


def pprint(data: set) -> None:
    min_x = min(d[0] for d in data)
    max_x = max(d[0] for d in data)
    min_y = min(d[1] for d in data)
    max_y = max(d[1] for d in data)
    print(min_x, max_x, min_y, max_y)
    for y in range(max_y + 1, min_y - 2, -1):
        print(
            "".join("#" if (x, y) in data else "." for x in range(min_x - 1, max_x + 2))
        )
    print()


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(
        f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt"
    ).open("r") as file:
        start, a, b, c, moves = parse_input(file.read().strip().split("\n"))

    beacons = illuminate() if args.part != 3 else illuminate_randomly()
    if args.part == 1:
        print(len(beacons))
    else:
        print(count_fireflies(beacons, False))
    print(time() - t)
