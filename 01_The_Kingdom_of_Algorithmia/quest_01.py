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

POTION_MAP = {
    "A": 0,
    "B": 1,
    "C": 3,
    "D": 5,
    "x": 0,
}

def group_cost(group: str) -> int:
    base = sum(POTION_MAP[creature] for creature in group)
    creatures = [char for char in group if char != "x"]
    if len(creatures) == 3:
        return base + 6
    if len(creatures) == 2:
        return base + 2
    return base

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read()
    print(sum(group_cost(data[i:i + args.part]) for i in range(0, len(data), args.part)))
    print(time() - t)
