import argparse

def parse_args() -> argparse.Namespace:
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

def parse_grid_of_int(lines: list[str]) -> tuple:
    grid = {}
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            grid[(r, c)] = int(val)
            max_c = c
        max_r = r
    return grid, max_r, max_c
