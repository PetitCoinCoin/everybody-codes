from itertools import takewhile
from pathlib import Path
from time import time

from utils.parsers import parse_args


def flip(shelf: str, *, count_moves_only: bool = False) -> int:
    flips = 0
    L = len(shelf)
    i = 0
    while i < L:
        offset = 1
        while i + offset < L and shelf[i + offset] == shelf[i]:
            offset += 1
        try:
            idx = shelf[: i + offset - 1 : -1].index(shelf[i])
        except ValueError:
            i += offset
            continue
        if idx < L - 1 - (i + offset):
            flips += 1 if count_moves_only else (L - idx - (i + offset))
            shelf = shelf[: i + offset] + shelf[L - idx - 1 : i + offset - 1 : -1] + shelf[L - idx :]
        i += offset
    return flips


def model_flip(shelf: str, quantity: int = 10) -> int:
    flips = 0
    L = len(shelf)
    char = shelf[0]
    start = shelf[::]
    end = shelf[::-1]  # reversed
    loop = 0
    rep = 1
    init_start = start
    init_end = end
    tale = ""
    while 2 * rep <= quantity + 1:
        while start:
            if quantity - 2 * rep < 0:
                if start[0] == char:
                    flips += len(list(takewhile(lambda x: x == char, start)))
                else:
                    start = char + start
                return flips + flip(start), ""
            else:
                loop += 1
                ls, le = 1, 1
                if start[0] == char:
                    while ls < len(start) and start[ls] == char:
                        ls += 1
                    nb_start = len(start) - ls
                else:
                    nb_start = len(start)
                j = end.index(char)
                while j + le < len(end) and end[j + le] == char:
                    le += 1
                nb_end = len(end) - j

                flips += (quantity - 2 * rep) * L + nb_start + nb_end
                if rep == 1:
                    tale = end[::-1][nb_end:] + tale
                new_start = end[j + le :]  # already reversed
                end = start[-nb_start:]
                start = new_start
        rep += 1
    
        if 2 * rep <= quantity + 1:
            start = init_start if not loop % 2 else init_start[::-1]
            end += init_end if not loop % 2 else init_end[::-1]

    return flips, "".join(x for x in end[::-1] if x != char) + tale


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().strip()
    if args.part == 1:
        print(flip(data, count_moves_only=True))
    elif args.part == 2:
        print(flip(data * 10))
    else:
        total_flip = 0
        for i in range(3):
            flips, data = model_flip(data, quantity=100 // (2**i))
            total_flip += flips
        print(total_flip)
    print(time() - t)
