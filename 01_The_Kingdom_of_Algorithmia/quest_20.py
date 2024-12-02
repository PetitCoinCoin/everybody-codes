import argparse

from heapq import heappop, heappush
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

FLOW_MAP = {
    ".": -1,
    "-": -2,
    "+": 1,
    "S": 0,
    "A": -1,
    "B": -1,
    "C": -1,
}

def parse_input(grid: dict, raw: str, r:int) -> None:
    for c, char in enumerate(raw):
        grid[(r, c)] = char

def next_positions(step: tuple, previous_step: tuple, *, is_part_three: bool = False) -> list:
    positions = []
    r, c = step
    d = ((0, 1), (0, -1), (1, 0)) if is_part_three else ((0, 1), (0, -1), (1, 0), (-1, 0))
    for delta in d:
        dr, dc = delta
        if is_part_three:
            if (r + dr, c + dc) == previous_step or width <= c + dc < 0:
                pass
            else:
                positions.append((r + dr, c + dc))
        else:
            if (r + dr, c + dc) == previous_step or data.get((r + dr, c + dc), "#") == "#":
                continue
            positions.append((r + dr, c + dc))
    return positions

def glide(iteration: int) -> int:
    queue = set([(1000, start, start)])
    it = 0
    while queue:
        if it == iteration:
            return max(state[0] for state in queue)
        new_queue = set()
        for alt, position, prev_position in queue:
            new_queue.update((alt + FLOW_MAP[data[pos]], pos, position) for pos in next_positions(position, prev_position))
        queue = new_queue
        it += 1

def glide_check_point() -> int:
    end_state = "SABCS"
    queue = {(start, start, "S"): 0}
    iteration = 0
    while queue:
        new_queue = {}
        for state, altitude in queue.items():
            position, prev_position, seen = state
            if seen == end_state:
                if altitude > 0:
                    return iteration
                continue
            for pos in next_positions(position, prev_position):
                char = data[pos]
                if char not in "ABCS" or end_state[:len(seen) + 1] == seen + char:
                    new_seen = seen + (char if char in "ABCS" else "")
                    alt = altitude + FLOW_MAP[char]
                    new_queue[(pos, position, new_seen)] = max(new_queue.get((pos, position, new_seen), -1000000000), alt)
        iteration += 1
        queue = new_queue

def go_south() -> int:
    altitude = 384400 - 3  # go left to be on the max warm air stream column
    pattern = 6  # going through a column decreases altitude by 6
    quot, rest = divmod(altitude, pattern)
    q, r = divmod(rest, 2)
    return quot * height + rest + (q + r) * 2

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        lines = file.read().split("\n")
        height = len(lines)
        width = len(lines[0])
        [parse_input(data, line, i) for i, line in enumerate(lines)]
    for key, val in data.items():
        if val == "S":
            start = key
            break
    if args.part == 1:
        print(glide(100))
    elif args.part == 2:
        print(glide_check_point())
    else:
        print(go_south())
    print(time() - t)
