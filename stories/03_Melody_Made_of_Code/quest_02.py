from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_input(lines: list[str]) -> tuple:
    source = None
    v_bones = []
    for r, line in enumerate(lines, 1):
        for c, char in enumerate(line):
            if char == "@":
                source = complex(c, (len(lines) - r))
            elif char == "#":
                v_bones.append(complex(c, (len(lines) - r)))
    return max(r, c) + 1, [v_bone - source for v_bone in v_bones]


def propagate_wave(*, until_surrounded: bool = False) -> int:
    v_bone = data[0]

    def is_surrounded(item: complex) -> bool:
        return all(str(item + s) in wave for s in seq)

    def get_condition() -> bool:
        if until_surrounded:
            return not is_surrounded(v_bone)
        return step != v_bone

    seq = [1j, 1, -1j, -1]
    wave = set()
    wave.add("0j")
    if until_surrounded:
        wave.add(str(v_bone))
    step = complex(0)
    counter = 0
    missed = 0
    while get_condition():
        while str(seq[(counter + missed) % len(seq)] + step) in wave:
            missed += 1
        step += seq[(counter + missed) % len(seq)]
        wave.add(str(step))
        if until_surrounded:
            for delta in seq:
                if str(step + delta) not in wave and is_surrounded(step + delta):
                    wave.add(str(step + delta))
        counter += 1
    return counter


def propagate_wave_multi() -> int:
    def is_surrounded(item: complex) -> bool:
        return all(
            any(
                str(item + mul * direction) in wave
                for mul in range(1, max_dim)
            )
            for direction in base_seq
        )
    
    def is_fully_surrounded(item: complex, seen: set[str]) -> bool:
        if not is_surrounded(item):
            return False
        neighbors = []
        for delta in base_seq:
            for mul in range(1, max_dim):
                if str(item + mul * delta) not in wave and str(item + mul * delta) not in seen:
                    neighbors.append(item + mul * delta)
                else:
                    break
        seen.add(str(item))
        return all(
            is_fully_surrounded(n, seen)
            for n in neighbors
        )

    base_seq = [1j, 1, -1j, -1]
    seq = [1j, 1j, 1j, 1, 1, 1, -1j, -1j, -1j, -1, -1, -1]
    wave = set([str(v_bone) for v_bone in data])
    wave.add("0j")
    step = complex(0)
    counter = 0
    missed = 0
    v_seen = set()
    while any(not is_fully_surrounded(v_bone, v_seen) for v_bone in data):
        seen = set()
        while str(next_step := seq[(counter + missed) % len(seq)] + step) in wave or is_fully_surrounded(next_step, seen):
            missed += 1
        step += seq[(counter + missed) % len(seq)]
        wave.add(str(step))
        counter += 1
        # v_seen = set() - not necessary here, and divides runtime by 5
    return counter


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        max_dim, data = parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        print(propagate_wave())
    elif args.part == 2:
        print(propagate_wave(until_surrounded=True))
    else:
        print(propagate_wave_multi())
    print(time() - t)
