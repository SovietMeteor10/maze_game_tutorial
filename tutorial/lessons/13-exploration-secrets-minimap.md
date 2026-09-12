# 13: Secrets and the Minimap

**Coding exercise:** `13_exploration_secrets_minimap.py` | **Model answer:** `../solutions/13_exploration_secrets_minimap.py`

## What You Will Build

You will build a tiny exploration display that knows which tile coordinates the
player has discovered. One coordinate will be a secret. Before searching, the
minimap will show known tiles as `.` and the unknown position as `?`. Searching
will add the secret coordinate to the discovered set, and the minimap will then
show all three positions as known. The complete runnable checkpoint is
`tutorial/checkpoints/13_exploration_secrets_minimap.py`.

This is deliberately smaller than the finished game. It does not generate a
whole dungeon or move a player. It isolates one useful rule: discovery is game
state, while the minimap is a view derived from that state.

## Learning Goals

- Use a `set` to remember unique discovered coordinates.
- Represent a grid position as a tuple such as `(3, 1)`.
- Test membership with `in`.
- Change state with `add()`.
- Render known and unknown places differently.
- Understand why a hidden wall is an overlay instead of a replacement for the
  underlying terrain.

## New Words

- **Discovery:** the fact that the player has learned about a location.
- **Set:** a collection of unique values. Adding the same value twice does not
  create a duplicate.
- **Tuple:** a small, ordered group of values. `(3, 1)` can mean x 3, y 1.
- **Fog of war:** the visual hiding of places the player has not discovered.
- **Overlay:** extra information drawn on top of base data, such as a secret
  wall over an existing opening.
- **Derived rendering:** an image or string calculated from state instead of
  stored as a second, possibly stale copy of the truth.

## Why This Matters

Exploration games need memory. If walking away made every room unknown again,
the map would not be useful. A discovered set gives us that memory without
changing the map itself. This distinction is important: terrain describes what
the world is, while discovery describes what the player knows.

It also makes the program easier to test. Given `{(1, 1), (2, 1)}`, we can
predict that positions 1 and 2 are visible and position 3 is not. We do not
need to inspect terminal pixels. This is an example of interpretability: a
beginner can read the state and understand it directly.

## Tiny Example, Line by Line

```python
discovered = {(1, 1), (2, 1)}
secret = (3, 1)
if secret not in discovered:
    discovered.add(secret)
```

Line 1 creates a set containing two known coordinates. The curly braces mean a
set here because the values are coordinates and there is no `key: value` colon.
Line 2 names the hidden coordinate. Line 3 asks whether the secret is absent.
Line 4 records it as known. The `if` protects the action, although calling
`add()` twice would still be safe because sets remove duplicates.

Here is the rendering idea:

```python
" ".join("." if (x, 1) in discovered else "?" for x in range(1, 4))
```

`range(1, 4)` visits 1, 2, and 3. For each x, `(x, 1)` is tested. A known
coordinate becomes `.`, otherwise it becomes `?`. `join()` puts spaces between
the resulting symbols. This is a compact loop; expand it into an ordinary
`for` loop if it feels too dense.

## Guided Build: Tie It To The Checkpoint

Open `tutorial/checkpoints/13_exploration_secrets_minimap.py`. First read it
without typing. Notice that `discovered` is the only long-lived map memory.
`secret` is separate. The program prints a before message, checks the secret,
adds it, and prints a minimap.

To build your own version, start with the same three values:

```python
discovered = {(1, 1), (2, 1)}
secret = (3, 1)
```

Print `Before search: . . ?` so the intended state is visible. Then write the
membership check. Inside it, print `A secret wall is found.` and add the tuple.
Finally, use the generator expression from the tiny example to produce the
minimap. Keep the coordinate order consistent. This project uses `x, y` for a
coordinate, while a grid stored as rows often uses `grid[y][x]`.

## Complete Checkpoint Walkthrough

The checkpoint begins with `discovered = {(1, 1), (2, 1)}`. The player knows
the first two positions. `secret = (3, 1)` is not in the set, so the `if` body
runs. The message confirms that searching found the hidden wall. `add(secret)`
changes the set to three coordinates. The final `print()` loops from x 1 to x
3. Every coordinate is now in the set, so every conditional expression chooses
`.`. The output is:

```text
Before search: . . ?
A secret wall is found.
Minimap: . . .
```

The checkpoint is intentionally non-interactive. The search is represented by
the code reaching the `if`, allowing a repeatable smoke test.

## Common Mistakes

- Writing `discovered = [(1, 1), (2, 1)]` creates a list, not a set. Membership
  still works, but the lesson about unique discovery is lost.
- Using `(1, 3)` when the secret is `(3, 1)` swaps coordinates.
- Using `range(1, 3)` forgets that the stop value is exclusive, so x 3 is not
  rendered.
- Replacing the terrain with `?` makes the base map forget what is there. Keep
  visibility separate from terrain.
- Drawing the secret before adding it makes the output look discovered even
  though state says otherwise.

## Side Quests

1. Add a fourth coordinate `(1, 2)` and render a two-row minimap. Use nested
   loops and decide what unknown cells should look like.
2. Mark the player with `@` when the coordinate is `(2, 1)`, but keep `?` for
   unknown locations.
3. Replace `.` with `S` for the start, `E` for the exit, and `B` for a boss
   landmark. Store landmarks in a dictionary and keep discovery in the set.

## Run Command And Expected Result

From the project root, run:

```text
python3 tutorial/checkpoints/13_exploration_secrets_minimap.py
```

Expected result:

```text
Before search: . . ?
A secret wall is found.
Minimap: . . .
```

## Learner Questions

- Why is a set a good fit for discovered coordinates?
- What information would be lost if the minimap were the only state?
- Why can an undiscovered connection exist in the world but remain hidden?
- What should happen if the player searches the same secret twice?

## Exact Reference Game Comparison

The reference uses `game/secrets.py` for a `SecretWall` overlay. It stores the
wall's tile coordinate, direction, and `found` flag. `game/game_state.py` keeps
secret walls separate from terrain and exposes discovered tiles through the
world. `game/world.py` masks undiscovered viewport tiles and renders the
minimap from discovered coordinates. The reference also creates searchable
frontier connections and reveals hidden rooms, so it has more placement rules
than this checkpoint. The core idea is identical: discovery is state, and
rendering is calculated from it.

## What To Remember

Keep the base world, the player's knowledge, and the display separate. A set is
excellent for unique discovered positions. A minimap should be derived from
state. A secret wall is an overlay that changes what the player may see or
cross, not a reason to corrupt the underlying map.
