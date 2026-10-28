from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_input(raw: str, max_value: int) -> dict:
    group = {str(k): set() for k in range(1, max_value + 1)}
    for item in raw.split(" "):
        if "<" in item:
            nb = item.split("<")
        else:
            nb = list(reversed(item.split(">")))
        group[nb[0]].add(nb[1])
    return group


def identify_order(group: dict, max_value: int) -> int:
    ordered = ""
    while len(ordered) < max_value:
        start = next(k for k, v in group.items() if not len(v))
        for value in group.values():
            if start in value:
                value.remove(start)
        ordered += start
        del group[start]
    return int(ordered)


if __name__ == "__main__":
    args = parse_args()
    t = time()
    max_value = 5 if args.part == 1 else 9
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(line, max_value) for line in file.read().strip().split("\n")]
    print(sum(identify_order(alloys, max_value) for alloys in data))
    print(time() - t)
