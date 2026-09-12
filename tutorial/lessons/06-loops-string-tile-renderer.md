# 06: Loops, Range, And A Tile Renderer

**Coding exercise:** `06_loops_string_tile_renderer.py` | **Model answer:** `../solutions/06_loops_string_tile_renderer.py`

## What You Will Build

You will build a tiny renderer that turns a set of openings into a five-row,
seven-column ASCII tile. The checkpoint is
`tutorial/checkpoints/06_tile_renderer.py`. It renders an east-west corridor
and then a tile open in all four directions.

The important idea is that the program stores one basic picture and edits only
the boundary cells that should be open. You do not need to write a different
five-line drawing for every combination of directions.

## Learning Goals

- Repeat work with `for` loops.
- Understand that `range` stops before its end value.
- Read and write list indexes.
- Use nested loops and generator expressions.
- Build strings with `join`.
- Keep rendering separate from game rules.

## New Words With Plain Definitions

- A **loop** repeats an indented block of code.
- `range` produces integer positions for a loop.
- An **index** is a position inside a sequence, starting at zero.
- A **nested loop** is a loop inside another loop.
- A **renderer** turns data into visible output.
- A **mutable** value can be changed after creation.
- **Composition** means combining small results into a larger result.
- A **generator expression** produces values one at a time for a function.
- **Cohesion** means that a function's responsibilities belong together.

## Why This Matters

The tile from lesson 05 can have sixteen possible opening sets, including the
empty set and all four directions. Copying sixteen pictures would make every
visual change tedious. A renderer gives us one recipe. The input says which
openings exist; the renderer decides how those openings look.

This division also prevents a common design problem. Drawing code should not
decide whether a player is allowed to walk through a doorway. A renderer can
show a space at the east edge, while a separate movement rule decides whether
that space is reachable. Keeping those jobs separate makes both functions
smaller and easier to test.

## Tiny Examples Explained Line By Line

```python
for number in range(3):
    print(number)
```

1. `for number` gives the current loop value the name `number`.
2. `range(3)` produces `0`, `1`, and `2`; it does not produce `3`.
3. The colon starts the loop body.
4. Indentation makes `print(number)` run once for each value.

Here is a list being built and then joined:

```python
letters = []
for number in range(3):
    letters.append(str(number))
print("-".join(letters))
```

1. `letters = []` creates an empty list.
2. The loop runs three times.
3. `str(number)` changes each integer into text.
4. `append` adds that text to the end of the list.
5. `"-".join(letters)` puts a hyphen between the list items.
6. The result is `0-1-2`.

`join` needs strings. It does not automatically turn integers into strings,
which is why `str` appears in the loop.

## Guided Build Tied To The Actual Checkpoint

The checkpoint starts `render` with this list of lists:

```python
rows = [
    list("+-----+"),
    list("|     |"),
    list("|     |"),
    list("|     |"),
    list("+-----+"),
]
```

The five outer items are rows. Each `list(...)` turns a string into individual
characters so a single cell can be replaced. Strings are not editable one
character at a time, but lists are mutable. The top and bottom rows begin with
horizontal walls, and the middle three rows begin and end with vertical walls.

Now read the four checks one at a time:

```python
if "N" in openings:
    rows[0][3] = " "
```

If north is open, row zero, column three becomes a space. Index three is the
middle character of the seven-character top edge. The south check changes
`rows[4][3]`. The west check changes `rows[2][0]`, and the east check changes
`rows[2][6]`. Notice the coordinate convention: `rows[y][x]`, with row first.

The return statement has two joins:

```python
return "\n".join("".join(row) for row in rows)
```

The inner `"".join(row)` turns each character list back into one line. The
outer `"\n".join(...)` places newline characters between those lines. The
result is one string that `print` can display. The input set is only read; it
is not changed by the renderer.

`main` calls `render` twice. The first call supplies `{"E", "W"}`, so only
the left and right walls have gaps. The second supplies all four directions,
so all four middle boundary cells have gaps. Both calls use the same recipe.

## Complete Checkpoint Walkthrough

Run the checkpoint and compare the two pictures. The first output is:

```text
+-----+
|     |
      
|     |
+-----+
```

The middle line appears blank because the left and right wall characters were
both replaced by spaces. The second output is:

```text
+-- --+
|     |
      
|     |
+-- --+
```

The exact appearance includes spaces, so viewing it in a proportional font can
be confusing. Count positions in the source if necessary. The top and bottom
center gaps represent north and south. The blank-looking middle row represents
east and west. No player, random number, or movement rule is involved yet.

Try changing the first call to `render({"N"})`. Only the top center should
open. Try `render(set())`; all walls should remain closed. These experiments
are useful because they connect one data change to one visual change.

## Common Mistakes

- `range(3)` ends at 2, not 3.
- Missing indentation changes which statements belong to the loop or `if`.
- A string cannot be edited at `text[3]`; convert it to a list first.
- Join characters into rows before joining rows into a picture.
- `rows[0][3]` means row zero, column three, not the reverse.
- Do not mutate `openings` while rendering it.
- Spaces are visible output data; do not trim them while debugging.

## Fun Side Quests

1. Render a north-only dead end and predict every changed cell.
2. Add a center marker such as `o`, then decide whether it is geometry or
   decoration.
3. Write a loop that renders every one of the sixteen direction masks.
4. Make a version with `.` for floor and explain why it is harder to see.
5. Add a title above each rendering that prints the sorted opening letters.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/06_tile_renderer.py
```

Expected result: two five-line ASCII tile pictures. The first has east and
west openings. The second has north, east, south, and west openings. The
program then ends without an error.

## Learner Questions

- Why do we use lists while constructing the picture and strings at the end?
- Which index is the center of a seven-character row?
- Why should a renderer avoid deciding whether an opening is safe?
- What would happen if `join` received integers instead of strings?
- How would you render a tile upside down without changing its input data?

## What To Remember

Loops remove repeated code, `range` supplies positions, and `join` composes
small strings into a larger picture. The renderer reads opening data and draws
it; it does not own movement, collision, or combat rules.

## Exact Reference Game Comparison

The checkpoint's `render(openings)` grows into `game/tiles.py:Tile.render`,
`game/tiles.py:Tile._add_room_walls`, and
`game/tiles.py:Tile._carve_corridor`. The reference game calculates opening
regions with `game/tiles.py:_opening_bounds` and exposes exact edge cells with
`game/tiles.py:opening_cells`. `game/room.py:build_room` requests a room open on
all four sides. The final screen is assembled by
`game/main.py:draw_screen`, which displays the result of the game renderer.
