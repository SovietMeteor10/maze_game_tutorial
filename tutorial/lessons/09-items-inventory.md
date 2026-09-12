# 09: Items And An Inventory

**Coding exercise:** `09_items_inventory.py` | **Model answer:** `../solutions/09_items_inventory.py`

This lesson gives the maze something worth finding. You will represent a key and a potion, place them on the floor, and move them into the player's inventory. The checkpoint is deliberately small. There is no keyboard input yet, so the loop acts out two pickups for us. That lets us study the data movement before we combine it with movement and collision.

## What You Will Build

You will study `tutorial/checkpoints/09_items_inventory.py`. It creates an `Item` data class, stores two items in a dictionary called `floor`, and stores collected items in a list called `inventory`. A loop removes the item at `(2, 1)` and then the item at `(3, 1)` with `pop`. Each removed item is added to the inventory with `append`.

The result is a tiny but real game rule: an item cannot be both on the floor and in the inventory after pickup. The screen is not responsible for that rule. The data structures and pickup code are responsible. This is our first useful example of separation of concerns.

## Learning Goals

- Explain what an item and an inventory represent.
- Read a `dataclass` with named fields.
- Use a tuple coordinate as a dictionary key.
- Understand list mutation with `append`.
- Understand dictionary mutation with `pop`.
- Separate the rule that changes game data from the text that reports it.
- Compare this teaching checkpoint with the actual reference game's item model.

## New Words With Plain Definitions

- **Item**: A thing in the game that can be found, carried, or used.
- **Inventory**: The collection of items currently carried by a player.
- **Floor**: Here, a dictionary describing items that are lying in the room.
- **Dataclass**: A Python feature that makes a small data-holding class with less setup code.
- **Field**: A named piece of data, such as `name` or `symbol`.
- **Dictionary**: A collection that connects keys to values. Here, a coordinate connects to an item.
- **Tuple**: A fixed group of values. `(2, 1)` is a two-number coordinate tuple.
- **Mutation**: Changing an existing list, dictionary, or object instead of creating a separate replacement.
- **Append**: Add one value to the end of a list.
- **Pop**: Remove a dictionary entry and return its value.
- **Separation of concerns**: Give different jobs to different parts of a program. Data storage, game rules, and display should not all be tangled together.

## Why This Matters

An adventure game needs to answer two different questions: "What is lying here?" and "What is the player carrying?" The `floor` dictionary answers the first question. The `inventory` list answers the second. Pickup is the transfer between those two places.

This transfer is state change. Before pickup, the key is floor state. After pickup, it is inventory state. If you only append the key, the player appears to carry it but the key is still on the map. If you only pop it, the key disappears. Correct code performs both changes as one small rule.

Separation of concerns matters because display changes often. Today the program prints `Picked up Gold Key`. Tomorrow a graphical interface might draw an icon, play a sound, and update a menu. The pickup rule should still be the same. The rule changes collections; another part can decide how to show the result.

## Tiny Examples Explained Line By Line

```python
floor = {(2, 1): "key"}
item = floor.pop((2, 1))
inventory = [item]
print(inventory)
```

Line 1 creates a dictionary. The coordinate `(2, 1)` is the key, and the string `"key"` is the value.

Line 2 looks up that coordinate, removes the entry, and saves the returned value in `item`. `pop` does two jobs at once.

Line 3 creates an inventory list containing the removed value. In the checkpoint, `append` makes the same change one step at a time.

Line 4 displays the inventory. The dictionary is now empty, so the key has one clear owner.

```python
inventory = []
inventory.append("potion")
print(inventory)
```

The first line creates an empty list. The second line mutates that list in place. The variable still refers to the same list, but its contents changed. The last line prints `['potion']`.

## Guided Build Tied To The Checkpoint

Open `tutorial/checkpoints/09_items_inventory.py` while reading this section. The import brings in `dataclass`. The `@dataclass` line tells Python that `Item` is mainly a bundle of named data. The class has two fields: `name` is human-readable text, and `symbol` is a short map character. Because this is a dataclass, Python supplies useful setup behavior, so `Item("Gold Key", "k")` creates an object with those fields.

Inside `main`, the `floor` dictionary has two entries. Notice that the values are `Item` objects, not plain names. That means the program can use `item.name` for a menu and `item.symbol` for a map. `inventory = []` starts the player with nothing. `position = (1, 1)` records a starting position, although this checkpoint does not use movement to change it.

The `for` loop visits the two demonstration coordinates. `floor.pop(position)` removes the item at the current coordinate. `inventory.append(item)` mutates the inventory by adding that object. The print statement uses `item.name`, because printing the whole object would show a less friendly representation. The final list expression reads every object in `inventory` and collects only its names.

Do not confuse the variable `position` with movement logic. The checkpoint is practicing item transfer, not collision. Later lessons can call the same idea after a real player walks onto a cell.

## Complete Checkpoint Walkthrough

Run the file with the command below. Python enters `main` because the final `if` statement checks that this file was run directly. `main` builds the floor, performs two pickups, and prints the final inventory.

The first pickup removes the `Gold Key` object from `(2, 1)` and appends it. The second removes the `Potion` object from `(3, 1)` and appends it. The expected output is:

```text
Picked up Gold Key
Picked up Potion
Inventory: ['Gold Key', 'Potion']
```

The checkpoint does not ask whether a coordinate contains an item before calling `pop`, does not read keys, and does not use an item. Those are future rules. A focused checkpoint makes one idea visible.

## Common Mistakes

- Calling `floor.pop((9, 9))` when that coordinate is absent raises `KeyError`.
- Appending an item without popping it leaves a duplicate on the floor.
- Storing plain text instead of an `Item` object means `item.name` will fail later.
- Writing `item["name"]` is dictionary syntax; this object uses `item.name`.
- A list does not automatically know that a potion heals or that a key opens a door.
- A tuple coordinate is not the same as two separate dictionary keys.
- Do not add keyboard code yet. First make the transfer correct.

## Fun Side Quests

1. Add `Item("Lantern", "l")` at `(4, 1)` and collect it in a third loop entry.
2. Print both names and symbols. Decide which belongs in a map and which belongs in an inventory menu.
3. Try collecting `(2, 1)` twice. Explain why the second `pop` fails, then write down what a real game should do instead.
4. Add a `value` field to the dataclass and calculate the total treasure value.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/09_items_inventory.py
```

Expected result: two pickup messages followed by `Inventory: ['Gold Key', 'Potion']`.

## Learner Questions

- Why is the floor a dictionary while the inventory is a list?
- What exactly does `pop` return?
- Why is mutation useful here, and when might making a new collection be clearer?
- Which part should change if you replace printed text with a graphical inventory?

## What To Remember

Pickup is a state transition from floor to inventory. `Item` groups related facts, `pop` removes the old location, and `append` records ownership. Separation of concerns keeps the pickup rule independent from display.

## Exact Reference Game Comparison

The reference game stores its richer item model in `game/items.py`. Its `Item` dataclass has world and local coordinates, a name, a kind, a symbol, an optional key ID, and a quantity. The checkpoint's `Item` has only `name` and `symbol`, but both represent an item as data instead of unrelated variables. In the reference game, `game/game.py` keeps floor items in `GameState.items` and transfers a collected item into `game/player.py`'s `Player.inventory`. The checkpoint uses a coordinate dictionary and a direct loop instead of real movement, but the ownership boundary is the same.
