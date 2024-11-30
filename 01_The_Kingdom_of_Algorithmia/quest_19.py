import argparse

from copy import deepcopy
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

def parse_input(msg: dict, imag: int, raw: str) -> None:
    for r, char in enumerate(raw):
        msg[complex(r, -imag)] = char

def rotate(msg: dict, pivot: complex, direction: str) -> tuple:
    prev_char = msg[pivot + 1j]
    delta = 1j
    new_pos = 0
    start, end = None, None
    for d in (-1, -1j, -1j, +1, +1, +1j, +1j, -1) if direction == "L" else (1, -1j, -1j, -1, -1, +1j, +1j, +1):
        new_pos = pivot + delta + d
        replaced = msg[new_pos]
        msg[new_pos] = prev_char
        if prev_char == ">":
            start = new_pos
        elif prev_char == "<":
            end = new_pos
        prev_char = replaced
        delta += d
    return start, end

def decrypt(msg: dict, instructions: str, row: int, col: int, iteration: int = 0, *, part: int = 1) -> str:
    start = None
    end = None
    cpt = 0
    for i in range(1, row + 1):
        for r in range(1, col + 1):
            loc_start, loc_end = rotate(msg, complex(r, -i), instructions[cpt % len(instructions)])
            if part == 2 and iteration < 99:
                cpt += 1
                continue
            if loc_start:
                start = loc_start
            if loc_end:
                end = loc_end
            if start and end and start.imag == end.imag:
                result = "".join(msg[complex(c, int(start.imag))] for c in range(int(start.real) + 1, int(end.real)))
                if not part == 2 or "." not in result:
                    return result
            cpt += 1
    return ""

def rotate_cycle(msg: dict, instructions: str, row: int, col: int) -> dict:
    cycle = {k: k for k in msg.keys()}
    cpt = 0
    for i in range(1, row + 1):
        for r in range(1, col + 1):
            rotate(cycle, complex(r, -i), instructions[cpt % len(instructions)])
            cpt += 1
    return cycle

def squaring_exp(msg: dict, power: int, cycle: dict, row: int, col: int) -> dict:
    performed = {}
    performed[1] = cycle
    exp = 1
    while exp < power:
        decrypted = performed[exp]
        exp *= 2
        performed[exp] = {k: decrypted[v] for k, v in decrypted.items()}
    required = [k for k in performed.keys() if k & power]
    result = {}
    for r in range(row + 2):
        for c in range(col + 2):
            cell = complex(c, -r)
            for two_power in required:
                cell = performed[two_power][cell]
            result[complex(c, -r)] = msg[cell]
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    notes = ""
    data = {}
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        lines = file.read()
        notes = lines.split("\n\n")[0]
        for i, line in enumerate(lines.split("\n\n")[1].split("\n")):
            parse_input(data, i, line.strip())
            cols = len(line.strip()) - 2
            rows = i - 1
    if args.part == 1:
        print(decrypt(data, notes, rows, cols))
    elif args.part == 2:
        for iteration in range(100):
            decoded = decrypt(data, notes, rows, cols, iteration, part=2)
        print(decoded)
    else:
        cycle = rotate_cycle(data, notes, rows, cols)
        end_state = squaring_exp(data, 1048576000, cycle, rows, cols)
        for key, val in end_state.items():
            if val == ">":
                start = key
            if val == "<":
                end = key
        print("".join(end_state[complex(c, int(start.imag))] for c in range(int(start.real) + 1, int(end.real))))
    print(time() - t)
