import argparse

from itertools import combinations, pairwise
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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split(",")]
    if args.part == 1:
        nails = 32
        print(sum(
            abs(i - j) == nails // 2
            for i, j in pairwise(data)
        ))
    elif args.part == 2:
        segments = sorted([
            (min(i, j), max(i, j))
            for i, j in pairwise(data)
        ])
        print(sum(
            seg2[0] < seg1[0] < seg2[1] and seg1[1] > seg2[1]
            for i, seg1 in enumerate(segments, 1)
            for seg2 in segments[:i]
        ))

    else:
        nails = 256
        segments = [
            (min(i, j), max(i, j))
            for i, j in pairwise(data)
        ]
        print(max(
            sum(
                (seg[0] < combi[0] < seg[1] and seg[1] < combi[1]) or (combi[0] < seg[0] < combi[1] and seg[1] > combi[1]) or (combi == seg)
                for seg in segments
            )
            for combi in combinations(range(1, nails + 1), 2)
        ))
    print(time() - t)
