import argparse

from copy import deepcopy
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

NEXT_D = (
    (1, 2), (1, -2), (2, 1), (2, -1),
    (-1, 2), (-1, -2), (-2, 1), (-2, -1)
)

def parse_input(lines: str) -> tuple:
    for r, line in enumerate(lines.split("\n")):
        for c, char in enumerate(line):
            if char == "S":
                data[(r, c)] = "S"
                init_sheeps.add((r, c))  # part 3
            elif char == "D":
                dragon = (r, c)
            elif char == "#":  # part 2
                hides.add((r, c))
            max_c = c
        max_r = r
    return dragon, max_r, max_c

def eat_sheeps(start: tuple, moves: int) -> set:
    r, c = start
    if moves == 1:
        return {
            (r + dr, c + dc)
            for (dr, dc) in NEXT_D
            if (r + dr, c + dc) in data
        }
    sheeps = set()
    for (dr, dc) in NEXT_D:
        if (r + dr, c + dc) in data:
            sheeps.add((r + dr, c + dc))
        sheeps |= eat_sheeps((r + dr, c + dc), moves - 1)
    return sheeps

def can_be_eaten(sheep: tuple, rounds: int) -> bool:
    r, c = sheep
    for i in range(rounds):
        if (r + i, c) not in hides and ((r + i, c) in dragons[i] or (r + i, c) in dragons[i + 1]):
            return True
        if (r + i + 1, c) in dragons[i + 1] and (r + i + 1, c) not in hides:
            return True
    return False

def tournament(position: tuple, sheeps: set, is_sheep_turn: bool = True) -> int:
    if not sheeps:
        return 1  # There is only one way to eat no sheep

    key = (position, tuple(sheeps), is_sheep_turn)
    if key in seen:
        return seen[key]

    res = 0
    if is_sheep_turn:
        sheep_moved = False
        for sheep in sheeps:
            sr, sc = sheep
            if sr == max_r:  # sheep escapes
                sheep_moved = True
                continue
            if (sr + 1, sc) != position or (sr + 1, sc) in hides:
                new_sheeps = deepcopy(sheeps)
                new_sheeps.remove(sheep)
                new_sheeps.add((sr + 1, sc))
                sheep_moved = True
                res += tournament(position, new_sheeps, False)
        if not sheep_moved:
            res += tournament(position, sheeps, False)
    else:
        pr, pc = position
        for dr, dc in NEXT_D:
            new_position = (pr + dr, pc + dc)
            if 0 <= pr + dr <= max_r and 0 <= pc + dc <= max_c:
                if new_position not in hides:
                    new_sheeps = sheeps - {new_position}
                    res += tournament(new_position, new_sheeps, True)
                else:
                    res += tournament(new_position, sheeps, True)
    seen[key] = res
    return res


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    init_sheeps = set()
    hides = set()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        dragon, max_r, max_c = parse_input(file.read().strip())
    if args.part == 1:
        print(len(eat_sheeps(dragon, 4)))
    elif args.part == 2:
        moves = 20
        dragons = {0 : {dragon}}
        for i in range(moves):
            dragons[i + 1] = {
                (d[0] + dr, d[1] + dc)
                for d in dragons[i]
                for dr, dc in NEXT_D
                if i <= d[0] + dr <= max_r or 0 <= d[1] + dc <= max_c
            }
        print(sum(
            can_be_eaten(sheep, moves)
            for sheep in data
        ))
    else:
        seen = {}
        print(tournament(dragon, init_sheeps))
    print(time() - t)
