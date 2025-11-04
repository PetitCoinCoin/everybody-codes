import argparse

from collections import deque
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

FLUFFBOLTS = "RGB"

def play_in_line(balloons: str) -> int:
    f = 0
    b = 0
    while b < len(balloons):
        while b < len(balloons) and balloons[b] == FLUFFBOLTS[f % 3]:
            b += 1
        b += 1
        f += 1
    return f

def play_in_circle(balloons: str) -> int:
    f = 0
    while balloons:
        b_count = len(balloons)
        if b_count % 2:
            balloons = balloons[1:]
        else:
            if balloons[0] == FLUFFBOLTS[f % 3]:
                mid = b_count // 2
                balloons = balloons[1:mid] + balloons[mid + 1:]
            else:
                balloons = balloons[1:]
        f += 1
    return f

def play_simultaneously(ball_1: deque, ball_2: deque) -> int:
    f = 0
    while len(ball_1) + len(ball_2):
        if len(ball_1) > len(ball_2):
            raise "Something went wrong"
        if len(ball_1) < len(ball_2):
            balloon = ball_2.popleft()
            ball_1.append(balloon)
        if len(ball_1) == len(ball_2) and ball_1[0] == FLUFFBOLTS[f % 3]:
            ball_2.popleft()
        ball_1.popleft()
        f += 1
    return f

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().strip()
    if args.part == 1:
        print(play_in_line(data))
    elif args.part == 2:
        print(play_in_circle(data * 100))
    else:
        print(play_simultaneously(deque(data * 50000), deque(data * 50000)))
    print(time() - t)
