import argparse

from itertools import pairwise
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

def parse_input(lines: str) -> list:
    names = lines.split("\n\n")[0].split(",")
    for line in lines.split("\n\n")[1].split("\n"):
        key, values = tuple(line.split(" > "))
        data[key] = values.split(",")
    return names

def is_valid(name: str) -> bool:
    for from_char, to_char in pairwise(name):
        if to_char not in data[from_char]:
            return False
    return True

def count_arrangements(start_char: str, chars: list[str], loop: int = 1) -> None:
    if loop > 11:
        return
    counts[start_char].append(sum(
        len(data.get(char, []))
        for char in chars
    ))
    count_arrangements(start_char, [next_char for char in chars for next_char in data.get(char, [])], loop + 1)

def count_names(name: str) -> int:
    i = 0
    result = 0
    while len(name) + i <= 11:
        if len(name) + i >= 7:
            result += counts[name[-1]][i]
        i += 1
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        names = parse_input(file.read().strip())
    if args.part == 1:
        for name in names:
            if is_valid(name):
                print(name)
                break
    elif args.part == 2:
        print(sum(
            i + 1
            for i in range(len(names))
            if is_valid(names[i])
        ))
    else:
        names = [name for name in names if is_valid(name)]
        prefixes = [
            name for name in names
            if not any(n for n in names if n != name and name.startswith(n))
        ]
        last_letters = {}
        for prefix in prefixes:
            last_letters[prefix[-1]] = min(last_letters.get(prefix[-1], 11), len(prefix))
        counts = {char: [1] for char in last_letters}
        for char, loop in last_letters.items():
            count_arrangements(char, [char], loop + 1)
        print(sum(
            count_names(prefix)
            for prefix in prefixes
        ))
    print(time() - t)
