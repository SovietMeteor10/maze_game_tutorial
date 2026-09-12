"""Checkpoint 09: floor items can be collected into an inventory list."""

from dataclasses import dataclass


@dataclass
class Item:
    name: str
    symbol: str


def main():
    floor = {(2, 1): Item("Gold Key", "k"), (3, 1): Item("Potion", "!")}
    inventory = []
    position = (1, 1)
    for position in [(2, 1), (3, 1)]:
        item = floor.pop(position)
        inventory.append(item)
        print("Picked up", item.name)
    print("Inventory:", [item.name for item in inventory])


if __name__ == "__main__":
    main()
