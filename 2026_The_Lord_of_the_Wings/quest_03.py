import math
from heapq import heappop, heappush
from pathlib import Path
from time import time

from utils.parsers import parse_args

def parse_input(raw: str, offset: int) -> tuple[str]:
    splitted = raw.split(" ")
    return (splitted[0][offset:], splitted[1])


def vote_to_decimal(vote: tuple[str],* , clear_invalid: bool) -> int:
    result = get_result(vote)
    if clear_invalid and not is_valid(vote, result):
        return 0
    return result


def get_result(vote: tuple[str]) -> int:
    standard, value = vote
    if len(standard) < len(value):
        standard *= math.ceil(len(value) / len(standard))
    standard = standard[-len(value):]
    m = len(standard)
    return sum(
        int(x) ** (m - 1 - i) * int(value[i])
        for i, x in enumerate(standard)
    )


def is_valid(vote: tuple[str], decimal: int) -> bool:
    standard, value = vote
    queue = []
    for i in range(10):
        if decimal - i >= 0:
            heappush(queue, (decimal - i, i))
    while queue:
        delta, other_value = heappop(queue)
        if not delta:
            return other_value >= int(value)
        d = 1 if delta < 10 else 10
        if other_value + d > int(value):
            pass
        result = get_result((standard, str(other_value + d)))
        if result > decimal:
            pass
        heappush(queue, (decimal - result, other_value + d))
    return True


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = [parse_input(line, 4 if args.part != 3 else 5) for line in file.read().strip().split("\n")]
    print(sum(vote_to_decimal(vote, clear_invalid=args.part == 3) for vote in data))
    print(time() - t)
