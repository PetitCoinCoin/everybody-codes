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

def get_beetles(brightness: int, stamps: list, *, is_part_three: bool = False) -> int:
    dp = {0: 0}
    if is_part_three:
        delta = 52 if brightness % 2 else 51
        brightness = brightness // 2
    else:
        delta = 1
    for b in range(1, brightness + delta):
        dp[b] = min([dp[b - s] for s in stamps if b >= s]) + 1
    if is_part_three:
        eps = 0
        if delta == 52:
            eps = 1
            delta = 51
        return min([
            dp[brightness - d] + dp[brightness + d + eps]
            for d in range(delta)
            if 2 * d + eps <= 100
        ])
    return dp[brightness]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [int(x.strip()) for x in file.readlines()]
    if args.part == 1:
        stamps = [1, 3, 5, 10]
    elif args.part == 2:
        stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]
    else:
        stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]
    print(sum([get_beetles(b, stamps, is_part_three=args.part == 3) for b in data]))
    print(time() - t)
