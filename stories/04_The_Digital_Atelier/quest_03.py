import math
from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_input(raw: list[str]) -> tuple:
    return (
        int(raw[0].split("=")[-1]),
        int(raw[1].split("=")[-1]),
        [int(x) for x in raw[2].split("=")[-1]],
        [int(x) for x in raw[3].split("=")[-1]],
    )


def place_stitches() -> None:
    lv = len(voff)
    lh = len(hoff)
    for x in range(lv):
        for y in range(lh):
            if not (hoff[(y + 1) % lh] ^ x % 2):
                grid[(x, y)][0] = 1
            if not (hoff[y] ^ x % 2):
                grid[(x, y)][2] = 1
            if not (voff[(x + 1) % lv] ^ y % 2):
                grid[(x, y)][1] = 1
            if not (voff[x] ^ y % 2):
                grid[(x, y)][3] = 1


def color_tiles(position: tuple) -> None:
    if position == (0, 0):
        current_color = 1
    else:
        current_color = colors[
            (position[0] - 1, position[1])
            if (position[0] - 1, position[1]) in grid
            else (position[0], position[1] - 1)
        ]
        current_color *= -1

    queue = {position}
    while queue:
        pos = queue.pop()
        x, y = pos
        colors[pos] = current_color
        for idx, shift in zip(range(4), ((0, 1), (1, 0), (0, -1), (-1, 0))):
            dx, dy = shift
            new_pos = (x + dx, y + dy)
            if new_pos in grid and not grid[pos][idx] and not colors[new_pos]:
                queue.add(new_pos)


def get_sub_part_count(color: int = 0) -> tuple:
    base = len(
        [
            coord
            for coord, tile in grid.items()
            if sum(tile) == 4 and (not color or colors[coord] == color)
        ]
    )
    partial_horizontal = len(
        [
            coord
            for coord, tile in grid.items()
            if sum(tile) == 4
            and coord[0] < width_r - 1
            and (not color or colors[coord] == color)
        ]
    )
    partial_vertical = len(
        [
            coord
            for coord, tile in grid.items()
            if sum(tile) == 4
            and coord[1] < height_r - 1
            and (not color or colors[coord] == color)
        ]
    )
    partial_corner = len(
        [
            coord
            for coord, tile in grid.items()
            if sum(tile) == 4
            and coord[0] < width_r - 1
            and coord[1] < height_r - 1
            and (not color or colors[coord] == color)
        ]
    )
    return base, partial_horizontal, partial_vertical, partial_corner


def get_color_count(color: int) -> int:
    base, partial_horizontal, partial_vertical, partial_corner = get_sub_part_count(
        color
    )
    (
        base_other,
        partial_horizontal_other,
        partial_vertical_other,
        partial_corner_other,
    ) = get_sub_part_count(-color)

    # Pattern is reproduced with the same colors among one direction if number of 1s in offset is even.
    # Otherwise, colors are inverted.
    if not sum(hoff) % 2:
        if not sum(voff) % 2:
            return (
                base * width_q * height_q
                + partial_horizontal * height_q
                + partial_vertical * width_q
                + partial_corner
            )
        else:
            return (
                (base * width_q + partial_horizontal) * math.ceil(height_q / 2)
                + (base_other * width_q + partial_horizontal_other) * math.floor(height_q / 2)
                + width_q * (partial_vertical_other if height_q % 2 else partial_vertical)
                + partial_corner_other if height_q % 2 else partial_corner
            )
    else:
        if not sum(voff) % 2:
            return (
                base * math.ceil(width_q / 2) * math.ceil(height_q / 2)
                + base_other * math.floor(width_q / 2) * math.floor(width_q / 2)
                + math.ceil(height_q / 2) * (partial_horizontal_other if width_q % 2 else partial_horizontal)
                + math.floor(height_q / 2) * (partial_horizontal if width_q % 2 else partial_horizontal_other)
                + math.ceil(width_q / 2) * (partial_vertical_other if height_q % 2 else partial_vertical)
                + math.floor(width_q / 2) * (partial_vertical if height_q % 2 else partial_vertical_other)
                + partial_corner_other if (height_q + width_q) % 2 else partial_corner
            )
        else:
            return (
                (base * height_q + partial_vertical) * math.ceil(width_q / 2)
                + (base_other * height_q + partial_vertical_other) * math.floor(width_q / 2)
                + height_q * (partial_horizontal_other if width_q % 2 else partial_horizontal)
                + partial_corner_other if width_q % 2 else partial_corner
            )


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(
        f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt"
    ).open("r") as file:
        width, height, hoff, voff = parse_input(file.read().strip().split("\n"))

    grid = {}
    # Base pattern has even length
    if len(hoff) % 2:
        hoff *= 2
    if len(voff) % 2:
        voff *= 2
    for x in range(len(voff)):
        for y in range(len(hoff)):
            grid[(x, y)] = [0, 0, 0, 0]  # top, right, bottom, left
    place_stitches()

    width_q, width_r = divmod(width + 1, len(voff))
    height_q, height_r = divmod(height + 1, len(hoff))

    if args.part == 1:
        (
            pattern,
            partial_horizontal_pattern,
            partial_vertical_pattern,
            partial_corner,
        ) = get_sub_part_count()
        print(
            pattern * width_q * height_q
            + partial_horizontal_pattern * height_q
            + partial_vertical_pattern * width_q
            + partial_corner
        )
    else:
        colors = {k: 0 for k in grid}
        for position, color in colors.items():
            if color:
                continue
            color_tiles(position)
        print(max(get_color_count(c) for c in (1, -1)))
    print(time() - t)
