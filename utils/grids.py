from typing import Iterable

def get_next(position: tuple[int], *, with_diagonals: bool = False) -> Iterable[tuple[int]]:
    r, c = position
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        yield (r + dr, c + dc)
    if with_diagonals:
        for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            yield (r + dr, c + dc)

def pprint(grid: dict, max_r: int, max_c: int, blank: str = " ") -> None:
    """Useful for debug or easter eggs"""
    print("\n".join(
        "".join(str(grid.get((r, c), blank)) for c in range(max_c + 1))
        for r in range(max_r + 1)
    ))
