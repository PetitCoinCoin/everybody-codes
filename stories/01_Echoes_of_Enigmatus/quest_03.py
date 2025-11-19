import argparse
import re

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

def get_clock(snail: tuple) -> int:
    x, y = snail
    return x + y - 1

def pass_time(snail: tuple, days: int) -> tuple:
    clock = get_clock(snail)
    x, _ = snail
    future_x = (((x - 1) + days ) % clock) + 1
    return (future_x, clock + 1 - future_x)

def position(snail: tuple) -> int:
    x, y = snail
    return x + 100 * y

def chinese_remainder_theorem() -> int:
    n = 1
    for snail in data:
        n *= get_clock(snail)
    result = 0
    for snail in data:
        _, y = snail
        clock = get_clock(snail)
        n_except = int(n / clock)
        mul = 1
        while (mul * n_except) % clock != 1:
            mul += 1
        result += (y - 1) * mul * n_except
    return result % n

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [
            tuple(int(x) for x in re.findall(r"(\d+)", raw))
            for raw in file.read().strip().split("\n")
        ]
    if args.part == 1:
        print(sum(position(pass_time(snail, 100)) for snail in data))
    else:
        print(chinese_remainder_theorem())
    print(time() - t)
