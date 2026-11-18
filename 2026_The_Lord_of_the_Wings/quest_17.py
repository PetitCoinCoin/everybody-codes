from heapq import heappush, heappop
from pathlib import Path
from time import time

from utils.grids import get_next
from utils.parsers import parse_args, parse_grid_of_char

NEXT_DIRECTION = {
    "L": (1, 0),
    "B": (0, 1),
    "R": (-1, 0),
    "T": (0, -1),
}

NEXT_SIDE_IN = {
    "L": "B",
    "B": "R",
    "R": "T",
    "T": "L",
}

NEXT_SIDE_OUT = {
    "L": "T",
    "B": "L",
    "R": "B",
    "T": "R",
}
OTHER_SIDE = {
    "L": (0, -1),
    "B": (1, 0),
    "R": (0, 1),
    "T": (-1, 0),
}


def walk_fast(end: tuple) -> int:
    queue = []
    heappush(queue, (0, (0, 0)))
    seen = set()
    while queue:
        distance, position = heappop(queue)
        if position == end:
            return distance
        if position in seen:
            continue
        seen.add(position)
        for next_position in get_next(position):
            if next_position not in seen and next_position in data:
                heappush(queue, (distance + 1, next_position))
    return 0


def follow_the_edge(end: tuple) -> int:
    """
    Go down to start, because why not.
    Then you have to arrive at the bottom right corner from the left (following the bottom edge)
    """
    position = (0, 0)
    side = "L"
    distance = 1
    while position != end or side != "B":
        r, c = position
        dr, dc = NEXT_DIRECTION[side]
        next_position = (r + dr, c + dc)
        if next_position in data:
            position = next_position

            ndr, ndc = OTHER_SIDE[side]
            next_neighbour = r + dr + ndr, c + dc + ndc
            if next_neighbour in data:
                side = NEXT_SIDE_OUT[side]
                continue
        else:
            side = NEXT_SIDE_IN[side]
        distance += 1
    return distance


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data, max_r, max_c = parse_grid_of_char(file.read().strip().split("\n"), keep_only="#")
    if args.part == 1:
        print(walk_fast((max_r, max_c)))
    else:
        total_edges = sum(
            sum(next_position not in data for next_position in get_next(position)) for position in data.keys()
        )
        if args.part == 2:
            print(total_edges)
        else:
            one_edge = follow_the_edge((max_r, max_c))
            print(min(one_edge, total_edges - one_edge))
    print(time() - t)
