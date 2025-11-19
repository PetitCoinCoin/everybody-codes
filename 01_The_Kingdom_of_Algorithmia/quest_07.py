import argparse

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

ACTION_MAP = {
    "+": lambda x: x + 1,
    "-": lambda x: max(x - 1, 0),
    "=": lambda x: x,
}

def parse_input(data: dict, raw: str, row: int = 0, *, is_track: bool = False) -> None:
    if is_track:
        for i in range(len(raw)):
            if raw[i] != " ":
                data[complex(i, -row)] = raw[i]
    else:
        key = raw.split(":")[0]
        value = raw.split(":")[1].split(",")
        data[key] = value

def get_segment_power(actions: list) -> int:
    instant_power = 10
    segment_power = 0
    nb = 0
    while nb < 10:
        instant_power = ACTION_MAP[actions[nb % len(actions)]](instant_power)
        segment_power += instant_power
        nb += 1
    return segment_power

def get_from_track(actions: list, track: str, *, is_parth_three: bool = False) -> int:
    plan = len(actions)
    instant_power = 10
    segment_power = 0
    nb = 0
    delta = 0
    while nb < (11 if is_parth_three else 10):
        for i in range(len(track)):
            instant_power = ACTION_MAP[actions[(delta + i) % plan] if track[i] not in ("+", "-") else track[i]](instant_power)
            segment_power += instant_power
        delta += len(track) % plan
        nb += 1
    return segment_power

def get_track(plan: dict) -> str:
    track = ""
    step = complex(1, 0)
    direction = 1
    while plan[step] != "S":
        track += plan[step]
        step += direction
        if not plan.get(step + direction):
            for d in (direction * 1j, direction * -1j):
                if plan.get(step + d):
                    direction = d
                    break
    return track + "S"


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        while line := file.readline():
            parse_input(data, line.strip())
    if args.part == 1:
        powers = [(get_segment_power(val), key) for key, val in data.items()]
        powers.sort(reverse=True)
        print("".join(x[1] for x in powers))
    elif args.part == 2:
        tr = """S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-"""
        tr_split = tr.split("\n")
        track = tr_split[0][1:] + "".join(tr_split[i][-1] for i in range(1, len(tr_split) - 1)) + tr_split[-1][::-1] + "".join(tr_split[i][0] for i in range(len(tr_split) - 2, 0, -1)) + "S"
        powers = [(get_from_track(val, track, 10), key) for key, val in data.items()]
        powers.sort(reverse=True)
        print("".join(x[1] for x in powers))
        get_from_track(data["J"], track)
    else:
        tr = """S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-"""
        track_data = {}
        tr_split = tr.split("\n")
        for i in range(len(tr_split)):
            parse_input(track_data, tr_split[i], i, is_track=True)
        track = get_track(track_data)
        base_plan = ["+"] * 5 + ["-"] * 3 + ["="] * 3
        opponent_score = get_from_track(data["A"], track, is_parth_three=True)
        winning_plans = 0
        plans = set(permutations(base_plan))
        print(sum(1 if get_from_track(plan, track, is_parth_three=True) > opponent_score else 0 for plan in plans))
    print(time() - t)
