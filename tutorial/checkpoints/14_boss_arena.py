"""Checkpoint 14: a larger arena has its own boss encounter state."""


class Boss:
    def __init__(self):
        self.hp, self.active, self.defeated = 12, False, False

    def summon(self):
        self.active = True

    def hit(self, damage):
        if self.active:
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
