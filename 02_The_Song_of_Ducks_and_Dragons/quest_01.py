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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().strip().split("\n\n")
    names = data[0].split(",")
    instructions = data[1].split(",")
    if args.part == 1:
        idx = 0
        for instruction in instructions:
            mul = 1 if instruction[0] == "R" else -1
            idx += int(instruction[1:]) * mul
            idx = min(max(0, idx), len(names) - 1)
        print(names[idx])
    elif args.part == 2:
        idx = 0
        for instruction in instructions:
            mul = 1 if instruction[0] == "R" else -1
            idx += int(instruction[1:]) * mul
        print(names[idx % len(names)])
    else:
        for instruction in instructions:
            mul = 1 if instruction[0] == "R" else -1
            idx = (int(instruction[1:]) * mul) % len(names)
            names[0], names[idx] = names[idx], names[0]
        print(names[0])
    print(time() - t)
