import argparse

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

DIR = ((0, 1), (0, -1), (1, 0), (-1, 0))

def parse_input(lines: list[str]) -> tuple[int]:
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            data[(r, c)] = int(val)
            max_c = c
        max_r = r
    return max_r, max_c

def chain_reaction(start: set[int]) -> set:
    ignited = start
    fired = set()
    while ignited:
        new_ignited = set()
        for barrel in ignited:
            if barrel in fired:
                continue
            fired.add(barrel)
            r, c = barrel
            for dr, dc in DIR:
                next_barrel = r + dr, c + dc
                if next_barrel not in destroyed and next_barrel in data and data[next_barrel] <= data[barrel]:
                    new_ignited.add(next_barrel)
        ignited = new_ignited
    return fired

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    destroyed = set()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        max_r, max_c = parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        print(len(chain_reaction({(0, 0)})))
    elif args.part == 2:
        print(len(chain_reaction({(0, 0), (max_r, max_c)})))
    else:
        for _ in range(3):
            max_destroyed = set()
            for barrel in data.keys():
                d = chain_reaction({barrel})
                if len(d) > len(max_destroyed):
                    max_destroyed = d
            destroyed |= max_destroyed
        print(len(destroyed))
    print(time() - t)
