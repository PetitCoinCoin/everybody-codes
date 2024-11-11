import argparse

from pathlib import Path
from statistics import median
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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [int(x.strip()) for x in file.readlines()]
    if args.part in (1, 2):
        level = min(data)
    else:
        level = median(data)
    print(int(sum(abs(x - level) for x in data)))
    print(time() - t)
