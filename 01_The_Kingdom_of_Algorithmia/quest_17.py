import argparse

import math
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

def manhattan(a: complex, b: complex) -> int:
    return abs(a.real - b.real) + abs(a.imag - b.imag)

def constellation_size(stars: set) -> int:
    total_distance = len(stars)
    seen = set()
    seen.add(stars.pop())
    while stars:
        min_star = None
        min_dist = math.inf
        for star in seen:
            for other in stars:
                if manhattan(star, other) < min_dist:
                    min_dist = manhattan(star, other)
                    min_star = other
        if min_star:
            seen.add(min_star)
            stars.remove(min_star)
            total_distance += min_dist
    return int(total_distance)

def find_constellations(stars: set) -> dict:
    constellations = {}
    while stars:
        temp = set()
        base = stars.pop()
        temp.add(base)
        loop = True
        while loop:
            loop = False
            for star in stars:
                if star not in temp:
                    for star_in in temp:
                        if manhattan(star_in, star) < 6:
                            temp.add(star)
                            loop = True
                            break
        stars -= temp
        constellations[len(constellations)] = temp
    return constellations

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        lines = file.read().split("\n")
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == "*":
                    data.add(complex(c, -r))
    if args.part in (1, 2):
        print(constellation_size(data))
    else:
        sizes = [constellation_size(constellation) for constellation in find_constellations(data).values()]
        sizes.sort(reverse=True)
        print(sizes[0] * sizes[1] * sizes[2])
    print(time() - t)
