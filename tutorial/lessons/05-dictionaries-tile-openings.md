# 05: Dictionaries, Keys, Values, And Tile Openings

**Coding exercise:** `05_dictionaries_tile_openings.py` | **Model answer:** `../solutions/05_dictionaries_tile_openings.py`

## What You Will Build

You will build the data model for the next part of the maze: a small catalogue
of tile names and the directions in which each tile is open. The checkpoint is
`tutorial/checkpoints/05_tile_openings.py`. It describes a room, corridor,
corner, and dead end, prints their openings, and checks whether two tiles agree
about an east-west connection.

This is not yet a complete map. It is a useful small step before a map exists.
Instead of hiding door information in a long collection of `if` statements, we
will put the information in data that the rest of the game can inspect.

## Learning Goals

- Create dictionaries with names and values.
- Read a value by using a dictionary key.
- Use sets to store unique direction letters.
- Compare two boolean results with `==`.
- Represent a tile connection as a reusable rule.
- Notice the difference between describing a tile and drawing a tile.

## New Words With Plain Definitions

- A **dictionary** is a collection that connects a key to a value.
- A **key** is the label used to find one item in a dictionary.
- A **value** is the information stored under a key.
- A **set** is a collection of unique values, with no promised order.
- A **boolean** is either `True` or `False`.
- A **direction** is one of `N`, `E`, `S`, or `W`.
- An **opening** is a side of a tile where the player can leave it.
- A **neighbor** is a tile directly beside another tile.
- **Data modeling** means choosing data that represents an idea clearly.
- A **connection** is an agreement between neighboring things.

## Why This Matters

Games contain many objects that have properties. A tile has a name, openings,
and later a shape. A potion has a name and an effect. A monster has health and
position. Dictionaries are a beginner-friendly way to group related facts
without creating a class yet.

The set of openings is especially important. A corridor that runs east and
west has two facts: it is open to the east and it is open to the west. A set
expresses exactly that. There is no accidental second `E`, and membership is
easy to ask with `in`.

The model also lets one rule handle every tile. The connection rule does not
need to know what a corridor is called or what a corner looks like. It only
needs to ask whether the left tile has an east opening and the right tile has a
west opening. This separation will make the later renderer and world builder
easier to understand.

## Tiny Examples Explained Line By Line

```python
door = {"state": "locked", "key": "gold"}
print(door["state"])
```

1. `door =` gives a name to the new value.
2. The braces create a dictionary.
3. `"state"` is a key, and `"locked"` is its value.
4. The comma separates the first entry from the second entry.
5. `door["state"]` looks up the value stored under the key `"state"`.
6. `print` displays `locked`.

Here is a set:

```python
openings = {"N", "E"}
print("E" in openings)
```

1. The braces contain two values but no colons, so this is a set.
2. The set says that north and east are open.
3. `"E" in openings` asks whether east is a member.
4. The answer is the boolean `True`, which `print` displays.

Do not confuse the two brace forms. A dictionary has `key: value` pairs. A set
has values separated by commas. An empty set is written `set()`, not `{}`,
because `{}` means an empty dictionary.

## Guided Build Tied To The Actual Checkpoint

Open `tutorial/checkpoints/05_tile_openings.py` and first read `TILES`:

```python
TILES = {
    "room": {"N", "E", "S", "W"},
    "corridor": {"E", "W"},
    "corner": {"E", "S"},
    "dead_end": {"N"},
}
```

The outer dictionary maps a tile name to its set of openings. The room has all
four sides. The corridor has east and west. The corner has east and south. The
dead end has only north. Spend a moment reading each line as a sentence: "the
corridor has these openings." That is the habit of reading data before code.

Next, `OPPOSITE` records direction pairs. North faces south, east faces west,
and so on. The checkpoint does not use this dictionary in its short rule, but
the relationship is worth naming now because a complete map must use it.

The function is:

```python
def connected(left, right):
    return ("E" in left) == ("W" in right)
```

The first membership test produces `True` if `left` opens east. The second
produces `True` if `right` opens west. `==` asks whether those answers match.
This exact checkpoint treats two closed sides as matching too. That is why the
function is a small demonstration rather than a complete map validator. A
stricter version could require both sides to be open, but do not silently
change the checkpoint while learning from it.

Finally, `main` loops over `TILES.items()`. Each pass receives a name and its
opening set. `sorted(openings)` makes output predictable, and `"".join(...)`
turns letters such as `E` and `W` into `EW`. The two `assert` statements are
tests: a corridor matches another corridor, and a north-only dead end does not
match an east-west corridor on this rule.

## Complete Checkpoint Walkthrough

Run the file from the project root. You should see these four descriptions in
dictionary insertion order:

```text
room: ENSW
corridor: EW
corner: ES
dead_end: N
```

There is no printed success message. If both assertions pass, Python simply
ends after printing the descriptions. If an assertion fails, Python shows an
`AssertionError`; that means one of the expected facts is no longer true.

Trace the first assertion by hand. A corridor contains `E`, so the left test
is `True`. The second corridor contains `W`, so the right test is `True`.
`True == True` is `True`. For the second assertion, the dead end lacks `E`
and the corridor has `W`, so the comparison is `False`; `assert not False`
passes.

## Common Mistakes

- A dictionary entry needs a colon: `"room": {"N"}`.
- A set has values, not key-value pairs.
- `TILES["missing"]` raises `KeyError` because that key is absent.
- Sets do not promise display order, so sort them before printing.
- Use one direction convention everywhere; do not mix `east` and `E` casually.
- A connection must consider both neighboring sides in a full validator.
- `==` compares values; `=` assigns a value.

## Fun Side Quests

1. Add a `t_junction` with `{"N", "E", "W"}` and predict its output.
2. Write `opposite(direction)` that returns `OPPOSITE[direction]`.
3. Add a `treasure_room` with all four openings and print it.
4. Add a `has_opening(tile, direction)` function and test it with assertions.
5. Decide whether an isolated tile with no openings should be called a room,
   a wall, or a very stubborn closet.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/05_tile_openings.py
```

Expected result: the four lines `room: ENSW`, `corridor: EW`, `corner: ES`,
and `dead_end: N`, followed by no error and no assertion output.

## Learner Questions

- Why is a set a better description of unique openings than a list here?
- Why does sorting matter for printed output but not for membership?
- Should two closed sides count as connected in a real maze?
- Where would a locked door belong: in tile geometry or in game state?
- What new tile type can you describe with only a name and a set?

## What To Remember

Dictionaries name concepts, sets store unique openings, and membership tests
turn tile facts into simple rules. Data is easier to reuse when it describes
what a tile is instead of mixing that description into every operation.

## Exact Reference Game Comparison

The small `TILES` dictionary is expanded by `game/tiles.py:Tile`, whose
`openings` field stores a `frozenset` and whose `is_open` method checks one
direction. `game/tiles.py:classify_openings` names shapes from opening sets, and
`game/tiles.py:room_for_openings` validates direction names. The reference
game's `game/world.py:generate_tiles` creates connections and
`game/world.py:validate_connections` checks both sides using the same opposite
direction idea. The checkpoint teaches the data model before those production
rules are added.
