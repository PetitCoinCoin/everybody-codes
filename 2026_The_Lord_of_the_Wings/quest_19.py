import operator
from collections import Counter
from copy import deepcopy
from functools import reduce
from itertools import permutations, zip_longest
from pathlib import Path
from time import time

from utils.parsers import parse_args, parse_grid_of_char

MIX = {
    "CC": "C",
    "MM": "M",
    "YY": "Y",
    "KK": "K",
    "KC": "K",
    "CK": "K",
    "KM": "K",
    "MK": "K",
    "YK": "K",
    "KY": "K",
    "CM": "B",
    "MC": "B",
    "MY": "R",
    "YM": "R",
    "CY": "G",
    "YC": "G",
}


def get_whites(first_layer: dict, second_layer: dict) -> int:
    crystal = [MIX[first_layer[(r, c)] + second_layer[(r, c)]] for r in range(rows + 1) for c in range(columns + 1)]
    return reduce(operator.mul, [x[1] for x in Counter(crystal).most_common(3)])


if __name__ == "__main__":
    args = parse_args()
    t = time()
    layers = []
    rows = 0
    columns = 0
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        for grid in file.read().strip().split("\n\n"):
            grid, max_r, max_c = parse_grid_of_char(grid.split("\n"))
            layers.append(grid)
            rows = max_r
            columns = max_c
    if args.part == 1:
        print(get_whites(*layers))

    elif args.part == 2:
        max_white = 0
        for perm in permutations("CMYK", 4):
            test_layer = deepcopy(layers[1])
            for key, value in test_layer.items():
                test_layer[key] = perm[int(value) - 1]
            max_white = max(max_white, get_whites(layers[0], test_layer))
        print(max_white)
    else:
        count = Counter(layers[0].values())
        # Black is underrepresented here, so we don't care about it
        base, rest = divmod(sum(x[1] for x in count.most_common(3)), 3)
        print(reduce(operator.mul, (b + d for b, d in zip_longest([base] * 3, [1] * rest, fillvalue=0))))
    print(time() - t)
