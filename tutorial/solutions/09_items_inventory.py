"""Lesson 09 model answer: items transfer from the floor to an inventory."""

from dataclasses import dataclass


@dataclass
class Item:
    """A named item with a short symbol for later map rendering."""

    name: str
    symbol: str


def pickup_item(floor, inventory, position):
    """Transfer an item and return it, or return None for an empty position."""
    if position not in floor:
        return None
    item = floor.pop(position)
    inventory.append(item)
    return item


def main():
    # MODEL ANSWER
    # floor and inventory are two parts of game state.  Pickup mutates both.
    floor = {(2, 1): Item("Gold Key", "k"), (3, 1): Item("Potion", "!")}
    inventory = []
    for position in [(2, 1), (3, 1)]:
        item = pickup_item(floor, inventory, position)
        if item is not None:
            print("Picked up", item.name)
    print("Inventory:", [item.name for item in inventory])
    print("Floor items left:", len(floor))


if __name__ == "__main__":
    main()
