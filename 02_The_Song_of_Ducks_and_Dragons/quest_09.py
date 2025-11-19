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

def parse_input(lines: str) -> None:
    for line in lines.split("\n"):
        splitted = line.split(":")
        data[int(splitted[0])] = splitted[-1]

def find_children(*, is_part_three: bool) -> None:
    for child, dna_child in data.items():
        for p1, dna1 in data.items():
            if p1 == child or (not is_part_three and p1 in children):
                continue
            for p2, dna2 in data.items():
                if p2 == child or p2 == p1 or (not is_part_three and p2 in children):
                    continue
                for i in range(len(dna_child)):
                    if dna_child[i] != dna1[i] and dna_child[i] != dna2[i]:
                        break
                else:
                    if is_part_three:
                        children[child] = (p1, p2)
                    else:
                        children[child] = (p1, p2, similarity(dna_child, dna1) * similarity(dna_child, dna2))
                    break
            else:
                continue
            break

def similarity(dna1: str, dna2: str) -> int:
    return sum(
        x1 == x2
        for x1, x2 in zip(dna1, dna2)
    )

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        parse_input(file.read().strip())
    children = {}
    find_children(is_part_three=args.part == 3)
    if args.part != 3:
        print(sum(child[-1] for child in children.values()))
    else:
        families: list[set] = []
        for child, parents in children.items():
            for family in families:
                if child in family or parents[0] in family or parents[1] in family:
                    family.update({child, parents[0], parents[1]})
                    break
            else:
                families.append({child, parents[0], parents[1]})
        # Group families
        moved = True
        while moved:
            moved = False
            for i in range(len(families) - 1):
                for j in range(i + 1, len(families)):
                    if families[i].intersection(families[j]):
                        families = families[:i] + families[i + 1:j] + [families[i] | families[j]] + families[j + 1:]
                        moved = True
                        break
                else:
                    continue
                break
        biggest_family = max(families, key=len)
        print(sum(x for x in biggest_family))
    print(time() - t)
