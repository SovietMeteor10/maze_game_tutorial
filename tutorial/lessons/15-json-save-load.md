# 15: JSON Save And Load

**Coding exercise:** `15_json_save_load.py` | **Model answer:** `../solutions/15_json_save_load.py`

## What You Will Build

You will save a small game state as JSON text and load it back into Python. The
state contains a position, health, inventory, and random seed. The checkpoint
serializes it with `json.dumps()`, restores it with `json.loads()`, checks that
the restored value equals the original, and prints the result. Run
`tutorial/checkpoints/15_json_save_load.py` after reading this lesson.

## Learning Goals

- Explain persistence: data that survives after a program stops.
- Explain serialization and deserialization.
- Recognize JSON objects, arrays, numbers, strings, and booleans.
- Use Python's standard-library `json` module.
- Understand a round trip from Python data to text and back.
- Validate loaded data before trusting it.
- Keep file I/O at a boundary instead of mixing it into movement or rendering.

## New Words

- **Persistence:** keeping information so it can be used later, even after the
  process ends.
- **Serialization:** converting in-memory data into a storable or transferable
  format.
- **Deserialization:** converting that format back into program data.
- **JSON:** a text format for objects, arrays, strings, numbers, booleans, and
  null values.
- **Round trip:** serialize a value and deserialize it to recover an equivalent
  value.
- **Validation:** checking that data has the expected shape and safe values.
- **Schema:** an agreed description of which fields and types are allowed.

## Why This Matters

Without persistence, a game run disappears when Python exits. A save file lets
the player pause a long exploration and continue later. JSON is useful for a
beginner because it is readable text and is supported by Python directly.

Serialization is not the same as copying an object blindly. A `Player` object,
a set, or a tuple may need to be converted into plain values first. The save
format should contain facts, not live methods. This boundary also improves
testability: we can test saving and loading with a small dictionary without
starting a terminal game.

## Tiny Example, Line by Line

```python
import json
state = {"position": [2, 1], "health": 8, "inventory": ["gold"], "seed": 7}
text = json.dumps(state, sort_keys=True)
restored = json.loads(text)
assert restored == state
```

`import json` loads the standard library module. `state` is made only of JSON
friendly values: a dictionary, lists, strings, and integers. `dumps()` means
dump to a string; it returns text rather than writing a file. `sort_keys=True`
makes the printed order predictable, which is friendly for tests and examples.
`loads()` means load from a string. The assertion checks the round trip.

JSON changes some Python details. A Python tuple becomes a JSON array and loads
as a list. A set is not directly supported. A custom class is not directly
supported either. Convert such values to dictionaries or lists before saving.

## Guided Build: Tie It To The Checkpoint

Open `tutorial/checkpoints/15_json_save_load.py`. Notice that it uses no game
class and does not create a file. This is the smallest useful checkpoint for
learning the format. Copy its `state` shape first. Run it and inspect the JSON
line. JSON uses double quotes around property names and strings, and square
brackets for arrays.

Next, imagine a file boundary:

```python
with open("save.json", "w") as file:
    file.write(text)
```

and later:

```python
with open("save.json") as file:
    restored = json.load(file)
```

`json.dump(state, file)` and `json.load(file)` are convenient file versions of
`dumps` and `loads`. Do not add this to the checkpoint unless you want a side
experiment; the official checkpoint is deterministic and leaves no extra file.

## Complete Checkpoint Walkthrough

The starting dictionary says the player is at `[2, 1]`, has 8 health, owns a
gold item, and the world seed is 7. `json.dumps()` turns it into one text value.
The exact ordering is stable because keys are sorted:

```text
{"health": 8, "inventory": ["gold"], "position": [2, 1], "seed": 7}
```

`json.loads()` parses that text. The result is a new dictionary with the same
values. The assertion proves equality. Finally, `tuple(restored["position"])`
converts the loaded position list to `(2, 1)` for a readable display. The
expected output is:

```text
JSON: {"health": 8, "inventory": ["gold"], "position": [2, 1], "seed": 7}
Loaded position: (2, 1)
```

The checkpoint proves data survived a format conversion. It does not yet prove
that an arbitrary, edited save file is safe.

## Validation Before Replacement

Never replace active game state with untrusted loaded data immediately. First
check that it is a dictionary, that required keys exist, and that values make
sense. For example, health might need to be an integer from 0 through 20,
position might need two integers, and inventory might need a list of strings.
Rejecting bad data is validation. It protects the game from confusing crashes
and impossible states.

```python
def valid_save(data):
    return (
        isinstance(data, dict)
        and isinstance(data.get("health"), int)
        and 0 <= data["health"] <= 20
        and isinstance(data.get("inventory"), list)
    )
```

This is only a start: booleans count as integers in Python, and position still
needs checking. The important design is to validate first, then replace state.

## Common Mistakes

- Calling `json.loads(state)` instead of serializing the dictionary first.
- Expecting a tuple to load as a tuple; JSON arrays load as lists.
- Trying to serialize a set or class instance directly.
- Treating JSON text as if it were a Python dictionary before calling `loads()`.
- Loading a file and trusting every field without validation.
- Saving only the display string and losing gameplay facts such as seed or HP.

## Side Quests

1. Add a `boss_defeated` Boolean and a `discovered` list of coordinate lists.
   Explain how a set would need conversion before saving.
2. Write a save file with `json.dump()` and load it with `json.load()`. Inspect
   the file in a text editor.
3. Make validation reject health `-1`, a missing `position`, and an inventory
   that is a string instead of a list.
4. Add a `version` field such as `1`. Ask how a future program could migrate
   an older save format.

## Run Command And Expected Result

From the project root, run:

```text
python3 tutorial/checkpoints/15_json_save_load.py
```

Expected result:

```text
JSON: {"health": 8, "inventory": ["gold"], "position": [2, 1], "seed": 7}
Loaded position: (2, 1)
```

## Learner Questions

- Which values in the checkpoint are JSON-friendly?
- Why is `sort_keys=True` helpful in a teaching checkpoint?
- What is the difference between `dumps` and `dump`?
- What should happen when a save has health 900?
- Why should file reading not be inside the movement function?

## Exact Reference Game Comparison

The tutorial checkpoint is an intentional extension. `plan.md` and the
reference product document say JSON save/load is not shipped in the current
`game/` product. The planned boundary is still clear: save player data, seed or
generated map, inventory, doors, discoveries, monsters, and progression, then
validate before replacing active state. Do not claim that `game/save.py` is a
reference module; it does not exist in this checkout. This checkpoint teaches
the planned persistence boundary without changing `game/`.

## What To Remember

Persistence keeps a run beyond one process. Serialization turns plain state into
JSON text; deserialization restores it. Prefer plain data, validate loaded data,
and keep file I/O at the edge of the program. A successful round trip is the
smallest proof that your save format is coherent.
