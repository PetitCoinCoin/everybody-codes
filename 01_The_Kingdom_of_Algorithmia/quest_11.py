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

def grow(start: str, generation: int) -> dict:
    population = {start: 1}
    next_gen = {}
    for _ in range(generation):
        for indiv, count in population.items():
            for next_indiv in data[indiv]:
                next_gen[next_indiv] = next_gen.get(next_indiv, 0) + count
        population = next_gen
        next_gen = {}
    return population

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        while line := file.readline():
            data[line.split(":")[0]] = line.split(":")[1].strip().split(",")
    if args.part == 1:
        print(sum(grow("A", 4).values()))
    elif args.part == 2:
        print(sum(grow("Z", 10).values()))
    else:
        min_pop = 1000000000000
        max_pop = 0
        for init in data.keys():
            final_population = sum(grow(init, 20).values())
            if final_population > max_pop:
                max_pop = final_population
            if final_population < min_pop:
                min_pop = final_population
        print(max_pop - min_pop)
    print(time() - t)
