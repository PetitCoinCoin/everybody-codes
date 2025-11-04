from __future__ import annotations

import argparse
import re

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
    _id: int
    rank: int
    symbol: str
    level: int = 0
    child_left: Node | None = None
    child_right: Node | None = None

    def __gt__(self, other: Node) -> bool:
        return self.rank > other.rank

class Tree:
    def __init__(self, root: Node) -> None:
        self.root = root
        self.root.level = 1
        self.levels = {}
    
    def insert(self, node: Node) -> None:
        tree_node = self.root
        tree_child = tree_node.child_left if node.rank < tree_node.rank else tree_node.child_right
        while tree_child:
            tree_node = tree_child
            tree_child = tree_node.child_left if node.rank < tree_node.rank else tree_node.child_right
        node.level = tree_node.level + 1
        if node.rank < tree_node.rank:
            tree_node.child_left = node
        else:
            tree_node.child_right = node
    
    def get_from_id(self, node: Node | None, id: int) -> Node | None:
        if not node:
            return None
        if node._id == id:
            return node
        return self.get_from_id(node.child_left, id) or self.get_from_id(node.child_right, id)

    def get_parent(self, node: Node | None, id: int) -> list:
        if not node:
            return []
        if node.child_left and node.child_left._id == id:
            return [(node, "left")] + self.get_parent(node.child_right, id)
        if node.child_right and node.child_right._id == id:
            return [(node, "right")] + self.get_parent(node.child_left, id)
        return self.get_parent(node.child_left, id) + self.get_parent(node.child_right, id)

    def reset_levels(self) -> None:
        self.levels = {}

    def build_levels(self, node: Node | None, level: int = 1) -> None:
        if not node:
            return
        node.level = level
        self.levels[level] = self.levels.get(level, 0) + 1
        self.build_levels(node.child_left, level + 1)
        self.build_levels(node.child_right, level + 1)
        return
        
    def decrypt_max(self) -> str:
        self.build_levels(self.root)
        max_level = max(self.levels, key=self.levels.get)
        return self.get_message(self.root, max_level)

    def get_message(self, node: Node | None, level: int) -> str:
        if not node:
            return ""
        if node.level == level:
            return node.symbol
        return self.get_message(node.child_left, level) + self.get_message(node.child_right, level)


def parse_input(raw: str) -> tuple[Node] | int:
    pattern = r"ADD id=(\d+) left=\[(\d+),(.)\] right=\[(\d+),(.)\]"
    infos = re.findall(pattern, raw)
    if infos:
        info = infos[0]
        return Node(_id=int(info[0]), rank=int(info[1]), symbol=info[2]), Node(_id=int(info[0]), rank=int(info[3]), symbol=info[4])
    return int(raw[5:])

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(row) for row in file.read().strip().split("\n")]
    root_left, root_right = data[0]
    tree_left = Tree(root_left)
    tree_right = Tree(root_right)
    if args.part == 1:
        for node_left, node_right in data[1:]:
            tree_left.insert(node_left)
            tree_right.insert(node_right)
    elif args.part == 2:
        for item in data[1:]:
            if isinstance(item, int):
                node_left = tree_left.get_from_id(root_left, item)
                node_right = tree_right.get_from_id(root_right, item)
                node_left.rank, node_right.rank = node_right.rank, node_left.rank
                node_left.symbol, node_right.symbol = node_right.symbol, node_left.symbol
                continue
            node_left, node_right = item
            tree_left.insert(node_left)
            tree_right.insert(node_right)
    else:
        for item in data[1:]:
            if isinstance(item, int):
                if item == 1:
                    tree_left.root, tree_right.root = tree_right.root, tree_left.root
                else:
                    from_left = tree_left.get_parent(root_left, item)
                    from_right = tree_right.get_parent(root_right, item)
                    if len(from_left) == 1:
                        parent_left, child_type_left = from_left[0]
                        parent_right, child_type_right = from_right[0]
                    elif len(from_left) == 2:  # both nodes in the left tree
                        parent_left, child_type_left = from_left[0]
                        parent_right, child_type_right = from_left[1]
                    else:  # both nodes in the right tree
                        parent_left, child_type_left = from_right[0]
                        parent_right, child_type_right = from_right[1]
                    if child_type_left == "left":
                        if child_type_right == "left":
                            parent_left.child_left, parent_right.child_left = parent_right.child_left, parent_left.child_left
                        else:
                            parent_left.child_left, parent_right.child_right = parent_right.child_right, parent_left.child_left
                    else:
                        if child_type_right == "left":
                            parent_left.child_right, parent_right.child_left = parent_right.child_left, parent_left.child_right
                        else:
                            parent_left.child_right, parent_right.child_right = parent_right.child_right, parent_left.child_right

                continue
            node_left, node_right = item
            tree_left.insert(node_left)
            tree_right.insert(node_right)
    print(tree_left.decrypt_max() + tree_right.decrypt_max())
    print(time() - t)
