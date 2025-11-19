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

def parse_input(line: str) -> None:
    identifier, data = line.split(":")
    swords[int(identifier)] = [int(x) for x in data.split(",")]

def get_quality(items: list) -> tuple:
    fishbone = []
    for val in items:
        for item in fishbone:
            key, left, right = tuple(item)
            if left is None and val < key:
                item[1] = val
                break
            if right is None and val > key:
                item[2] = val
                break
        else:
            fishbone.append([val, None, None])
    return int("".join(str(x[0]) for x in fishbone)), fishbone

def sort_swords(sword: tuple[int, list[int]]) -> tuple[int]:
    identifier, numbers = sword
    quality, fishbone = get_quality(numbers)
    values = [quality]
    for level in fishbone:
        value = int("".join((str(x) for x in level if x is not None)))
        values.append(value)
    values.append(identifier)
    return tuple(values)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    swords = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        for line in file.read().strip().split("\n"):
            parse_input(line)
    if args.part == 1:
        print(get_quality(list(swords.values())[0])[0])
    elif args.part == 2:
        qualities = [get_quality(sword)[0] for sword in swords.values()]
        print(max(qualities) - min(qualities))
    else:
        sorted_swords = sorted([(key, value) for key, value in swords.items()], key=sort_swords, reverse=True)
        print(sum(
            sorted_swords[i][0] * (i + 1)
            for i in range(len(sorted_swords))
        ))
    print(time() - t)
