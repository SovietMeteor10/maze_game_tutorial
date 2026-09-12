"""Checkpoint 12: a player action is followed by a surviving enemy action."""


class Fighter:
    def __init__(self, name, hp, damage):
        self.name, self.hp, self.damage = name, hp, damage


def attack(attacker, target):
    target.hp = max(0, target.hp - attacker.damage)
    return "{} hits {} ({} hp left)".format(attacker.name, target.name, target.hp)


def main():
    player, snake = Fighter("Player", 10, 3), Fighter("Snake", 5, 1)
    print(attack(player, snake))
    if snake.hp:
        print(attack(snake, player))
    print("Defeated:", snake.hp == 0)


if __name__ == "__main__":
    main()
