from collections import deque
from itertools import batched
from pathlib import Path
from time import time

from utils.parsers import parse_args

def parse_input(lines: list[str]) -> list:
    return [
        range(int(line.split("-")[0]), int(line.split("-")[-1]) + 1)
        for line in lines
    ]

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n"))
    wheel = deque([1])
    turns = int("2025" * args.part)
    neg = 0
    for right, left in batched(data, 2):  # No need to handle shorter last batch, len(data) is even
        wheel.extendleft(left)
        neg += len(left)
        wheel.extend(right)
    print(wheel[(neg + turns) % len(wheel)])
    print(time() - t)
