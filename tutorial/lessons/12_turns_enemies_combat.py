"""Lesson 12 exercise: apply simple turn-order and combat rules."""


class Fighter:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage


def attack(attacker, target):
    """Damage the target, clamp hp at zero, and return a result message."""
    # TODO: Make sure damage changes target.hp, not attacker.hp.
    target.hp = max(0, target.hp - attacker.damage)
    return "{} hits {} ({} hp left)".format(attacker.name, target.name, target.hp)


def main():
    # WORKED EXAMPLE: the player acts first; a defeated enemy loses its turn.
    player = Fighter("Player", 10, 3)
    snake = Fighter("Snake", 5, 1)
    print(attack(player, snake))
    if snake.hp > 0:  # This condition enforces the turn rule.
        print(attack(snake, player))
    print("Defeated:", snake.hp == 0)
    # TODO: Change player damage to 5 and predict which turn disappears.


if __name__ == "__main__":
    main()
