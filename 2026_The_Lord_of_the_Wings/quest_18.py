import re
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from time import time

from utils.parsers import parse_args


@dataclass
class Stack:
    x: int
    y: int
    w: int = 1


def parse_input(raw: str) -> tuple[int]:
    matches = re.findall(r"(\d+)", raw)
    return Stack(*map(int, matches))


def is_useful(idx: int, stack: Stack) -> bool:
    if idx == 0 or idx == len(data) - 1:
        return True
    return stack.y >= max(data[:idx], key=lambda s: s.y).y or stack.y >= max(data[idx + 1 :], key=lambda s: s.y).y


def count_material() -> int:
    """Hopefully, data is already sorted by x"""
    material = 0
    for stack1, stack2 in pairwise(data):
        material += stack1.y * stack1.w
        material += (stack2.x - stack1.x - stack1.w) * min(stack1.y, stack2.y)
    material += data[-1].y * data[-1].w
    return material


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    data = [stack for i, stack in enumerate(data) if is_useful(i, stack)]
    print(count_material())
    print(time() - t)
