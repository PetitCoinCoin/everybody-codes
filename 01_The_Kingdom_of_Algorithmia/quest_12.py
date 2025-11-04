import argparse
import math

from dataclasses import dataclass
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

@dataclass
class Target:
    x: int
    y: int
    type: str

def parse_input(raw: str, y: int) -> list[Target]:
    x = -1
    targets = []
    for i in range(len(raw)):
        if raw[i] in "TH":
            targets.append(Target(x, y, raw[i]))
        x += 1
    return targets

def shooting_power(target: Target) -> int:
    for start in [
        Target(0, 0, "A"),
        Target(0, 1, "B"),
        Target(0, 2, "C"),
    ]:
        distance = target.x - start.x + target.y - start.y
        if distance / 3 == distance // 3:
            mul = 2 if target.type == "H" else 1
            return distance // 3 * (start.y + 1) * mul
    return 0

def shoot(target: Target) -> int:
    ranking = 1000000000
    height = 0
    delta = target.x // 2
    is_shot = False
    for start in [
        Target(0, 0, "A"),
        Target(0, 1, "B"),
        Target(0, 2, "C"),
    ]:
        # can't be reached
        if start.y + delta < target.y - delta:
            continue
        power_limit = math.ceil(delta / 2)
        # reached while projectile is moving up
        if start.y + delta == target.y - delta:
            is_shot = True
            power = delta
            temp_ranking = power * (start.y + 1)
        # reached while projectile is moving horizontally
        elif target.y - delta >= start.y + power_limit:
            is_shot = True
            power = target.y - delta - start.y
            temp_ranking = power * (start.y + 1)
        # reached while projectile is moving down
        else:
            height_diff = target.y - delta - start.y
            if (delta + height_diff) // 3 == (delta + height_diff) / 3:
                temp_ranking = (delta + height_diff) // 3 * (start.y + 1)
                is_shot = True
            else:
                continue
        if target.y - delta > height:
            height = target.y - delta
            ranking = temp_ranking
        elif target.y - delta == height and temp_ranking < ranking:
            ranking = temp_ranking
    return ranking if is_shot else 0

def shoot_moving(target: Target) -> int:
    if target.x % 2:
        target.x -= 1
        target.y -= 1
    while target.x and target.y:
        power = shoot(target)
        if power:
            # print("et hop")
            return power
        target.x -= 1
        target.y -= 1
    print("head shot!")
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = []
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        lines = file.readlines()
        if args.part in (1, 2):
            y = len(lines) - 2
            for line in lines:
                data.extend(parse_input(line, y))
                y -= 1
        else:
            data = [Target(int(line.split()[0]), int(line.strip().split()[1]), "#") for line in lines]
    if args.part in (1, 2):
        print(sum([shooting_power(target) for target in data]))
    else:
        print(sum([shoot_moving(target) for target in data]))
    print(time() - t)
