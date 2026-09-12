"""Lesson 09 exercise: move items from a floor dictionary into an inventory."""

from dataclasses import dataclass


@dataclass
class Item:
    """Small bundle of facts about something the player can carry."""

    name: str
    symbol: str


def pickup_item(floor, inventory, position):
    """Move one item from floor state to inventory state."""
    # TODO: Check whether position is in floor before calling pop.
    # TODO: Return a useful result when there is no item at this position.
    item = floor.pop(position)
    inventory.append(item)  # append mutates the existing list.
    return item


def main():
    # WORKED EXAMPLE: the item is in exactly one place after pickup.
    floor = {(2, 1): Item("Gold Key", "k"), (3, 1): Item("Potion", "!")}
    inventory = []
    for position in [(2, 1), (3, 1)]:
        item = pickup_item(floor, inventory, position)
        print("Picked up", item.name)

    print("Inventory:", [item.name for item in inventory])
    print("Floor items left:", len(floor))
    # TODO: Add a third item and collect it in the scripted example.


if __name__ == "__main__":
    main()
