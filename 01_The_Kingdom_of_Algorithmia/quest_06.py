import argparse

from collections import deque
from copy import deepcopy
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
class Node:
    name: str
    children: list
    path: str

def build_tree(raw) -> tuple:
    name = raw.split(":")[0]
    children = raw.split(":")[1].split(",")
    if name in ("ANT", "BUG"):  # From data analysis
        children = ["@"]
    return name, children

def get_finest(tree: dict, *, is_full: bool = True) -> str:
    paths_len = {}
    queue = deque(["RR"])
    while queue:
        node = tree[queue.popleft()]
        node.path += node.name if is_full else node.name[0]
        for child in node.children:
            if child == "@":
                path_len = len(node.path) + 1
                saved = paths_len.get(path_len, (0, ""))
                paths_len[path_len] = (saved[0] + 1, "") if saved[0] else (1, node.path + "@")
                continue
            if tree.get(child):
                tree[child].path = node.path
                queue.append(child)
    for count, val in paths_len.values():
        if count == 1:
            return val

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        while line := file.readline():
            name, children = build_tree(line.strip())
            data[name] = Node(name, children, "")
    print(get_finest(data, is_full=args.part == 1))
    print(time() - t)
