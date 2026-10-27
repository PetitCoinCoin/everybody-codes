import math
from pathlib import Path
from time import time

from utils.parsers import parse_args


def get_missing_pines_cones(x: int, *, with_one_empty: bool) -> int:
    d = 1 if with_one_empty else 0
    sqrt = math.sqrt(x + d)

    if sqrt == int(sqrt) and (not with_one_empty or (x + 1) % 2):
        return 0

    offset = 1 if with_one_empty and int(sqrt) % 2 else 0
    return (int(sqrt) + 1 + offset) ** 2 - d - x


def get_missing_pines_cones_empty_center(x: int) -> int:
    """
    If no pine is missing, we have x = base² - (base - 2)²
    Which leads to x = 4(base - 1)
    """
    base = max(3, math.ceil(1 + x / 4))
    return base**2 - (base - 2) ** 2 - x


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(
        f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt"
    ).open("r") as file:
        data = [int(x) for x in file.read().strip().split(",")]
    if args.part == 1:
        print(sum(get_missing_pines_cones(x, with_one_empty=False) for x in data))
    elif args.part == 2:
        print(sum(get_missing_pines_cones_empty_center(x) for x in data))
    else:
        print(sum(get_missing_pines_cones(x, with_one_empty=True) for x in data))
    print(time() - t)
