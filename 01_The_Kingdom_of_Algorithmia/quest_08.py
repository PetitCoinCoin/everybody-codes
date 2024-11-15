import argparse
import math

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

def with_thickness(priests: int, acolytes: int, *, is_part_three: bool = False) -> int:
    available = 202400000 if is_part_three else 20240000
    blocks = 1
    base = 1
    thickness = 1
    heights = [1]
    while blocks < available:
        thickness = (thickness * priests) % acolytes
        if is_part_three:
            thickness += acolytes
            heights = [h + thickness for h in heights]
            heights.append(thickness)
        base += 2
        blocks += thickness * base
    if is_part_three:
        heights = heights[::-1] + heights[1:]
        empty = 0
        for height in heights[1:-1]:
            empty += (priests * base * height) % acolytes
        return blocks - empty - available
    return (blocks - available) * base

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = int(file.read())
    if args.part == 1:
        # Solve x² + x/2 - data = 0: Sum of x first terms of an arithmetic serie, with common difference 2
        delta = (1/2) ** 2 + 4 * data
        n = int((-1/2 + math.sqrt(delta)) / 2)
        base_width = n * 2 + 1
        missing = ((n + 1) * (1 + base_width) / 2) - data
        print(int(base_width * missing))
    elif args.part == 2:
        print(with_thickness(data, 1111))
    else:
        print(with_thickness(data, 10, is_part_three=True))
    print(time() - t)
