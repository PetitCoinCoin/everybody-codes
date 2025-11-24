import operator

from itertools import accumulate
from pathlib import Path
from time import time

from utils.parsers import parse_args

def count_blocks(wall: int, pattern: list[int]) -> int:
    return sum(
        wall // value
        for value in pattern
    )

def find_pattern() -> list[int]:
    pattern = []
    for i in range(1, len(data) + 1):
        for j in range(i - 1, len(data), i):
            if not data[j]:
                break
        else:
            for j in range(i - 1, len(data), i):
                data[j] -= 1
            pattern.append(i)
    return pattern

def binary_search(min_wall: int, max_wall: int, previous_res: int, previous_wall: int) -> int:
    if max_wall - min_wall == 1:
        result = count_blocks(max_wall, spell_pattern)
        if previous_res < result <= blocks:
            return max_wall
        return previous_wall
    wall = (min_wall + max_wall) // 2
    result = count_blocks(wall, spell_pattern)
    if result == blocks:
        return wall
    if result > blocks:
        return binary_search(min_wall, wall, previous_res, previous_wall)
    if result > previous_res:
        return binary_search(wall, max_wall, result, wall)
    return binary_search(wall, max_wall, previous_res, previous_wall)

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split(",")]
    if args.part == 1:
        print(count_blocks(90, data))
    elif args.part == 2:
        spell_pattern = find_pattern()
        print(list(accumulate(spell_pattern, operator.mul))[-1])
    else:
        spell_pattern = find_pattern()
        blocks = 202520252025000
        print(binary_search(1, blocks // 2, 0, 0))
    print(time() - t)
