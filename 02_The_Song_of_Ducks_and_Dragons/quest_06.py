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
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().strip()
    if args.part == 1:
        print(sum(
            Counter(data[:idx])["A"]
            for idx in range(len(data))
            if data[idx] == "a"
        ))
    elif args.part == 2:
        print(sum(
            Counter(data[:idx])[data[idx].upper()]
            for idx in range(len(data))
            if data[idx].islower()
        ))
    else:
        distance = 1000
        repeat = 1000
        base_pairs = sum(
            Counter(data[max(idx - distance, 0):idx + distance + 1])[data[idx].upper()]
            for idx in range(len(data))
            if data[idx].islower()
        )
        additional_pairs_start = sum(
            Counter(data[-(distance - idx):])[data[idx].upper()]
            for idx in range(distance)
            if data[idx].islower()
        )
        additional_pairs_end = sum(
            Counter(data[:distance + idx + 1])[data[idx].upper()]
            for idx in range(-distance, 0)
            if data[idx].islower()
        )
        print(repeat * base_pairs + (repeat - 1) * (additional_pairs_start + additional_pairs_end))
    print(time() - t)
