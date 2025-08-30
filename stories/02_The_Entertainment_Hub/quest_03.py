import argparse
import re

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


class Dice:
    def __init__(self, values: list[int], seed: int) -> None:
        self.values: list[int] = values
        self.current: int = 0  # index
        self.seed: int = seed
        self.pulse: int = seed
        self.rolls: int = 0
        self.rank: int = 0  # index
        self.track: list[int] = []
        self.done: bool = False
    
    def add_track(self, track: list[int]) -> None:
        self.track = track

    def roll(self) -> int:
        if not self.done:
            self.rolls += 1
            spin = self.rolls * self.pulse
            self.current = (self.current + spin) % len(self.values)
            self.pulse = ((self.pulse + spin) % self.seed) + 1 + self.rolls + self.seed
            if self.track:
                self.__check_track()
            return self.values[self.current]
        return 0
    
    def __check_track(self):
        if self.values[self.current] == self.track[self.rank]:
            self.rank += 1
        if self.rank == len(self.track):
            self.done = True


def parse_input(raw: str, part: int) -> list:
    raw_split = raw.split("\n\n")
    pattern = r"(\d+): faces=\[([\d,\-]+)\] seed=(\d+)"
    for d_id, values, seed in re.findall(pattern, raw_split[0]):
        data[int(d_id)] = Dice(
            values=[int(x) for x in values.split(",")],
            seed=int(seed)
        )
    if part == 1:
        return []
    if part == 2:
        return [int(x) for x in raw_split[-1]]
    return raw_split[-1].split("\n")

def build_board() -> None:
    for r, row in enumerate(game):
        for c, char in enumerate(row):
            board[(r, c)] = int(char)

def play(dice: Dice) -> set:
    seen = set()
    start_value = dice.roll()
    positions = set()
    for pos, val in board.items():
        if val == start_value:
            positions.add(pos)
    while positions:
        next_value = dice.roll()
        next_positions = set()
        for r,c in positions:
            seen.add((r, c))
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)):
                if board.get((r + dr, c + dc)) == next_value:
                    next_positions.add((r + dr, c + dc))
        positions = next_positions
    return seen

def easter_egg() -> None:
    print("\n".join([
        "".join([
            "#" if (r, c) in coins else "."
            for c in range(len(row))
        ])
        for r, row in enumerate(game)
    ]))


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data: dict[int, Dice] = dict()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        game = parse_input(file.read().strip(), args.part)
    if args.part == 1:
        points = 0
        while points < 10000:
            for dice in data.values():
                points += dice.roll()
        print(data[1].rolls)
    elif args.part == 2:
        finished = []
        for dice in data.values():
            dice.add_track(game)
        while len(finished) < len(data.keys()):
            for player, dice in data.items():
                if dice.done:
                    if player not in finished:
                        finished.append(player)
                    continue
                dice.roll()
        print(",".join(str(x) for x in finished))
    else:
        board = dict()
        build_board()
        coins = set()
        for dice in data.values():
            coins |= play(dice)
        easter_egg()
        print(len(coins))
    print(time() - t)
