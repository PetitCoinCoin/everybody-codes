import argparse

from collections import Counter
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
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = (int(x) for x in file.read().strip().split("\n")[0].split(","))
    if args.part == 1:
        print(sum(set(data)))
    elif args.part == 2:
        print(sum(sorted(set(data))[:20]))
    else:
        print(max(Counter(data).values()))
    print(time() - t)
