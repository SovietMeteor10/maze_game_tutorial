# 14: A Boss Arena

**Coding exercise:** `14_structures_boss_arena.py` | **Model answer:** `../solutions/14_structures_boss_arena.py`

## What You Will Build

You will build a small arena and a boss object with three important facts:
whether it is active, how much health it has, and whether it is defeated. The
checkpoint summons the boss and applies three attacks. The arena is larger than
an ordinary sample room, but the real lesson is the encounter state behind the
picture. Run `tutorial/checkpoints/14_boss_arena.py` to see it.

## Learning Goals

- Explain why a larger structure can still be represented by ordinary data.
- Create a class with an initializer and methods.
- Change state through `summon()` and `hit()`.
- Prevent damage before activation.
- Clamp health at zero with `max()`.
- Store a clear `defeated` completion flag.
- Recognize a simple state machine: inactive, active, defeated.

## New Words

- **Arena:** a special area where an encounter takes place.
- **State:** information describing what is true right now.
- **State machine:** a small set of allowed states and transitions between them.
- **Activation:** changing an encounter from waiting to running.
- **Health points, or HP:** a number representing how much damage an entity
  can take.
- **Flag:** a Boolean value used to record a condition, such as `defeated`.
- **Invariant:** a rule that should remain true, such as HP never being below
  zero.

## Why This Matters

A boss is not just a letter printed inside a room. The game must know whether
the boss can take damage, whether the player has finished the encounter, and
what reward or exit should become available. Keeping these facts in state lets
other code make decisions without guessing from the screen.

The separate `defeated` flag may seem redundant because zero HP suggests
defeat. It is useful because completion is a game event. Later code can unlock
an exit once, display a victory message, or prevent the boss from respawning.
This improves interpretability: `boss.defeated` says exactly what it means.

## Tiny Example, Line by Line

```python
class Boss:
    def __init__(self):
        self.hp, self.active, self.defeated = 12, False, False
```

`class Boss` defines a new kind of object. `__init__` runs when a Boss is made.
The three assignments give it 12 HP, mark it inactive, and mark it not
defeated. The comma-separated assignment sets three attributes at once; write
them on separate lines if that is clearer.

```python
def hit(self, damage):
    if self.active:
        self.hp = max(0, self.hp - damage)
        self.defeated = self.hp == 0
```

The method receives the boss as `self` and a damage number. The `if` blocks
damage while the encounter is inactive. `self.hp - damage` calculates the new
value. `max(0, ...)` enforces the invariant that HP cannot go negative. The
last line turns the comparison into `True` exactly when HP reaches zero.

## Guided Build: Tie It To The Checkpoint

Open `tutorial/checkpoints/14_boss_arena.py`. The `Boss` class is intentionally
small. `summon()` only sets `active` to `True`; it does not change HP. `hit()`
does the rule work. The `main()` function owns the demonstration: it creates
an arena list, creates a boss, summons it, applies damage values `(5, 5, 5)`,
and prints the result.

Build in that order. First make the class and confirm `Boss().active` is
`False`. Add `summon()` and confirm it becomes `True`. Then add `hit()` and
test one hit: 12 HP should become 7. Test an over-sized hit too; HP should be
0, not a negative number. Finally set `defeated` from the HP comparison.

The arena itself is a list of strings:

```python
arena = ["#########", "#.......#", "#...B...#", "#.......#", "#########"]
```

Each string is one row. `#` is a wall, `.` is floor, and `B` is the boss
marker. This is a visual representation, not the full boss state.

## Complete Checkpoint Walkthrough

`boss = Boss()` starts with `(12, False, False)`. `boss.summon()` changes only
the active flag. The first `boss.hit(5)` changes HP from 12 to 7 and leaves
defeated false. The second changes 7 to 2. The third calculates `2 - 5`, then
`max(0, -3)` produces 0. The comparison `0 == 0` sets defeated to true.

The final loop prints the five arena rows. `"\n".join(arena)` places a newline
between rows without adding extra formatting. The status line prints both
flags, producing:

```text
#########
#.......#
#...B...#
#.......#
#########
Boss active: True defeated: True
```

The checkpoint does not implement movement or real-time combat. That is a
feature, not a missing piece: it makes the state transition easy to inspect.

## Common Mistakes

- Forgetting `self` means the method cannot read or change this boss.
- Subtracting damage before checking `active` lets an unsummoned boss die.
- Using `self.hp = self.hp - damage` without `max()` creates negative HP.
- Setting `defeated = True` during `summon()` skips the encounter.
- Inferring completion only from a printed `B`. The symbol is not state.
- Mutating the arena string to represent HP. Keep the visual layer and rules
  separate.

## Side Quests

1. Add `heal(amount)` that increases HP only while active and never exceeds a
   chosen maximum such as 12.
2. Add a `rewarded` flag. Set it only once after defeat and print a treasure
   message when the flag changes.
3. Add a second attack value and print a line after each hit showing current
   HP. Try damage larger than the remaining HP.
4. Add an `entrance_closed` flag that becomes true when summoned and false when
   defeated. Ask what rule would open it safely.

## Run Command And Expected Result

From the project root, run:

```text
python3 tutorial/checkpoints/14_boss_arena.py
```

The expected result is the arena followed by:

```text
Boss active: True defeated: True
```

## Learner Questions

- What are the allowed encounter states before and after `summon()`?
- Why is `defeated` useful even though HP is also stored?
- Which line enforces the non-negative HP invariant?
- What should happen if `hit()` is called before `summon()`?
- Which part of this checkpoint would belong to rendering in a larger game?

## Exact Reference Game Comparison

The reference keeps progression fields in `game/game_state.py`, including
`boss_active`, `boss_defeated`, `boss_split`, `boss_tiles`, and
`boss_room_size`. `game/game.py` summons a special 5 x 5 region, teleports the
player, spawns the giant snake and minions, and later handles split behavior.
The tutorial checkpoint is intentionally a compact model: it has a 5-row
display and one boss with 12 HP, while the reference uses a generated arena,
100 HP for the giant boss, timed effects, minions, and a victory loop.

## What To Remember

Represent an encounter with explicit state. Use methods for small rule changes,
protect invariants such as non-negative HP, and keep a completion flag when an
event matters. A large game feature can begin as a tiny, testable state machine.
