from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from time import time

from utils.parsers import parse_args

@dataclass
class Hand:
    direction: int
    start: int
    moves: int
    steps: int

    def count_crossings(self, hand: Hand) -> int:
        pattern_start = 0
        pattern_crossings = []
        additional_crossings = 0
        lc_multiple = math.lcm(self.steps, hand.steps)
        self_step = lc_multiple // self.steps
        hand_step = lc_multiple // hand.steps
        prev_self = self.start * self_step
        prev_hand = hand.start * hand_step
        m = 1
        while m - pattern_start < lc_multiple:
            next_self = prev_self + self_step * self.direction
            next_hand = prev_hand + hand_step * hand.direction
            if self.direction < 0 and next_self and prev_self * next_self <= 0:
                prev_self += lc_multiple
                next_self += lc_multiple
            if hand.direction < 0 and next_hand and prev_hand * next_hand <= 0:
                prev_hand += lc_multiple
                next_hand += lc_multiple
            if prev_self % lc_multiple == prev_hand % lc_multiple:
                pass
            elif (prev_self - prev_hand) * (next_self - next_hand) <= 0 or next_self % lc_multiple == next_hand % lc_multiple:
                if not pattern_start:
                    pattern_start = m
                pattern_crossings.append(m - pattern_start)
            prev_self = next_self % lc_multiple
            prev_hand = next_hand % lc_multiple
            m += 1

        if not pattern_start and self.steps != hand.steps:
            pattern_start = lc_multiple
            pattern_crossings = [0]
        
        max_hand = self if self.moves >= hand.moves else hand
        max_step = lc_multiple // max_hand.steps
        min_hand = self if self.moves < hand.moves else hand
        min_step = lc_multiple // min_hand.steps
        
        full = min_hand.moves // lc_multiple

        min_end_position = (min_hand.start * min_step + min_hand.direction * min_step * min_hand.moves) % lc_multiple
        max_end_position = (max_hand.start * max_step + max_hand.direction * max_step * min_hand.moves) % lc_multiple
        
        additional_crossings, rest = divmod(max_hand.moves - min_hand.moves, max_hand.steps)
        end_position = (max_hand.start * max_step + max_hand.direction * max_step * max_hand.moves) % lc_multiple

        if max_hand.direction == 1:
            if min_end_position != max_end_position and (end_position - min_end_position) % lc_multiple <= rest * max_step:
                additional_crossings += 1
        else:
            if min_end_position != max_end_position and (min_end_position - end_position) % lc_multiple <= rest * max_step:
                additional_crossings += 1
        return full * len(pattern_crossings) + sum(pattern_start + full * lc_multiple + m <= min_hand.moves for m in pattern_crossings) + additional_crossings

    def bruteforce_count_crossings(self, hand: Hand) -> int:
        """
        Sure it works. Keeping it for the archive.
        """
        crossings = 0
        lc_multiple = math.lcm(self.steps, hand.steps)
        self_step = lc_multiple // self.steps
        hand_step = lc_multiple // hand.steps
        prev_self = self.start * self_step
        prev_hand = hand.start * hand_step
        for m in range(1, max(self.moves, hand.moves) + 1):
            next_self = prev_self + self_step * self.direction if m <= self.moves else prev_self
            next_hand = prev_hand + hand_step * hand.direction if m <= hand.moves else prev_hand
            if self.direction < 0 and next_self and prev_self * next_self <= 0:
                prev_self += lc_multiple
                next_self += lc_multiple
            if hand.direction < 0 and next_hand and prev_hand * next_hand <= 0:
                prev_hand += lc_multiple
                next_hand += lc_multiple
            if prev_self % lc_multiple == prev_hand % lc_multiple:
                pass
            elif (prev_self - prev_hand) * (next_self - next_hand) <= 0 or next_self % lc_multiple == next_hand % lc_multiple:
                crossings += 1
            prev_self = next_self % lc_multiple
            prev_hand = next_hand % lc_multiple
        return crossings

def parse_input(lines: str) -> list[Hand]:
    hands = [int(x) for x in lines[0].split(" ")[-1].split(":")]
    directions = [1 if x == "CW" else -1 for x in lines[1].split(" ")[-1].split(":")]
    starts = [int(x) for x in lines[2].split(" ")[-1].split(":")]
    moves = [int(x) for x in lines[3].split(" ")[-1].split(":")]
    return [
        Hand(direction=d, start=s, moves=m, steps=h)
        for d, s, m, h in zip(directions, starts, moves, hands)
    ]

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(blocks.split("\n")) for blocks in file.read().strip().split("\n\n")]

    print(sum(
        sum(
            portal[i].count_crossings(portal[j])
            for i in range(len(portal) - 1)
            for j in range(i + 1, len(portal))
        )
        for portal in data
    ))
    print(time() - t)
