from pathlib import Path
from time import time

from utils.parsers import parse_args

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    if args.part == 1:
        print(data)
    elif args.part == 2:
        raise NotImplementedError
    else:
        raise NotImplementedError
    print(time() - t)
