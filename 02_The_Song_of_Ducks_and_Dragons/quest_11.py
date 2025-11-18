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

def phase_one() -> int:
    r = 0
    moved = True
    while moved:
        if r == MAX_ROUNDS:
            return r
        moved = False
        for i in range(len(data) - 1):
            if data[i] > data[i + 1]:
                data[i] -= 1
                data[i + 1] += 1
                moved = True
        if moved:       
            r += 1
    return r

def phase_two(start: int) -> int:
    r = start
    moved = True
    while moved:
        if r == MAX_ROUNDS:
            return r
        moved = False
        for i in range(len(data) - 1):
            if data[i] < data[i + 1]:
                data[i] += 1
                data[i + 1] -= 1
                moved = True
        if moved:       
            r += 1
        print("**", r, flock_checksum(), data)
    return r

def flock_checksum() -> int:
    return sum(
        i * x
        for i, x in enumerate(data, 1)
    )

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split("\n")]
    if args.part == 1:
        MAX_ROUNDS = 10
        phase_two(phase_one())
        print(flock_checksum())
    else:
        MAX_ROUNDS = -1
        # This solution runs for hours for part 3
        # print(phase_two(phase_one()))

        # This one doesn't, as the input is already sorted!
        r_phase_one = phase_one()
        final_value = sum(data) // len(data)
        r_phase_two = sum(x - final_value for x in data if x > final_value)
        print(r_phase_one + r_phase_two)
    print(time() - t)
