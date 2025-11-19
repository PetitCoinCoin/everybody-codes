import argparse
import math

from itertools import permutations
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

MAP_DIR = {
    "R": 1,
    "L": -1,
}

def parse_input(raw_game: str, raw_tokens: str) -> tuple:
    for r, row in enumerate(raw_game.split("\n")):
        for c, char in enumerate(row):
            if char == ".":
                game.add((r, c))
            right = c
        last_row = r
    return last_row, right, raw_tokens.split("\n")

def slot_to_position(slot: int) -> int:
    if slot % 2:
        return (slot - 1) * 2
    return (slot - 2) * 2 + 2

def position_to_slot(pos: int) -> int:
    if pos % 4:
        return (pos - 2) // 2 + 2
    return pos // 2 + 1

def play_token(slot: int, token: str) -> int:
    r = -1
    c = slot_to_position(slot)
    for char in token:
        if r == final_row:
            break
        if not c:
            dc = 1
        elif c == right_border:
            dc = -1
        else:
            dc = MAP_DIR[char]
        c += dc
        while (r + 1, c) in game:
            r += 1
    return max(position_to_slot(c) * 2 - slot, 0)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    game = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        final_row, right_border, tokens = parse_input(*file.read().strip().split("\n\n"))
    last_slot = position_to_slot(right_border)
    if args.part == 1:
        print(sum(play_token(s + 1, token) for s, token in enumerate(tokens)))
    elif args.part == 2:
        print(
            sum(
                max(play_token(s + 1, token) for s in range(last_slot))
                for token in tokens
            )
        )
    else:
        results = dict()
        for i, token in enumerate(tokens):
            results[i] = dict()
            for s in range(last_slot):
                results[i][s] = play_token(s + 1, token)
        min_win = math.inf
        max_win = 0
        for slots in permutations(range(last_slot), len(tokens)):
            min_win = min(
                min_win,
                sum(results[i][s] for i, s in zip(range(len(tokens)), slots)),
            )
            max_win = max(
                max_win,
                sum(results[i][s] for i, s in zip(range(len(tokens)), slots)),
            )
        print(min_win, max_win)
    print(time() - t)
