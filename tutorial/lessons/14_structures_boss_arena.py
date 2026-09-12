"""Lesson 14 exercise: model a larger arena and its boss state.

The arena is display data.  The Boss object stores state: active, health, and
defeated.  Methods make the allowed state changes easy to read.
"""


# WORKED EXAMPLE:
# boss = Boss()
# boss.summon()
# boss.hit(5)  # 12 becomes 7, never a negative number.


class Boss:
    """A small state machine: inactive, active, then defeated."""

    def __init__(self, hp=12):
        # TODO: Store health and two Boolean state flags.
        self.hp = hp
        self.active = False
        self.defeated = False

    def summon(self):
        """Activate the encounter without changing its health."""
        # TODO: Change the boss from inactive to active.
        self.active = True

    def hit(self, damage):
        """Apply damage only to an active boss and update defeated."""
        # TODO: Use max(0, ...) to protect the non-negative HP invariant.
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
