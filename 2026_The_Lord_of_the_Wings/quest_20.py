from itertools import dropwhile, takewhile
from pathlib import Path
from time import time

from utils.parsers import parse_args

SEGMENTS = {
    "1": 2,
    "2": 5,
    "3": 5,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 3,
    "8": 7,
    "9": 6,
    "0": 6,
    "+": 2,
    "-": 1,
    "=": 2,
    "A": 6,
}

MINUS_ONE = {
    "6": ("5",),
    "7": ("1",),
    "8": ("0", "6", "9", "A"),
    "9": ("5", "3"),
    "+": ("-",),
}

PLUS_ONE = {
    "1": ("7",),
    "3": ("9",),
    "5": ("6", "9"),
    "6": ("8",),
    "9": ("8",),
    "0": ("8",),
    "-": ("+",),
    "A": ("8",),
}

MOVE_ONE = {
    "2": ("3",),
    "3": ("2", "5"),
    "5": ("3",),
    "6": ("9", "0", "A"),
    "9": ("6", "0", "A"),
    "0": ("9", "6", "A"),
    "A": ("9", "6", "0"),
}


def is_correct(equation: list, base: int) -> bool:
    formatted_equation = "".join(
        str(int(char, base)) if char not in "+-=" else char
        for char in equation
    )
    while formatted_equation.startswith("0"):
        formatted_equation = formatted_equation[1:]
    return eval(formatted_equation.replace("=", "=="))

def can_fix(equation: list[str], base: int) -> bool:
    left = list(takewhile(lambda x: x!= "=", equation))
    right = list(dropwhile(lambda x: x!= "=", equation))[1:]

    for src, dests in MOVE_ONE.items():
        for side, other_side in ((left, right), (right, left)):
            for idx in (i for i, c in enumerate(side[0]) if c == src):
                for dest in dests:
                    if is_correct([side[0][:idx] + dest + side[0][idx + 1:]] + side[1:], base) == is_correct(other_side, base):
                        return True
            for idx in (i for i, c in enumerate(side[-1]) if c == src):
                for dest in dests:
                    if is_correct(side[:-1] + [side[-1][:idx] + dest + side[-1][idx + 1:]], base) == is_correct(other_side, base):
                        return True

    for minus_src, minus_dests in MINUS_ONE.items():
        for src_i in range(3):
            for side, other_side in ((left, right), (right, left)):
                for minus_idx in (i for i, c in enumerate(side[src_i]) if c == minus_src):
                    for minus_dest in minus_dests:
                        minus_left = side[:src_i] + [side[src_i][:minus_idx] + minus_dest + side[src_i][minus_idx + 1:]] + side[src_i + 1:]
                        for plus_src, plus_dests in PLUS_ONE.items():
                            for dest_i in range(3):
                                for plus_idx in (i for i, c in enumerate(minus_left[dest_i]) if c == plus_src):
                                    for plus_dest in plus_dests:
                                        if is_correct(minus_left[:dest_i] + [minus_left[dest_i][:plus_idx] + plus_dest + minus_left[dest_i][plus_idx + 1:]] + minus_left[dest_i + 1:], base) == is_correct(other_side, base):
                                            return True
                                for plus_idx in (i for i, c in enumerate(other_side[dest_i]) if c == plus_src):
                                    for plus_dest in plus_dests:
                                        if is_correct(other_side[:dest_i] + [other_side[dest_i][:plus_idx] + plus_dest + other_side[dest_i][plus_idx + 1:]] + other_side[dest_i + 1:], base) == is_correct(minus_left, base):
                                            return True
    return False

def number_to_base_str(n: int, base: int) -> str:
    if n == 0 or base == 10:
        return str(n)
    digits = []
    while n:
        digits.append(str(n % base))
        n //= base
    return "".join(digits[::-1])

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [line.split(" ") for line in file.read().strip().split("\n")]
    base = 10 if args.part == 1 else 11
    print(number_to_base_str(
        sum(
            sum(
                sum(SEGMENTS[c] for c in char)
                for char in equation
            )
            for equation in data
            if is_correct(equation, 11) or (args.part == 3 and can_fix(equation, base))
        ),
        base
    ))
    print(time() - t)
