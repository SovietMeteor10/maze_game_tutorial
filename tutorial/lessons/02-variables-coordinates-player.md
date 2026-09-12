# 02: Variables, Coordinates, And A Player

**Coding exercise:** `02_variables_coordinates_player.py` | **Model answer:** `../solutions/02_variables_coordinates_player.py`

## What You Will Build

You will run `tutorial/checkpoints/02_player_coordinates.py`, which places a
player marker, `@`, inside a small room. The room is still fixed and there is
still no keyboard input. The new part is that the marker comes from two numbers:
an x coordinate and a y coordinate. Change those numbers and the marker moves
to a different cell when you run the file again.

This is the first lesson where the screen has a piece of changing state. The
room is the template. The player position is the state. The `@` character is a
visual choice made while drawing that state.

## Learning Goals

- Store whole numbers in variables.
- Understand x as horizontal and y as vertical.
- Use Python's zero-based indexes.
- Read a grid with `picture[y][x]`.
- Copy display data before changing it.
- Keep a player's position separate from the player's printed symbol.
- Recognize tuple unpacking in `x, y = 4, 2`.

## New Words

- An **integer** is a whole number, such as `4` or `-1`.
- A **coordinate** is a number or pair of numbers that locates something.
- An **index** is a position in an ordered value. Python starts indexes at `0`.
- **Indexing** means using square brackets to fetch one item.
- A **tuple** is an ordered group of values, commonly written `(x, y)`.
- **Mutation** means changing existing data in place.
- **State** means what is true right now, such as the player's position.
- A **copy** is separate data with the same starting contents.
- A **grid** is data arranged in rows and columns.
- **Rendering** means turning state into something visible on screen.

## Why This Matters

The game must know where the player is even when it is not currently printing
the player. Keeping `(x, y)` as data makes movement, collision, saving, and
testing possible. If the program treated the `@` character as the location,
every other system would have to search through printed text. That becomes
fragile as soon as there are items, monsters, or several rooms.

Coordinate order is another important habit. A screen is naturally a list of
rows. Therefore y selects a row first, and x selects a character in that row.
Writing `picture[x][y]` is a common beginner error because the words "x first"
feel natural. The code follows the data shape: `picture[y][x]`.

## Tiny Examples Explained Line By Line

```python
x = 2
y = 1
point = (x, y)
print(point[0], point[1])
```

Line 1 stores a horizontal position. Line 2 stores a vertical position. Line 3
groups both values into a tuple. Line 4 reads the first and second tuple items.
The first item has index `0`, so `point[0]` is x and `point[1]` is y.

```python
row = list("...")
row[1] = "@"
print("".join(row))
```

`"..."` is a string, but strings cannot have one character replaced. `list`
turns it into `['.', '.', '.']`, which can be mutated. Index `1` is the middle
character, so assignment changes it to `@`. `join` turns the character list
back into printable text.

## Guided Build Tied To The Actual Checkpoint

Open `tutorial/checkpoints/02_player_coordinates.py`. `ROOM` is a list of four
strings. The `draw(x, y)` function begins with a list comprehension:
`[list(row) for row in ROOM]`. Read it as: make a character list for every row
in `ROOM`. This creates a new two-dimensional picture, so drawing does not
rewrite the template.

The next line, `picture[y][x] = "@"`, performs two selections. First, y picks
the row. Then x picks a character within that row. It replaces that character
in the copy. The return expression reverses the conversion: inner `join`
combines characters into each row, and outer `join` puts newline characters
between rows.

In `main`, `x, y = 4, 2` is tuple unpacking. Python treats the right side as two
values and stores them in the two names on the left. `print(draw(x, y))` passes
the current coordinates into the drawing function. The following format call
prints a sentence so you can compare the numbers with the visible marker.

## Complete Checkpoint Walkthrough

1. Start from the project root.
2. Run the checkpoint command below.
3. Python creates no player object yet; it stores two integers.
4. `draw(4, 2)` copies all four room rows into mutable character lists.
5. Row index 2 is selected, then character index 4 is replaced with `@`.
6. The rows are joined and printed.
7. The coordinate sentence confirms `x=4, y=2`.

Change x to `1`. The marker moves left. Change y to `1`. It moves upward.
Remember that index `0` is the first row or character. If you use an index past
the available data, Python raises an indexing error. That is not random bad
luck; it means the caller supplied a coordinate outside this tiny room. Later
lessons will add rules to prevent such a move.

## Common Mistakes

- `picture[x][y]` swaps the row and column.
- Index `0` is the first item, not the second item.
- Editing `ROOM` directly makes future drawings inherit the `@` marker.
- Treating `@` as the player's actual state mixes data with display.
- A string row must be converted to a list before one character can change.
- Negative indexes have special Python meaning and are not normal map bounds.
- Choosing coordinates at the wall can hide the marker in the border.

## Fun Side Quests

- Replace `@` with `P`, then explain why the position data does not change.
- Draw a second marker at another coordinate and decide how two positions would
  be represented.
- Print the room at three different coordinates without changing `ROOM`.
- Make a paper grid and label its top-left cell `(0, 0)`.
- Add a `symbol` parameter to `draw` as an experiment, then call `draw(4, 2,
  "M")` only if you also update the function definition.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/02_player_coordinates.py
```

Expected result: a four-row room with `@` at x=4, y=2, followed by
`The player is at x=4, y=2.`

## Learner Questions

- Why does y choose a row before x chooses a column?
- Why does `draw` copy the room before mutation?
- What is the difference between `(4, 2)` and the character `@`?
- What should happen when a coordinate is outside the room?
- If y increased upward instead of downward, which drawing rules would change?

## What To Remember

Store position as numbers, not as a character hidden in a picture. For a grid
of rows, use `picture[y][x]`. Copy a template before changing it. These rules
will let the next checkpoint update the same state rather than rebuilding the
idea from scratch.

## Exact Reference Game Comparison

The checkpoint's two integers correspond to the reference game's
`game/player.py:Player.x` and `game/player.py:Player.y` fields. The reference
player also has `tile_x` and `tile_y` for the larger world grid, plus inventory
and health. `game/room.py:is_floor` checks whether a local coordinate is usable,
while `game/main.py:draw_screen` renders the player over the room. The
checkpoint has only local coordinates and one marker, but it establishes the
same separation: terrain is one value, player state is another, and rendering
combines them.
