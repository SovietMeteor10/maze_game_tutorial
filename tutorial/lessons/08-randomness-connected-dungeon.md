# 08: Randomness, Seeds, And Connected Growth

**Coding exercise:** `08_randomness_connected_dungeon.py` | **Model answer:** `../solutions/08_randomness_connected_dungeon.py`

## What You Will Build

You will build a small generated dungeon from connected cells. The checkpoint
is `tutorial/checkpoints/08_connected_dungeon.py`. It uses seed `7`, starts at
the center of a seven-by-seven grid, grows until it has twelve cells, and
prints `.` for a cell and `#` for empty space.

This is deliberately smaller than a finished maze generator. It focuses on a
valuable guarantee: each new cell is chosen next to a cell that already
exists. That means the result grows as one connected group instead of creating
unrelated islands.

## Learning Goals

- Import and use Python's `random` module.
- Create a separate seeded random generator.
- Understand reproducible randomness.
- Store unique coordinate pairs in a set.
- Choose a neighbor using four direction options.
- Read a bounds check safely.
- Render generated cells with nested loops.

## New Words With Plain Definitions

- A **module** is a Python file or library of related tools.
- An **API** is the collection of names a module offers you to call.
- **Randomness** means choices are not predictable in advance.
- A **seed** is the starting value for a repeatable random sequence.
- **Reproducible** means the same inputs can produce the same result again.
- A **coordinate pair** is two values such as `(x, y)`.
- A **tuple** is an ordered, usually fixed group of values.
- A **set** stores unique values and ignores duplicate additions.
- A **neighbor** is a cell directly north, south, east, or west.
- A **bound** is a limit a coordinate must stay within.
- A **graph** is a group of points and relationships between them.

## Why This Matters

Hand-authored maps are precise, but generated maps provide variety. The tradeoff
is that changing output is harder to debug. A seed gives us both: the player
can receive a different map by changing the seed, and a bug report can include
the seed so the exact map can be recreated.

Connectivity matters because a group of random cells can contain unreachable
islands. This checkpoint avoids that problem with a simple growth rule: choose
an existing cell, choose one of its four adjacent candidates, and add the
candidate if it is inside the grid. The algorithm is not trying to create
beautiful rooms, loops, or a difficult maze. It teaches the constraint before
those features are added.

## Tiny Examples Explained Line By Line

```python
import random
coin = random.Random(4)
print(coin.choice(["heads", "tails"]))
```

1. `import random` loads Python's standard random module.
2. `random.Random(4)` creates a separate generator with seed `4`.
3. `coin` is a useful name for that generator.
4. `choice` selects one item from the list.
5. Running this same code again gives the same choice because the seed and
   choices are the same.

Here is the set behavior used for cells:

```python
cells = {(1, 1)}
cells.add((1, 1))
print(len(cells))
```

1. The set begins with one tuple representing `x = 1`, `y = 1`.
2. Adding the same tuple again changes nothing.
3. `len(cells)` is still `1`.

That duplicate behavior is exactly what growth needs. A random choice may
propose a cell already present. The set quietly keeps one copy, and the loop
tries again.

## Guided Build Tied To The Actual Checkpoint

The checkpoint begins with:

```python
def make_dungeon(seed, size=7):
    randomizer = random.Random(seed)
    cells = {(size // 2, size // 2)}
```

The function accepts a seed and a grid size. `size // 2` uses integer division
to find the center index. For size seven, both coordinates are three, so the
starting cell is `(3, 3)`.

The growth loop is:

```python
while len(cells) < 12:
    x, y = randomizer.choice(tuple(cells))
    nx, ny = randomizer.choice([
        (x + 1, y), (x - 1, y),
        (x, y + 1), (x, y - 1),
    ])
    if 0 <= nx < size and 0 <= ny < size:
        cells.add((nx, ny))
```

1. Continue while fewer than twelve unique cells exist.
2. Convert the set to a tuple because `choice` needs a sequence, then choose
   an existing cell.
3. Unpack its coordinates into `x` and `y`.
4. Choose one candidate neighbor. Increasing `x` moves east; decreasing `x`
   moves west; increasing `y` moves south; decreasing `y` moves north.
5. The condition checks both coordinates. Valid values are zero through
   `size - 1`.
6. Only an in-bounds candidate is added.

Because every accepted candidate is adjacent to an old cell, the accepted
cells remain connected. Because `cells` is a set, duplicates do not inflate
the count.

The `main` function calls `make_dungeon(7)`. Its nested loops visit each `y`
from zero through six and each `x` from zero through six. The expression
`"." if (x, y) in cells else "#"` chooses the visible character. The final
line reports the seed and `len(cells)`, which should be twelve.

## Complete Checkpoint Walkthrough

Run the checkpoint exactly as written. With Python's seeded generator, the
output is:

```text
#######
#######
#.....#
......#
##.####
#######
#######
Seed 7 created 12 connected cells.
```

The exact seven rows are important when checking your local result. A dot is a
member of the set, and a hash is not. The middle area contains the starting
cell and its grown neighbors. You do not need to identify the order in which
the cells were added; the set stores the final result, not its history.

Try changing only the seed to `1`. The picture should change, but the final
count should still be twelve. Try changing the target from twelve to twenty in
your own copy. The map can grow until the grid has no more unique cells, but
the loop would need a clear stopping rule if you request more than the grid
can hold. This is a useful example of an assumption the small checkpoint does
not validate.

## Common Mistakes

- Removing the seed makes output harder to reproduce.
- Using a list permits duplicate coordinates and makes counting unreliable.
- Calling `random.choice(cells)` fails because a set is not a sequence.
- Forgetting a bounds check can create negative or oversized coordinates.
- Choosing from all grid cells instead of neighbors can break connectivity.
- Changing the target without considering the seven-by-seven capacity can make
  the loop impossible to finish.
- Mixing `(x, y)` and `(y, x)` makes the picture appear transposed.

## Fun Side Quests

1. Try seeds `1`, `2`, and `7`. Which result looks most maze-like?
2. Print the center marker as `S` instead of `.`.
3. Add diagonal candidates and explain how that changes the meaning of
   connected.
4. Count how many cells have a neighboring cell on each of their four sides.
5. Add a target parameter and safely reject targets larger than `size * size`.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/08_connected_dungeon.py
```

Expected result: seven rows of `.` and `#`, followed by
`Seed 7 created 12 connected cells.`. The output should match the complete
picture in the walkthrough when run with the original code.

## Learner Questions

- Why must each new cell be chosen next to an existing cell?
- What information should a bug report include when a generated map is wrong?
- Why does a set make duplicate proposals harmless?
- What would happen if diagonal neighbors were allowed?
- Would a dungeon made from one long line be connected but still boring?

## What To Remember

Seeded randomness gives variety that can be replayed. A set is a good model for
unique cells, and growing from an existing cell gives a simple connectivity
guarantee. Bounds checks keep generated coordinates inside the map.

## Exact Reference Game Comparison

The checkpoint's `make_dungeon` is the small graph idea that leads toward
`game/world.py:generate_tiles`. The reference generator builds a serpentine
path, adds occasional graph edges, stores direction sets, and calls
`game/world.py:validate_connections`. Its `WorldMap._random_for` uses a seed
plus a position so discovered tiles can be generated consistently. Rendering
is more detailed in `game/world.py:render_viewport`, but the core lessons are
the same: coordinates are data, random choices need constraints, and connected
worlds need an explicit construction rule.
