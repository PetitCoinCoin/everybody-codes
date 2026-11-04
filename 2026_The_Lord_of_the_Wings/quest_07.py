import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from time import time

from utils.parsers import parse_args

LIMIT = 1000000


@dataclass
class Cloud:
    cid: int
    energy: int
    connections: list[int]


def parse_input(raw: str) -> None:
    matches = re.findall(r"(\d+)", raw)
    data[int(matches[0])] = Cloud(
        cid=int(matches[0]), energy=int(matches[1]), connections=[int(x) for x in matches[2:]]
    )


def propagate_impulse(to_handle: dict[int, dict[int, int]], *, with_explosion: bool = False) -> None:
    exploded = set()
    while to_handle:
        to_handle_next = {}
        for cloud_id, values in to_handle.items():
            if cloud_id in exploded:
                continue
            for strength, nb in values.items():
                data[cloud_id].energy += nb * strength
            for c_id in data[cloud_id].connections:
                if c_id in exploded:
                    continue
                if c_id not in to_handle_next:
                    to_handle_next[c_id] = {}
                for strength, nb in values.items():
                    if strength > 1:
                        to_handle_next[c_id][strength - 1] = to_handle_next[c_id].get(strength - 1, 0) + nb

            if with_explosion and data[cloud_id].energy > LIMIT:
                exploded.add(cloud_id)
                for c_id in data[cloud_id].connections:
                    if c_id in exploded:
                        continue
                    if c_id not in to_handle_next:
                        to_handle_next[c_id] = {}
                    to_handle_next[c_id][10] = to_handle_next[c_id].get(10, 0) + 1
        to_handle = to_handle_next if [k for k, v in to_handle_next.items() if v] else None
    return exploded


if __name__ == "__main__":
    args = parse_args()
    t = time()
    data: dict[int, Cloud] = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        for line in file.read().strip().split("\n"):
            parse_input(line)
    init_strength = 5 if args.part == 1 else 10
    if args.part != 3:
        start = sorted(data.values(), key=lambda x: len(x.connections))[-1].cid
        propagate_impulse({start: {init_strength: 1}})
        print(sum(cloud.energy for cloud in data.values()))
    else:
        init_data = deepcopy(data)
        max_energy = 0
        for start in data.keys():
            data = deepcopy(init_data)
            exploded = propagate_impulse({start: {init_strength: 1}}, with_explosion=True)
            max_energy = max(max_energy, sum(cloud.energy for cloud in data.values() if cloud.cid not in exploded))
        print(max_energy)
    print(time() - t)
