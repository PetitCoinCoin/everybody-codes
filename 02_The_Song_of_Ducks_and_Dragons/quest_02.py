import argparse
import re

from collections import namedtuple
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

Complex = namedtuple("Complex", "x y")

def c_add(a: Complex, b: Complex) -> Complex:
    return Complex(a.x + b.x, a.y + b.y)

def c_mul(a: Complex, b: Complex) -> Complex:
    return Complex(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)

def c_div(a: Complex, b: Complex) -> Complex:
    return Complex(int(a.x / b.x), int(a.y / b.y))

def cycle(count: int, divider: Complex, base: Complex) -> Complex:
    result = Complex(0, 0)
    for _ in range(count):
        result = c_mul(result, result)
        result = c_div(result, divider)
        result = c_add(result, base)
        if not can_be_engraved(result):
            return result
    return result

def can_be_engraved(a: Complex) -> bool:
    bound = 1000000
    return -bound <= a.x <= bound and -bound <= a.y <= bound

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = Complex(*tuple(int(x) for x in re.findall(r"A=\[(-?\d+),(-?\d+)\]", file.read())[0]))
    if args.part == 1:
        print(list(cycle(3, Complex(10, 10), data)))
    else:
        steps = 10 if args.part == 2 else 1
        points = [
            [
                can_be_engraved(cycle(100, Complex(100000,100000), c_add(data, Complex(c, r))))
                for c in range(0, 1001, steps)
            ]
            for r in range(0, 1001, steps)
        ]
        print("\n".join([
            "".join(["X" if point else "." for point in row])
            for row in points
        ]))
        print(sum(sum(row) for row in points))
    print(time() - t)
