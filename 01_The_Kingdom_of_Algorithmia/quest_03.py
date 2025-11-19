import argparse

from collections import deque
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

def remove_blocks(area: dict, *, is_last_part: bool = False) -> int:
    delta_next = (1, -1, 1j, -1j)
    if is_last_part:
        delta_next += (1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)
    candidates = deque()
    for key, value in area.items():
        if value:
            candidates.append(key)
    i = 0
    while candidates:
        block = candidates.popleft()
        for delta in delta_next:
            if area.get(block + delta, 0) < area[block]:
                break
        else:
            area[block] += 1
            candidates.append(block)
        i+=1
    return sum(area.values())

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().split("\n")
    grid = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            grid[complex(j, -i)] = 1 if data[i][j] == "#" else 0
    print(remove_blocks(grid, is_last_part=args.part == 3))
    print(time() - t)
