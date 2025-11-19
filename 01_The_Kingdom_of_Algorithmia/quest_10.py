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

def parse_input(result: dict, raw: str, r: int, nr: int, *, is_part_three: bool = False) -> None:
    if is_part_three:
        temp = ""
        l = len(raw.strip())
        for i in range(l):
            if i not in (1, l - 1) and i % 6 == 1:
                temp += raw[i] + " " + raw[i - 1:i + 1]
            else:
                temp += raw[i]
        raw = temp
    notes = len(raw.strip()) // 9 + 1
    if r in (0, 1, 6, 7):
        for note in range(notes):
            for c in range(1, 5):
                item = result.get((note, nr), {})
                col = item.get(f"c{c}", set())
                col.add((len(col), raw[1 + c + note * 9]))
                item[f"c{c}"] = col
                result[(note, nr)] = item
    else:
        for note in range(notes):
            for c in (0, 1, 6, 7):
                item = result.get((note, nr), {})
                row = item.get(f"r{r - 1}", set())
                row.add((len(row), raw[c + note * 9]))
                item[f"r{r - 1}"] = row
                result[(note, nr)] = item

def runic_word(notes: dict) -> str:
    word = ""
    for r in range(1, 5):
        for c in range(1, 5):
            try:
                if len({x[1] for x in notes[f"r{r}"]}) != 4 or len({ x[1] for x in notes[f"c{c}"]}) != 4:
                    word += "?"
                else:
                    inter = {x[1] for x in notes[f"r{r}"]}.intersection({ x[1] for x in notes[f"c{c}"]})
                    if len(inter) == 1:
                        word += inter.pop()
                    else:
                        word += "?"
            except KeyError:
                word += "?"
    return word

def letter_power(letter: str) -> int:
    return ord(letter.lower()) - 96

def runic_power(rune: str) -> int:
    return sum((i + 1) * letter_power(rune[i]) for i in range(len(rune)))

def try_complete(result: dict, data: dict) -> None:
    move = True
    while move:
        move = False
        for key, val in result.items():
            if "?" not in val:
                continue
            for i, char in enumerate(val):
                missing = ""
                if char == "?":
                    row_idx, col_idx = divmod(i, 4)
                    col_symbols = data[key][f"c{col_idx + 1}"]
                    row_symbols = data[key][f"r{row_idx + 1}"]
                    if len({x[1] for x in col_symbols}) != 4 or len({x[1] for x in row_symbols}) != 4:
                        # several matching symbols, no possible word.
                        continue
                    inter = {x[1] for x in col_symbols}.intersection({x[1] for x in row_symbols})
                    if len(inter) == 1:
                        # nominal case, one common symbol, might be "?" though.
                        missing = inter.pop()
                    elif len(inter) > 1:
                        # several matching symbols, no possible word.
                        continue
                    else:
                        # no matching symbols, might be a "?" in col OR row set.
                        c, r = key
                        if "?" in {x[1] for x in row_symbols}:
                            col = {val[(i + 4 * n) % 16] for n in range(5)}
                            missing_set = {x[1] for x in col_symbols} - col
                            if not missing_set or len(missing_set) > 1:
                                continue
                            missing = missing_set.pop()
                            for x in row_symbols:
                                if x[1] == "?":
                                    if x[0] in (0, 1) and data.get((c - 1, r)) and "?" in {y[1] for y in data[(c - 1, r)][f"r{row_idx + 1}"]}:
                                        data[(c - 1, r)][f"r{row_idx + 1}"].add((x[0] + 2, missing))
                                        data[(c - 1, r)][f"r{row_idx + 1}"].remove((x[0] + 2, "?"))
                                    if x[0] in (2, 3) and data.get((c + 1, r)) and "?" in {y[1] for y in data[(c + 1, r)][f"r{row_idx + 1}"]}:
                                        data[(c + 1, r)][f"r{row_idx + 1}"].add((x[0] - 2, missing))
                                        data[(c + 1, r)][f"r{row_idx + 1}"].remove((x[0] - 2, "?"))
                        else:
                            row = set(val[row_idx * 4: (row_idx + 1) * 4])
                            missing_set = {x[1] for x in row_symbols} - row
                            if not missing_set or len(missing_set) > 1:
                                continue
                            missing = missing_set.pop()
                            for x in col_symbols:
                                if x[1] == "?":
                                    if x[0] in (0, 1) and data.get((c, r - 1)) and "?" in {y[1] for y in data[(c, r - 1)][f"c{col_idx + 1}"]}:
                                        data[(c, r - 1)][f"c{col_idx + 1}"].add((x[0] + 2, missing))
                                        data[(c, r - 1)][f"c{col_idx + 1}"].remove((x[0] + 2, "?"))
                                    if x[0] in (2, 3) and data.get((c, r + 1)) and "?" in {y[1] for y in data[(c, r + 1)][f"c{col_idx + 1}"]}:
                                        data[(c, r + 1)][f"c{col_idx + 1}"].add((x[0] - 2, missing))
                                        data[(c, r + 1)][f"c{col_idx + 1}"].remove((x[0] - 2, "?"))
                    if missing and missing != "?":
                        val = val[:i] + missing + val[i + 1:]
                        move = True
            if move:
                result[key] = val

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        i = 0
        nr = 0
        while line := file.readline():
            if line.strip() == "":
                nr += 1
                i = -1
            else:
                parse_input(data, line, i, nr, is_part_three=args.part == 3)
            i += 1
    if args.part == 1:
        print(runic_word(data[(0, 0)]))
    elif args.part == 2:
        print(sum(runic_power(runic_word(candidate)) for candidate in data.values()))
    else:
        runes = {}
        for key, val in data.items():
            runes[key] = runic_word(val)
        try_complete(runes, data)
        print(sum(runic_power(rune) for rune in runes.values() if "?" not in rune))
    print(time() - t)
