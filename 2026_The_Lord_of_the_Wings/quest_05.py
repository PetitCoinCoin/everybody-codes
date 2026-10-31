from pathlib import Path
from time import time

from utils.parsers import parse_args, parse_grid_of_int

NEIGHBORS = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))
TREE_NEIGHBORS = (
    (0, 1),
    (0, 2),
    (0, -1),
    (0, -2),
    (1, 0),
    (2, 0),
    (-1, 0),
    (-2, 0),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
)


def propagate_land(start: tuple[int]) -> None:
    global land

    added = {start}
    land.add(start)
    while len(added):
        new_added = set()
        while added:
            cell = added.pop()
            for candidate in candidates(cell, land, data):
                if is_valid_land_candidate(candidate):
                    new_added.add(candidate)
        land |= new_added
        added = new_added


def propagate_sand() -> None:
    global sand, land

    added = set()
    for cell in land:
        if len(candidates(cell, land, data, border_included=True)) >= 1:
            added.add(cell)
            sand.add(cell)
    land -= added

    while len(added):
        new_added = set()
        while added:
            cell = added.pop()
            for candidate in candidates(cell, sand, land):
                if is_valid_sand_candidate(candidate):
                    new_added.add(candidate)
        sand |= new_added
        land -= new_added
        added = new_added


def propagate_trees() -> None:
    global sand, land, trees

    added = set()
    for cell in land:
        if is_valid_tree_candidate(cell):
            added.add(cell)
            trees.add(cell)
    land -= added

    cpt = 0
    while cpt < 2:
        cpt += 1
        new_added = set()
        for cell in land:
            r, c = cell
            tree_neighbors = [(r + dr, c + dc) for dr, dc in NEIGHBORS if (r + dr, c + dc) in trees]
            sand_neighbors = [(r + dr, c + dc) for dr, dc in NEIGHBORS if (r + dr, c + dc) in sand]
            if len(tree_neighbors) >= 4 and len(sand_neighbors) == 0:
                new_added.add(cell)
        trees |= new_added
        land -= new_added


def candidates(cell: tuple[int], field: set, whole: dict | set, *, border_included: bool = False) -> list:
    r, c = cell
    return [
        (r + dr, c + dc)
        for dr, dc in NEIGHBORS
        if (r + dr, c + dc) not in field and (border_included or (r + dr, c + dc) in whole)
    ]


def is_valid_land_candidate(cell: tuple[int]) -> bool:
    r, c = cell
    return (
        len([(r + dr, c + dc) for dr, dc in NEIGHBORS if (r + dr, c + dc) in land or data.get((r + dr, c + dc), 0)])
        >= 5
    )


def is_valid_sand_candidate(cell: tuple[int]) -> bool:
    r, c = cell
    return len([(r + dr, c + dc) for dr, dc in NEIGHBORS if (r + dr, c + dc) in sand]) >= 5


def is_valid_tree_candidate(cell: tuple[int]) -> bool:
    r, c = cell
    return all([(r + dr, c + dc) in land for dr, dc in TREE_NEIGHBORS])


if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    land = set()
    sand = set()
    trees = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data, max_r, max_c = parse_grid_of_int(file.read().strip().split("\n"))

    propagate_land((max_r // 2, max_c // 2))
    if args.part == 1:
        print(len(land))
    else:
        propagate_sand()
        if args.part == 2:
            print(len(sand))
        else:
            propagate_trees()
            print(len(trees))
    print(time() - t)
