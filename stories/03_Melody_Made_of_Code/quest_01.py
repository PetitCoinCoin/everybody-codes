import re

from dataclasses import dataclass
from pathlib import Path
from time import time

from utils.parsers import parse_args

@dataclass
class Scale:
    identifier: int
    red: int
    green: int
    blue: int
    shine: int

    @property
    def colorness(self) -> int:
        return self.red + self.green + self.blue
    
    @property
    def main_color(self) -> str:
        if self.red > self.green and self.red > self.blue:
            return "r"
        if self.green > self.red and self.green > self.blue:
            return "g"
        if self.blue > self.red and self.blue > self.green:
            return "b"
        return ""


def parse_input(line: str) -> Scale:
    pattern = r"(\d+):([rR]+) ([gG]+) ([bB]+)\s?([sS]*)"
    infos = re.findall(pattern, line)[0]
    return Scale(
        identifier=int(infos[0]),
        red=color_to_int(infos[1]),
        green=color_to_int(infos[2]),
        blue=color_to_int(infos[3]),
        shine=color_to_int(infos[4])
    )


def color_to_int(color: str) -> int:
    if not color:
        return 0
    as_bin = "".join("1" if char.isupper() else "0" for char in color)
    return int(as_bin, 2)


def assign_group(scale: Scale) -> None:
    key = scale.main_color
    if not key:
        return
    if scale.shine <= 30:
        key += "m"
    elif scale.shine >= 33:
        key += "s"
    else:
        return
    groups[key].add(scale.identifier)


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    if args.part == 1:
        print(sum(
            scale.identifier
            for scale in data
            if scale.main_color == "g"
        ))
    elif args.part == 2:
        max_shine = max(scale.shine for scale in data)
        max_darkness = min(scale.colorness for scale in data if scale.shine == max_shine)
        print(next(
            scale.identifier for scale in data
            if scale.shine == max_shine and scale.colorness == max_darkness
        ))
    else:
        groups = {
            key: set()
            for key in ("rm", "gm", "bm", "rs", "gs", "bs")
        }
        for scale in data:
            assign_group(scale)
        max_group = max(groups, key=len)
        print(sum(groups[max_group]))
    print(time() - t)
