from pathlib import Path
from time import time

from utils.parsers import parse_args


def parse_input(raw: list[str]) -> None:
    for line in raw:
        ingredients = line[5:].split(",")
        data[line[:4]] = set(ingredients)


def get_null_ingredients(item: str = "NULL") -> None:
    global null_ingredients

    if item not in data:
        return set()

    for ingredient in data[item]:
        if ingredient not in null_ingredients:
            null_ingredients.add(ingredient)
            null_ingredients |= get_null_ingredients(ingredient)
    return set()


def get_null_products(init_null: str = "NULL") -> set:
    products = set()
    to_add = {init_null}
    while to_add:
        new_to_add = set()
        while to_add:
            item = to_add.pop()
            products.add(item)
            for product, ingredients in data.items():
                if item in ingredients and product not in products:
                    new_to_add.add(product)
        to_add = new_to_add
    return products


if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        null_ingredients = {"NULL"}
        get_null_ingredients()
        print(len(null_ingredients) - 1)
    elif args.part == 2:
        null_products = get_null_products()
        print(len(null_products) - 1)
    else:
        nullv1_products = get_null_products("NULLv1")
        nullv2_products = get_null_products("NULLv2")
        nullv3_products = get_null_products("NULLv3")
        print(
            len(
                nullv1_products.intersection(nullv2_products)
                | nullv1_products.intersection(nullv3_products)
                | nullv2_products.intersection(nullv3_products)
            )
        )
    print(time() - t)
