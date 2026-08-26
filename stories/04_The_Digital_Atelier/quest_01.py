from pathlib import Path
from time import time

from utils.parsers import parse_args


def is_crossing(old_pos: int, new_pos: int, segments: list[list[int]]) -> bool:
    return any(
        (old_pos in range(s[0], s[1] + 1)) ^ (new_pos in range(s[0], s[1] + 1))
        for s in segments
    )


def trace(points: list[int], part: int) -> int:
    pos = 0
    seen = {0}
    ups = []
    downs = []
    max_pos = 0
    is_down = True

    for point in points:
        prev_pos = pos
        segments = downs if is_down else ups
        skip = False
        if (
            (new_pos := pos - point) > 0
            and new_pos not in seen
            and (part < 3 or not is_crossing(prev_pos, new_pos, segments))
        ):
            pos = new_pos
        else:
            pos += point
            if part > 1:
                while pos in seen or (
                    part == 3 and is_crossing(prev_pos, pos, segments)
                ):
                    if part == 3 and pos > max_pos:
                        pos = prev_pos
                        skip = True
                        break
                    pos += 1
                if skip:
                    continue
        seen.add(pos)
        max_pos = max(max_pos, pos)
        segments.append((min(prev_pos, pos), max(prev_pos, pos)))
        is_down = not is_down
    return pos


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(
        f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt"
    ).open("r") as file:
        data = [
            [int(x) for x in line.split(",")]
            for line in file.read().strip().split("\n")
        ]
        print(sum(trace(points, args.part) for points in data))
    print(time() - t)
