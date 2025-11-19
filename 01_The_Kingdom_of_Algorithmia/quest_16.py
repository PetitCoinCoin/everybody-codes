import argparse

import math
from functools import cache
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

def get_coins(faces: str) -> int:
    symbols = {}
    for char in faces:
        symbols[char] = symbols.get(char, 0) + 1
    return sum(max(val - 2, 0) for val in symbols.values())

def part_2() -> int:
    base_loop = math.lcm(*[len(data[c]) for c in steps.keys()])
    loops, rest = divmod(202420242024, base_loop)
    total = 0
    i = 1
    while i <= base_loop + rest:
        result = ""
        for c in range(len(steps)):
            result += data[c + 1][(i * steps[c + 1]) % len(data[c + 1])]
        coins = get_coins(result)
        total += coins
        if i == base_loop:
            total *= loops
        i += 1
    return total

@cache
def part_3(state: tuple, right_pull: int, func: callable) -> int:
    new_state = tuple([(state[c] + steps[c + 1]) % len(data[c + 1]) for c in range(len(steps))])
    prev_new_state = tuple([(state[c] + steps[c + 1] - 1) % len(data[c + 1]) for c in range(len(steps))])
    next_new_state = tuple([(state[c] + steps[c + 1] + 1) % len(data[c + 1]) for c in range(len(steps))])
    coins = get_coins("".join(data[c + 1][new_state[c]] for c in range(len(steps))))
    prev_coins = get_coins("".join(data[c + 1][prev_new_state[c]] for c in range(len(steps))))
    next_coins = get_coins("".join(data[c + 1][next_new_state[c]] for c in range(len(steps))))
    if right_pull - 1:
        coins += part_3(new_state, right_pull - 1, func)
        prev_coins += part_3(prev_new_state, right_pull - 1, func)
        next_coins += part_3(next_new_state, right_pull - 1, func)
    return func(coins, prev_coins, next_coins)


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    steps = {}
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if not i:
                for j, val in enumerate(line.strip().split(",")):
                    steps[j + 1] = int(val)
                    data[j + 1] = []
            else:
                for j in range(len(steps)):
                    cat = line[4 * j: 4 * j + 3]
                    if cat.replace(" ", ""):
                        if args.part > 1:
                            data[j + 1].append(cat[0] + cat[-1])
    if args.part == 1:
        result = []
        for c in range(len(steps)):
            col = c + 1
            result.append(data[col][(100 * steps[col]) % len(data[col])])
        print(" ".join(result))
    elif args.part == 2:
        print(part_2())
    else:
        print(part_3((0,0,0,0,0), 256, max), part_3((0,0,0,0,0), 256, min))
    print(time() - t)
