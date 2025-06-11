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

def eni(n: int, exp: int, mod: int) -> int:
    result = ""
    value = 1
    for _ in range(exp):
        value = (value * n) % mod
        result = str(value) + result
    return int(result)

def eni_tail(n: int, exp: int, mod: int, tail: int) -> int:
    return int("".join([str(pow(n, exp - i, mod)) for i in range(0, min(exp, tail))]))

def eni_sum(n: int, exp: int, mod: int) -> int:
    value = 1
    result = 0
    seen = {}
    i = 0
    with_cache = True
    while i < exp:
        value = (value * n) % mod
        result += value
        if with_cache and value in seen:
            prev_i, prev_res = seen[value]
            delta_res = result - prev_res
            delta_i = i - prev_i
            mul, remain = divmod(exp - prev_i, delta_i)
            result = mul * delta_res + (prev_res - value)
            value = next(k for k, v in seen.items() if v[0] == i - 1)
            i = exp - remain
            with_cache = False
            continue
        seen[value] = i, result
        i += 1
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [
            [int(x) for x in re.findall(r"(\d+)", row)]
            for row in file.read().strip().split("\n")
        ]
    if args.part == 1:
        print(max(sum(eni(values[i], values[i + 3], values[-1]) for i in range(3)) for values in data))
    elif args.part == 2:
        print(max(sum(eni_tail(values[i], values[i + 3], values[-1], 5) for i in range(3)) for values in data))
    else:
        print(max(sum(eni_sum(values[i], values[i + 3], values[-1]) for i in range(3)) for values in data))
    print(time() - t)
