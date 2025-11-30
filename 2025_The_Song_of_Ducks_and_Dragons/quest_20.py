from heapq import heappop, heappush
from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_grid_of_char(lines: list[str]) -> tuple:
    global start, end

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char in "#TSE":
                data[(r, c)] = char if char == "#" else "T"
                if char == "S":
                    start = (r, c)
                elif char == "E":
                    end = (r, c)
            max_c = c
        max_r = r
    return max_r, max_c

def get_neighbours(triangle: tuple) -> list:
    r, c = triangle
    result = [(r, c - 1), (r, c + 1)]
    if (not r % 2 and c % 2) or (r % 2 and not c % 2):
        result.append((r + 1, c))
    if (r % 2 and c % 2) or (not r % 2 and not c % 2):
        result.append((r - 1, c))
    return result

def rotate_once(grid: dict, e: tuple) -> dict:
    result = {}
    for position, char in grid.items():
        r, c = position
        result[((c - r) // 2, (len_c + (c - r) // 2 - r - c))] = char
        if position == e:
            e_rot = ((c - r) // 2, (len_c + (c - r) // 2 - r - c))
    return result, e_rot

def find_path(*, with_rotation: bool = False) -> int:
    heap = []
    heappush(heap, (0, 0, start))
    seen = set()
    while heap:
        dist, rot, position = heappop(heap)
        if rot == 0 and position == end:
            return dist
        if with_rotation:
            if rot == 1 and position == end_120:
                return dist
            if rot == 2 and position == end_240:
                return dist
        if (position, rot) in seen:
            continue
        seen.add((position, rot))
        neighbours = get_neighbours(position)
        if with_rotation:
            neighbours.append(position)
        for new_position in neighbours:
            if not with_rotation:
                if data.get(new_position) == "T":
                    heappush(heap, (dist + 1, 0, new_position))
            else:
                if rot == 0 and data_120.get(new_position) == "T":
                    heappush(heap, (dist + 1, 1, new_position))
                elif rot == 1 and data_240.get(new_position) == "T":
                    heappush(heap, (dist + 1, 2, new_position))
                elif rot == 2 and data.get(new_position) == "T":
                    heappush(heap, (dist + 1, 0, new_position))
    return 0

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    start = None
    end = None
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        len_r, len_c = parse_grid_of_char(file.read().strip().split("\n"))
    if args.part == 1:
        pairs = 0
        for r in range(len_r):
            for c in range(len_c):
                if data.get((r, c)) != "T":
                    continue
                if data.get((r, c + 1)) == "T":
                    pairs += 1
                if (not r % 2 and c % 2) or (r % 2 and not c % 2):
                    if data.get((r + 1, c)) == "T":
                        pairs += 1
        print(pairs) 
    elif args.part == 2:
        print(find_path())
    else:
        data_120, end_120 = rotate_once(data, end)
        data_240, end_240 = rotate_once(data_120, end_120)
        print(find_path(with_rotation=True))
    print(time() - t)
