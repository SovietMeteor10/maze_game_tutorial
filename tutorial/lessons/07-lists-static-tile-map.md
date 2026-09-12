# 07: Lists Of Lists, Rows, Columns, And A Static Map

**Coding exercise:** `07_lists_static_tile_map.py` | **Model answer:** `../solutions/07_lists_static_tile_map.py`

## What You Will Build

You will assemble several small tile fragments into one hand-authored map.
The checkpoint is `tutorial/checkpoints/07_static_tile_map.py`. Its `MAP` is a
three-by-three list of tile-sized strings. The program joins each row of tiles
side by side, joins the completed rows vertically, and reports the dimensions.

This lesson adds a second level of organization. A tile is made from
characters, while a map is made from tiles. Keeping those layers visible helps
you reason about coordinates and prepares you for generated maps later.

## Learning Goals

- Read a nested list using row-first indexing.
- Tell a row from a column.
- Use `len` to inspect map dimensions.
- Join tile fragments horizontally and vertically.
- Understand a rectangular-map invariant.
- Distinguish tile layout from the characters inside one tile.

## New Words With Plain Definitions

- A **list** is an ordered collection of values.
- A **nested list** is a list containing other lists.
- A **row** runs from left to right.
- A **column** runs from top to bottom.
- A **tile** is one map-sized piece of a larger world.
- A **fragment** is a small piece that can be combined with other pieces.
- A **dimension** is a size, such as three rows by three columns.
- **Static** means fixed while the program runs.
- A **coordinate convention** is an agreed meaning for each index.
- An **invariant** is a fact that should remain true.
- **Rectangular** means every row has the same number of columns.

## Why This Matters

Earlier, a room was a character grid. That is useful when drawing one room,
but it becomes awkward when describing a dungeon made of many rooms. A nested
list gives the map its own layer: `MAP[y][x]` identifies a tile, and the tile's
string describes its local appearance.

This is a form of composition. The final display is assembled in stages:
characters make tile strings, tile strings make map rows, and map rows make a
whole screen. If the tile width changes, you can update the fragments without
changing the idea of row and column lookup.

Rectangularity is also important. If row zero has three tiles but row one has
four, Python will allow the list, but a renderer that expects a grid may create
an uneven picture. We call "every row has the same length" an invariant because
it is a fact we want to preserve whenever the map changes.

## Tiny Examples Explained Line By Line

```python
grid = [["A", "B"], ["C", "D"]]
print(grid[1][0])
```

1. The outer list has two rows.
2. The first inner list is row zero: `A`, then `B`.
3. The second inner list is row one: `C`, then `D`.
4. `grid[1]` selects the second row.
5. `[0]` then selects the first item in that row.
6. The printed answer is `C`.

With the map convention used here, the first index is `y` and the second is
`x`: `grid[y][x]`. Saying "row one, column zero" out loud prevents reversing
the indexes.

```python
for row in grid:
    print(" ".join(row))
```

1. The loop receives one inner list at a time.
2. `" ".join(row)` places a space between that row's values.
3. `print` writes one finished row per loop pass.

## Guided Build Tied To The Actual Checkpoint

Open `tutorial/checkpoints/07_static_tile_map.py`. Its map is:

```python
MAP = [
    ["+---+", "     ", "+---+"],
    ["| . |", " . . ", "| . |"],
    ["+---+", "     ", "+---+"],
]
```

There are three outer items, so there are three map rows. Each outer item is
itself a list of three tile fragments, so there are three map columns. Each
fragment is five characters wide and five characters high when the three
corresponding map rows are viewed together.

Read the coordinate `(tile_x, tile_y)` as `(column, row)`. In Python that is
`MAP[tile_y][tile_x]`. For example, `MAP[0][2]` is the tile at column two,
row zero, which is `"+---+"`. Do not call this a character grid: the outer
values are tile pieces, even though each piece is text.

The main display expression is:

```python
print("\n".join("".join(row) for row in MAP))
```

The inner join takes one outer row and places its three tile strings directly
beside one another. The outer join places the resulting lines underneath one
another. In this tiny example, each outer row contributes one screen line,
because each tile fragment is only one line of text. The code is intentionally
small; the lesson is the two levels of data, not a full room renderer.

The second print uses `len(MAP)` for the number of rows. `len(MAP[0])` counts
the columns in the first row. This assumes the map is non-empty and
rectangular. That assumption is fine for the checkpoint, but a larger game
should validate it explicitly.

## Complete Checkpoint Walkthrough

Run the checkpoint and read the output as three tile columns:

```text
+---+     +---+
| . | . . | . |
+---+     +---+
The map has 3 rows and 3 columns.
```

The first printed line joins the first outer row: a left border, a blank middle
piece, and a right border. The second line places dots in all three sections,
and the final map line closes the top and bottom pieces. The dimension line is
not inferred from the visual output; it comes directly from the nested list.

Change the center value in the source to `" TREASURE "` and run again. The
center display changes, but the map remains three rows by three columns as long
as the replacement stays compatible with the intended width. Add a fourth
fragment to only the first row. Python still accepts it, but the screen is no
longer rectangular. This experiment shows why a validator is useful.

If you want a simple check, add this after `MAP` while experimenting:

```python
assert MAP and all(len(row) == len(MAP[0]) for row in MAP)
```

The first condition rejects an empty map. The `all` expression checks every
row against the first row's length. You do not need to add it to the official
checkpoint for this lesson; understand what it protects first.

## Common Mistakes

- Reversing `MAP[y][x]` into `MAP[x][y]`.
- Reading `len(MAP[0])` when `MAP` is empty.
- Adding a tile to one row and forgetting the rectangular invariant.
- Mixing tile fragments with different intended widths.
- Losing a quote, comma, or bracket in the nested literal.
- Forgetting that list indexes start at zero.
- Treating a tile fragment as if it were the whole screen.

## Fun Side Quests

1. Design a five-by-five map on paper before typing it.
2. Put ` T ` in a tile and call it the treasure room.
3. Add the rectangularity assertion and intentionally make it fail.
4. Print column numbers above the map for debugging.
5. Write a function that returns the tile at `(x, y)` and test the corners.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/07_static_tile_map.py
```

Expected result: the three composed map lines shown above, followed by
`The map has 3 rows and 3 columns.` and no error.

## Learner Questions

- What does `MAP[0][2]` mean in words?
- Why is the first index a row in the Python list but `x` often names a column?
- What invariant must survive when you add a new tile?
- Should tile width be stored separately or measured from the data?
- When would a static, hand-authored map be better than a random map?

## What To Remember

Nested lists model rows and columns. The outer list arranges tiles, while the
inner text supplies tile content. Pick a coordinate convention, say it aloud,
and protect rectangular data when a map grows.

## Exact Reference Game Comparison

The checkpoint's `MAP` is a tiny hand-authored version of the larger structure
in `game/world.py:WorldMap`, which stores tile positions in dictionaries keyed
by `(x, y)`. Tile geometry is produced by `game/room.py:build_room` and
`game/tiles.py:Tile.render`, rather than by literal one-line fragments. The
reference game's `game/world.py:render_viewport` joins many rendered tile rows
into a screen, using the same outer composition idea at a larger scale.
