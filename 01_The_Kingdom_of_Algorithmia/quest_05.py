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


def dance_turn(round_nb: int, places: dict) -> None:
    columns = len(places)
    clap_col = round_nb % columns
    clapper = places[clap_col].pop(0)
    dancing_col = (clap_col + 1) % columns
    side, idx = divmod(clapper, len(places[dancing_col]))
    if (side % 2 and idx) or (not side % 2 and not idx):  # right
        if idx == 1:
            places[dancing_col].append(clapper)
        else:
            places[dancing_col].insert(-idx + 1, clapper)
    elif side % 2 or (not side % 2 and idx):  # left
        places[dancing_col].insert(idx - 1, clapper)
    

def dance(nb_round: int, places: dict) -> str:
    i = 0
    while i < nb_round:
        dance_turn(i, places)
        i += 1
    return "".join(str(col[0]) for col in places.values())

def dance_for_real(places: dict) -> int:
    shouted = {}
    i = 0
    while True:
        dance_turn(i, places)
        number = "".join(str(col[0]) for col in places.values())
        shouted[number] = shouted.get(number, 0) + 1
        i += 1
        if shouted[number] == 2024:
            return int(number) * i

def infinite_dance(places: dict) -> str:
    shouted = set()
    config = {}
    i = 0
    columns = len(places)
    while True:
        conf = str(i % columns) + "-".join(["".join(str(x) for x in col) for col in places.values()])
        if config.get(conf):
            return max(shouted)
        config[conf] = True
        dance_turn(i, places)
        number = "".join(str(col[0]) for col in places.values())
        shouted.add(number)
        i += 1

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        while line:=file.readline():
            for i, val in enumerate(line.split(" ")):
                data[i] = data.get(i, [])
                data[i].append(int(val.strip()))
    if args.part == 1:
        print(dance(10, data))
    elif args.part == 2:
        print(dance_for_real(data))
    else:
        print(infinite_dance(data))
    print(time() - t)
