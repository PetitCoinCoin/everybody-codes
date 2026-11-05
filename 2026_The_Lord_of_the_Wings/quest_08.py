from pathlib import Path
from time import time

from utils.parsers import parse_args

ROUNDS = ("TL", "TR", "R", "BR", "BL", "L")
START_DIRECTIONS = {
    "TL": ((-1, 1), (0, 2)),
    "L": ((1, -1), (1, 1)),
    "TR": ((0, 2), (1, 1)),
    "R": ((1, 1), (1, -1)),
    "BR": ((1, -1), (0, -2)),
    "BL": ((1, 1), (0, 2)),
}
SHADOW_DIRECTIONS = {
    "TL": (1, 1),
    "L": (0, 2),
    "TR": (1, -1),
    "R": (0, -2),
    "BR": (-1, -1),
    "BL": (-1, 1),
}


def parse_input(lines: list[str]):
    r_max_c = 0
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != ".":
                data[(r, c)] = int(char)
                if not c:
                    starts["TL"] = (r, c)
                    starts["BL"] = (r, c)
                    r_max_c = r
                if r == r_max_c:
                    starts["BR"] = (r, c)
                if not r and "L" not in starts:
                    starts["L"] = (r, c)
                    starts["TR"] = (r, c)
                if not r:
                    starts["R"] = (r, c)


def get_energy_from_shadow(direction: str, *, with_warriors: bool = False) -> int:
    energy = 0
    start = starts[direction]
    next_directions = START_DIRECTIONS[direction]
    while start:
        energy += energy_from_line(start, direction, with_warriors=with_warriors)
        r, c = start
        for dr, dc in next_directions:
            if (r + dr, c + dc) in data:
                start = (r + dr, c + dc)
                break
        else:
            start = None
    return energy


def energy_from_line(start: tuple[int], direction: str, *, with_warriors: bool = False) -> int:
    global warriors

    r, c = start
    energy = 1 if data[start] > 0 else 0
    shadow = data[start]
    if with_warriors and data[start] == 9:
        warriors += 1
        data[start] = -2
    else:
        data[start] += 1
    dr, dc = SHADOW_DIRECTIONS[direction]
    next_ent = (r + dr, c + dc)
    while next_ent in data:
        shadow = max(0, shadow - 1)
        if data[next_ent] > shadow:
            if data[next_ent] > 0:
                energy += 1
                shadow = data[next_ent]
            if with_warriors:
                data[next_ent] += 1
        elif data[next_ent] < 1:
            data[next_ent] += 1
        if with_warriors and data[next_ent] == 10:
            warriors += 1
            data[next_ent] = -2
        next_ent = (next_ent[0] + dr, next_ent[1] + dc)
    return energy


if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    starts = {}
    warriors = 0
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        print(get_energy_from_shadow("TL"))
    elif args.part == 2:
        print(sum(get_energy_from_shadow(direction) for direction in ROUNDS))
    else:
        energy = 0
        tours = 0
        while warriors < 100000:
            for direction in ROUNDS:
                tours += 1
                energy += get_energy_from_shadow(direction, with_warriors=True)
                if warriors >= 100000:
                    break
        print(energy)
    print(time() - t)
