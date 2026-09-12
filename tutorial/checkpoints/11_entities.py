"""Checkpoint 11: classes bundle the data and behavior of entities."""


class Tile:
    def __init__(self, kind):
        self.kind = kind


class Item:
    def __init__(self, name):
        self.name = name


class Door:
    def __init__(self, key):
        self.key, self.open = key, False


class Player:
    def __init__(self, name):
        self.name, self.hp, self.inventory = name, 10, []


class Monster:
    def __init__(self, name):
        self.name, self.hp = name, 4


def main():
    player = Player("Explorer")
    player.inventory.append(Item("Gold Key"))
    things = [Tile("room"), Door("gold"), player, Monster("Snake")]
    print("Entities:", ", ".join(type(thing).__name__ for thing in things))
    print(player.name, "has", player.inventory[0].name)


if __name__ == "__main__":
    main()
