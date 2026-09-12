"""Lesson 11 model answer: classes package data for simple game entities."""


class Tile:
    def __init__(self, kind):
        self.kind = kind


class Item:
    def __init__(self, name):
        self.name = name


class Door:
    def __init__(self, key):
        self.key = key
        self.open = False

    def describe(self):
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
    # MODEL ANSWER
    # A class is a recipe.  Each call creates an object, also called an instance.
    # Attributes hold state; methods hold behavior.  Objects inside objects show
    # composition: the Player contains an Item in its inventory.
    player = Player("Explorer")
    player.inventory.append(Item("Gold Key"))
    second_player = Player("Guide")
    things = [Tile("room"), Door("gold"), player, Monster("Snake")]
    print("Entities:", ", ".join(type(thing).__name__ for thing in things))
    print(player.name, "has", player.inventory[0].name)
    print(things[1].describe())
    print("Separate inventories:", player.inventory != second_player.inventory)


if __name__ == "__main__":
    main()
