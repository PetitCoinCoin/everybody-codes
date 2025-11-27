import math

from pathlib import Path
from time import time

from utils.parsers import parse_args

def parse_input(lines: list[str]) -> None:
    for line in lines:
        x, y, d = tuple(int(v) for v in line.split(","))
        data[x] = data.get(x, set()) | set(range(y, y + d))

def flap():
    min_flaps = {(0, 0): 0}
    xs = 0
    rs = range(1)
    for x in data.keys():
        for y in data[x]:
            for ys in rs:
                if (xs, ys) not in min_flaps:
                    continue
                if x - xs < abs(y - ys):
                    continue
                dx = x - xs
                dy = y - ys
                flaps = (dx + dy) / 2
                if int(flaps) != flaps:
                    continue
                min_flaps[(x, y)] = min(min_flaps.get((x, y), math.inf), min_flaps[(xs, ys)] + int(flaps))
        xs = x
        rs = data[x]
    return min(
        v
        for k, v in min_flaps.items()
        if k[0] == xs
    )

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        parse_input(file.read().strip().split("\n"))
    print(flap())
    print(time() - t)
