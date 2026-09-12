"""Lesson 12 model answer: a surviving enemy receives the next turn."""


class Fighter:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage


def attack(attacker, target):
    """Mutate the target's health and report the state transition."""
    target.hp = max(0, target.hp - attacker.damage)
    return "{} hits {} ({} hp left)".format(attacker.name, target.name, target.hp)


def main():
    # MODEL ANSWER
    # Each Fighter instance owns independent attributes.  The attack rule reads
    # the attacker and mutates the target.  Turn order allows only a survivor to act.
    player = Fighter("Player", 10, 3)
    snake = Fighter("Snake", 5, 1)
    print(attack(player, snake))
    if snake.hp > 0:
        print(attack(snake, player))
    print("Defeated:", snake.hp == 0)


if __name__ == "__main__":
    main()
