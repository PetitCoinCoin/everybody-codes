from typing import Iterable

def get_next(position: tuple[int], *, with_diagonals: bool = False) -> Iterable[tuple[int]]:
    r, c = position
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        yield (r + dr, c + dc)
    if with_diagonals:
        for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            yield (r + dr, c + dc)
