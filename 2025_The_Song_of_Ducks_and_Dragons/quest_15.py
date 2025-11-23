import operator

from heapq import heappop, heappush
from pathlib import Path
from time import time

from utils.parsers import parse_args

def parse_input(directions: list) -> complex:
    step = complex(0)
    d = 1j
    for direction in directions:
        if direction[0] == "R":
            d *= -1j
        else:
            d *= 1j
        for _ in range(1, int(direction[1:]) + 1):
            step += d
            data.add(step)
    return step

def parse_large_input(directions: list) -> tuple:
    rows = {}
    colums = {}
    step = complex(0)
    d = 1j
    for i, direction in enumerate(directions):
        if direction[0] == "R":
            d *= -1j
        else:
            d *= 1j
        if d.real:
            r = int(step.real)
            last_r = r + int(d.real * int(direction[1:]))
            rows[int(step.imag)] = range(min(r, last_r), max(r, last_r) + 1)
        else:
            i = int(step.imag)
            last_i = i + int(d.imag * int(direction[1:]))
            colums[int(step.real)] = range(min(i, last_i), max(i, last_i) + 1)
        step += int(direction[1:]) * d
    return (int(step.real), int(step.imag)), rows, colums

def find_exit() -> int:
    heap = []
    heappush(heap, (0, 0, 0))
    seen = set()
    while heap:
        segments, r, i = heappop(heap)
        step = complex(r, i)
        if step in seen:
            continue
        seen.add(step)
        for d in (1, -1, 1j, -1j):
            if step + d not in data:
                heappush(heap, (segments + 1, r + d.real, i + d.imag))
            elif step + d == end:
                return segments + 1
    return 0

def find_large_exit() -> int:
    heap = []
    heappush(heap, (0, (0, 0), (0, 0)))
    seen = set()
    start = True
    while heap:
        segments, from_d, step = heappop(heap)
        if step in ((re + 1, ie), (re - 1, ie), (re, ie + 1), (re, ie - 1)):
            return segments + 1
        if step == end:
            return segments
        if step in seen:
            continue
        seen.add(step)
        dist_to_end = is_direct(step, end)
        if dist_to_end:
            return segments + dist_to_end
        r, i = step
        from_dr, from_di = from_d
        for dr, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (r + dr in rows.get(i + di, [])) or (i + di in columns.get(r + dr, [])):
                continue  # next step is a wall
            if (dr and dr == -from_dr) or (di and di == -from_di):
                continue  # no turning back
            if start and ((dr and r + dr not in rows.get(i, [])) or (di and i + di not in columns.get(i, []))):
                heappush(heap, (segments + 1, (dr, di), (r + dr, i + di)))
            
            # Avoid if / elif / else depending on direction
            orth_keys = columns_keys if dr else rows_keys
            if dr < 0 or di < 0:
                orth_keys = orth_keys[::-1]
            orth_items = columns if dr else rows
            compare = operator.le if (dr > 0 or di > 0) else operator.ge
            dim = r if dr else i
            orth_dim = i if dr else r
            closest = -1 if (dr > 0 or di > 0) else 1

            # Search for orthogonal lines; add position just before, and just after (except if you need to cross the wall)
            for key in orth_keys:
                if compare(key, dim):
                    continue
                dist = abs(dim - key)
                if dist > 1:
                    position = (key + closest, orth_dim) if dr else (orth_dim, key + closest)
                    heappush(heap, (segments + dist - 1, (dr, di), position))
                    if orth_dim in orth_items[key]:
                        break
                    else:
                        position = (key - closest, orth_dim) if dr else (orth_dim, key - closest)
                        if orth_dim in orth_items.get(key - closest, []):
                            continue
                        heappush(heap, (segments + dist + 1, (dr, di), position))
        start = False
    return 0

def is_direct(pos1: tuple, pos2: tuple) -> int:
    r1, i1 = pos1
    r2, i2 = pos2
    for col in columns_keys:
        if min(r1, r2) < col < max(r1, r2) and (i1 in columns[col] or i2 in columns[col]):
            break
    else:
        for row in rows_keys:
            if min(i1, i2) < row < max(i1, i2) and (r1 in rows[row] or r2 in rows[row]):
                break
        else:
            return abs(r1 - r2) + abs(i1 - i2)
    return 0

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = set([complex(0)])
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        if args.part != 3:
            end = parse_input(file.read().strip().split(","))
        else:
            end, rows, columns = parse_large_input(file.read().strip().split(","))
    if args.part != 3:
        print(find_exit())
    else:
        re, ie = end
        columns_keys = sorted(columns.keys())
        rows_keys = sorted(rows.keys())
        print(find_large_exit())
    print(time() - t)
