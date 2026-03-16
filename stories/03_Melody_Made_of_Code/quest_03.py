from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path
from time import time

from utils.parsers import parse_args


@dataclass
class Node:
    id: int
    plug: str
    left_socket: str
    right_socket: str
    data: str = ""
    parent: Node | None = None
    parent_side: str = ""
    left: Node | None = None
    right: Node | None = None

    def __repr__(self) -> str:
        left = self.left.id if self.left else ""
        right = self.right.id if self.right else ""
        return f"{self.id}: plug={self.plug}, left_scoket={self.left_socket}, right_socket={self.right_socket}, left={left}, right={right}"


class Tree:
    def __init__(self, *, with_weak: bool = False, can_break: bool = False) -> None:
        self.root: Node | None = None
        self.with_weak = with_weak
        self.can_break = with_weak and can_break
    
    @property
    def check_sum(self) -> int:
        ids = self.__read(self.root)
        check = 0
        for i, id in enumerate(ids, 1):
            check += i * id
        return check

    def add(self, node: Node) -> None:
        if not self.root:
            self.root = node
        else:
            parent, side = self.__find_socket(node.plug)
            detached = self.__attach_node(parent, node, side)
            self.__handle_detached(detached, parent, side)

    def __handle_detached(self, node: Node | None, parent: Node, side: str) -> None:
        if not node:
            return
        node.parent = None
        node.parent_side = ""
        if side == "L":
            if self.__has_link(parent.right_socket, node.plug, parent.right):
                detached = self.__attach_node(parent, node, "R")
                self.__handle_detached(detached, parent, "R")
                return
            if parent.right:
                new_parent, new_side = self.__find_socket(node.plug, parent.right)
                if new_parent:
                    detached = self.__attach_node(new_parent, node, new_side)
                    self.__handle_detached(detached, new_parent, new_side)
                    return
        # Detached from right side, or left but no match on right side
        if not parent.parent:  # parent is root
            print("parent is root")
            if parent.left:
                new_parent, new_side = self.__find_socket(node.plug, parent.left)
                if new_parent:
                    detached = self.__attach_node(new_parent, node, new_side)
                    self.__handle_detached(detached, new_parent, new_side)
                    return
                raise ValueError("Can't re-attach node")
            if self.__has_link(parent.left_socket, node.plug, parent.left):
                detached = self.__attach_node(parent, node, "L")
                self.__handle_detached(detached, node, "L")
                return
            raise ValueError("Definetely can't re-attach node")
        self.__handle_detached(node, parent.parent, parent.parent_side)

    def __read(self, start: Node) -> list[int]:
        if not start:
            return []
        if not start.left and not start.right:
            return [start.id]
        return self.__read(start.left) + [start.id] + self.__read(start.right)

    def __find_socket(self, plug: str, start: Node | None = None) -> tuple[Node | None, str]:
        if not start:
            start = self.root
        if self.__has_link(start.left_socket, plug, start.left):
            return start, "L"
        if start.left:
            node, side = self.__find_socket(plug, start.left)
            if node:
                return node, side
        if self.__has_link(start.right_socket, plug, start.right):
            return start, "R"
        if start.right:
            return self.__find_socket(plug, start.right)
        return None, ""

    def __has_link(self, socket: str, plug: str, node: Node | None) -> bool:
        if node:
            if self.can_break:
                return socket == plug and node.plug != plug
            return False
        if self.with_weak:
            item1_split = socket.split()
            item2_split = plug.split()
            return item1_split[0] == item2_split[0] or item1_split[1] == item2_split[1]
        return socket == plug

    @staticmethod
    def __attach_node(parent: Node | None, node: Node, side: str) -> Node | None:
        if not parent:
            raise ValueError("Can't find a socket that matches")
        if side == "L":
            detached = parent.left
            parent.left = node
        elif side == "R":
            detached = parent.right
            parent.right = node
        else:
            raise ValueError("This node doesn't seem to be a good fit to add a child")
        node.parent = parent
        node.parent_side = side
        return detached


def parse_input(line: str) -> Node:
    pattern = r"id=(\d+), plug=([\w\s]+), leftSocket=([\w\s]+), rightSocket=([\w\s]+)"
    infos = re.findall(pattern, line)[0]
    return Node(
        id=int(infos[0]),
        plug=infos[1],
        left_socket=infos[2],
        right_socket=infos[3]
    )


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    tree = Tree(with_weak=args.part != 1, can_break=args.part == 3)
    for node in data:
        tree.add(node)
    print(tree.check_sum)
    print(time() - t)
