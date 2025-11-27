import re

from pathlib import Path
from time import time

from utils.parsers import parse_args

def parse_input(lines: str) -> None:
    for line in lines:
        pattern = r"Plant (\d+) with thickness (\d+):"
        for _id, thickness in (map(int, match) for match in re.findall(pattern, line)):
            data[_id] = {"thickness": thickness, "children": []}
            rev_data[_id] = {"thickness": thickness, "parents": []}
        link_pattern = r"branch to Plant (\d+) with thickness (-?\d+)"
        for other_id, other_thickness in (map(int, match) for match in re.findall(link_pattern, line)):
            data[other_id]["children"].append((_id, other_thickness))
            rev_data[_id]["parents"].append((other_id, other_thickness))

def get_energy(plant: int, test: list[int] = []) -> int:
    if not rev_data[plant]["parents"]:
        return 1 if not test else test[plant - 1]
    energy = sum(
        get_energy(p, test) * t
        for p, t in rev_data[plant]["parents"]
    )
    return energy if energy >= rev_data[plant]["thickness"] else 0

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    rev_data = {}
    test_cases = []
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        plant_input = file.read().strip().split("\n\n\n")
        parse_input(plant_input[0].split("\n\n"))
        if len(plant_input) > 1:
            test_cases = [
                [int(x) for x in line.split()]
                for line in plant_input[1].split("\n")
            ]
    for plant, values in data.items():
        if not values["children"]:
            last_plant = plant
    if args.part == 1:
        print(get_energy(last_plant))
    elif args.part == 2:
        print(sum(get_energy(last_plant, test) for test in test_cases))
    else:
        # Doesn't work for test input.
        # Otherwise, negative thickness are only present at first level, and consistent,
        # ie. a root plant always have only a negative or positive impact on all its children
        roots = len([k for k, v in rev_data.items() if not v["parents"]])
        contribution = [1] * roots
        for plant, value in data.items():
            if value["thickness"] == 1 and any(child[1] < 0 for child in value["children"]):
                contribution[plant - 1] = 0
        max_energy = get_energy(last_plant, contribution)
        print(sum(
            max_energy - energy
            for test in test_cases
            if (energy := get_energy(last_plant, test))
        ))
    print(time() - t)
