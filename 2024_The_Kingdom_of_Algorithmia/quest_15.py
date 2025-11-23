import argparse

from collections import Counter
from copy import deepcopy
from heapq import heapify, heappop, heappush
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

def parse_input(area: dict, specific: dict, raw: str, i: int) -> None:
    for c, char in enumerate(raw):
        if char not in "~#":
            area[(c, i)] = char
            if char != ".":
                specific[char] = specific.get(char, set()) | {(c, i)}

def parse_part_3(area: dict) -> tuple:
    data_l = {}
    herbs_l = {}
    data_m = {}
    herbs_m = {}
    data_r = {}
    herbs_r = {}
    for key, val in area.items():
        col = key[0] // (col_nb // 3)
        if col == 2:
            data_r[key] = val
            if val != ".":
                herbs_r[val] = herbs_r.get(val, set()) | {key}
            if val == "R":
                entry_r = key
        elif col == 1:
            data_m[key] = val
            if val != ".":
                herbs_m[val] = herbs_m.get(val, set()) | {key}
        else:
            data_l[key] = val
            if val != ".":
                herbs_l[val] = herbs_l.get(val, set()) | {key}
            if val == "E":
                entry_l = key
    return data_l, herbs_l, data_m, herbs_m, data_r, herbs_r, entry_l, entry_r

def next_steps(area: dict, step: tuple, seen: dict) -> set:
    steps = set()
    x, y = step
    for delta in (1, -1):
        if (x + delta, y) not in seen and area.get((x + delta, y)):
            steps.add((x + delta, y))
        if (x, y + delta) not in seen and area.get((x, y + delta)):
            steps.add((x, y + delta))
    return steps

def get_herb(area: dict, start: tuple) -> int:
    seen = {}
    queue = [(0, start)]
    heapify(queue)
    while queue:
        distance, step = heappop(queue)
        if area[step] == "H":
            return distance
        seen[step] = True
        for next_step in next_steps(area, step, seen):
            heappush(queue, (distance + 1, next_step))
    return 0

def distance_between(area: dict, start: tuple, end: set) -> dict:
    seen = {}
    dist = {}
    queue = set([start])
    distance = 0
    while queue:
        new_queue = set()
        for step in queue:
            if step in end:
                dist[step] = distance
            if len(dist) == len(end):
                return dist
            seen[step] = True
            new_queue |= next_steps(area, step, seen)
        distance += 1
        queue = new_queue
    return dist

def get_harvest(area: dict, specific: dict, start: tuple, *, is_part_3_middle: bool = False) -> int:
    distances = {}
    spec = deepcopy(specific)
    herb_list = list(spec.keys())
    for herb_type in herb_list:
        group = spec.pop(herb_type)
        for herb in group:
            for other_group in spec.values():
                for step, dist in distance_between(area, herb, other_group).items():
                    distances[(min(herb, step), max(herb, step))] = dist
    queue = []
    heappush(queue, (0, start, ""))
    end_state = sorted(specific.keys())
    while queue:
        dist, step, seen = heappop(queue)
        if sorted(seen) == end_state:
            return dist
        if len(seen) == len(end_state) - 1:
            # search for start char
            candidates = {start}
        else:
            # search for new
            candidates = set()
            for other_herb, group in specific.items():
                if other_herb != area[start] and (
                    (other_herb not in seen and not is_part_3_middle)
                    or is_part_3_middle):
                    if is_part_3_middle and Counter(seen)["K"] == 1 and other_herb == "K":
                        candidates = {herb for herb in group if herb != step}
                        print("pouet", candidates, seen)
                    elif not is_part_3_middle or other_herb not in seen:
                        candidates.update(group)
        for candidate in candidates:
            heappush(queue, (dist + distances[min(candidate, step), max(candidate, step)], candidate, seen + area[candidate]))
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    herbs = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            parse_input(data, herbs, line.strip(), i)
            col_nb = len(line.strip())
            i += 1
    for key in data.keys():
        if not key[1]:
            entry = key
            data[key] = "+"
            herbs["+"] = {entry}
    if args.part == 1:
        print(2 * get_herb(data, entry))
    elif args.part == 2:
        print(get_harvest(data, herbs, entry))
    else:
        data_l, herbs_l, data_m, herbs_m, data_r, herbs_r, entry_l, entry_r = parse_part_3(data)
        min_left = get_harvest(data_l, herbs_l, entry_l)
        min_middle = get_harvest(data_m, herbs_m, entry, is_part_3_middle=False)
        min_right = get_harvest(data_r, herbs_r, entry_r)
        print(min_left + min_middle + min_right + 6*2)
    print(time() - t)
