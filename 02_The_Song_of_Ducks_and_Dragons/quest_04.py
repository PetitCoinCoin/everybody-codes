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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        if args.part != 3:
            data = [int(x) for x in file.read().strip().split("\n")]
        else:
            data = [
                tuple((int(x) for x in line.split("|"))) if "|" in line else (int(line), int(line))
                for line in file.read().strip().split("\n")
            ]
    if args.part == 1:
        print(2025 * data[0] // data[-1])
    elif args.part == 2:
        print(math.ceil(10000000000000 * data[-1] / data[0]))
    else:
        turns = 100
        for i in range(len(data) - 1):
            turns *= data[i][-1] / data[i + 1][0]
        print(int(turns))
    print(time() - t)
