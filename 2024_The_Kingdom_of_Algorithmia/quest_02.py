import argparse

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

def count_symbols(words: set, line: str) -> int:
    symbols = set()
    for i in range(len(line)):
        for word in words:
            if line[i:].startswith(word):
                for j in range(i, i + len(word)):
                    symbols.add(j)
                break
    return len(symbols)

def circular_count(words: set, lines: list) -> int:
    symbols = set()
    rows = len(lines)
    cols = len(lines[0])
    for k in range(rows):
        line = lines[k]
        for i in range(cols):
            for word in words:
                if (line[i:] + line).startswith(word):
                    for j in range(i, i + len(word)):
                        symbols.add((k, j % cols))
    for i in range(cols):
        col = "".join(line[i] for line in lines)
        for k in range(rows):
            for word in words:
                if col[k:].startswith(word):
                    for j in range(k, k + len(word)):
                        symbols.add((j % rows, i))
    return len(symbols)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().split("\n")
    runes = [word.strip() for word in data[0].split(":")[-1].split(",")]
    if args.part == 1:
        helmet = data[1]
        print(sum(helmet.count(rune) for rune in runes))
    elif args.part == 2:
        duplicate_runes = set(runes + [rune[::-1] for rune in runes])
        print(sum(count_symbols(duplicate_runes, line) for line in data[1:]))
    else:
        duplicate_runes = set(runes + [rune[::-1] for rune in runes])
        print(circular_count(duplicate_runes, data[1:]))
    print(time() - t)
