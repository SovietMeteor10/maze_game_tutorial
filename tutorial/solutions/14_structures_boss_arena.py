"""MODEL ANSWER: Lesson 14 structures and a boss arena.

The arena is composition of rows, while Boss keeps encounter state.  Keeping
these responsibilities separate makes the rules interpretable and testable.
"""


class Boss:
    """A boss with explicit activation, health, and completion state."""

    def __init__(self, hp=12):
        if not isinstance(hp, int) or isinstance(hp, bool) or hp < 0:
            raise ValueError("hp must be a non-negative integer")
        self.hp = hp
        self.active = False
        self.defeated = False

    def summon(self):
        self.active = True

    def hit(self, damage):
        if not isinstance(damage, int) or isinstance(damage, bool) or damage < 0:
            raise ValueError("damage must be a non-negative integer")
        if self.active and not self.defeated:
            self.hp = max(0, self.hp - damage)
            self.defeated = self.hp == 0


def main():
    arena = ["#########", "#.......#", "#...B...#", "#.......#", "#########"]
    boss = Boss()
    boss.summon()
    for damage in (5, 5, 5):
        boss.hit(damage)
    print("\n".join(arena))
    print("Boss active:", boss.active, "defeated:", boss.defeated)


if __name__ == "__main__":
    main()
