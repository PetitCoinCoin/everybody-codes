from pathlib import Path
from time import time

from utils.grids import get_next
from utils.parsers import parse_args, parse_grid_of_int

def chain_reaction(start: set[int]) -> set:
    ignited = start
    fired = set()
    while ignited:
        new_ignited = set()
        for barrel in ignited:
            if barrel in fired:
                continue
            fired.add(barrel)
            for next_barrel in get_next(barrel):
                if next_barrel not in destroyed and next_barrel in data and data[next_barrel] <= data[barrel]:
                    new_ignited.add(next_barrel)
        ignited = new_ignited
    return fired

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    destroyed = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data, max_r, max_c = parse_grid_of_int(file.read().strip().split("\n"))
    if args.part == 1:
        print(len(chain_reaction({(0, 0)})))
    elif args.part == 2:
        print(len(chain_reaction({(0, 0), (max_r, max_c)})))
    else:
        for _ in range(3):
            max_destroyed = set()
            for barrel in data.keys():
                d = chain_reaction({barrel})
                if len(d) > len(max_destroyed):
                    max_destroyed = d
            destroyed |= max_destroyed
        print(len(destroyed))
    print(time() - t)
