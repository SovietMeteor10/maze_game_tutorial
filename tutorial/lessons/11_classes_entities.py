"""Lesson 11 exercise: use classes and objects to package entity state."""


class Tile:
    def __init__(self, kind):
        self.kind = kind  # An attribute belongs to this instance.


class Item:
    def __init__(self, name):
        self.name = name


class Door:
    def __init__(self, key):
        self.key = key
        self.open = False

    def describe(self):
        """A method is a function that belongs to a class."""
        return "{} door ({})".format(self.key, "open" if self.open else "closed")


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 10
        self.inventory = []


class Monster:
    def __init__(self, name):
        self.name = name
        self.hp = 4


def main():
    # WORKED EXAMPLE: Player contains an Item object: this is composition.
    # Player is a class recipe; player is one object, or instance, made from it.
    # Each instance gets its own attributes instead of sharing one global state.
    player = Player("Explorer")
    player.inventory.append(Item("Gold Key"))
    things = [Tile("room"), Door("gold"), player, Monster("Snake")]
    print("Entities:", ", ".join(type(thing).__name__ for thing in things))
    print(player.name, "has", player.inventory[0].name)
    print(things[1].describe())
    # TODO: Make another Player and prove its inventory is separate.


if __name__ == "__main__":
    main()
