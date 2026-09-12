# 10: State, Mutation, Doors, And Keys

**Coding exercise:** `10_state_doors_keys.py` | **Model answer:** `../solutions/10_state_doors_keys.py`

A door is more than a wall symbol. It can be locked now and open later. This lesson names that changing information as state and shows a safe order for changing it. The checkpoint uses a simple dictionary for one door and a list for one inventory. It is small enough to trace by hand, but it models a real progression rule.

## What You Will Build

You will study `tutorial/checkpoints/10_doors_keys.py`. It creates `door = {"key": "gold", "state": "locked"}` and `inventory = ["gold"]`. The function `try_open(door, inventory)` checks the current state, checks whether the required key is carried, consumes the key, changes the door to open, and returns a status word.

The checkpoint also explains an overlay. The terrain is the base map. The door is extra information placed on top of a connection. Opening the door changes the overlay, not the underlying terrain data.

## Learning Goals

- Define state and state transition in plain language.
- Tell the difference between reading data and mutating data.
- Validate an action before changing anything.
- Trace a function with early returns.
- Explain why separation of concerns helps maps and doors evolve independently.
- Connect the tiny dictionary example to the reference game's `Door` class.

## New Words With Plain Definitions

- **State**: The current facts about a game, such as a door being locked.
- **State transition**: A rule-driven change from one state to another.
- **Mutation**: Changing an existing object, list, or dictionary in place.
- **Validation**: Checking whether an action is allowed before doing it.
- **Branch**: One route through code selected by a condition.
- **Return value**: The result a function sends back to its caller.
- **Overlay**: Information drawn or stored above a base layer without replacing that base.
- **Key**: In this lesson, a carried item that permits a door action. In a dictionary, a key is also a lookup label.
- **Consumption**: Removing a resource because an action used it.
- **Separation of concerns**: Keeping terrain, progression rules, inventory, and display in distinct jobs.

## Why This Matters

Without state, every door is permanently the same. With state, a player can explore, find a gold key, return to a locked connection, and make progress. The important detail is not the word `open`; it is that the program changes its stored facts only when the requirements are met.

The order of operations protects the player. First ask whether the door is already open. Then ask whether the required key is in the inventory. Only after those checks should the code remove the key and mutate the door. If the key is missing, the inventory must remain unchanged. This is validation before mutation.

The function returns text instead of printing inside every branch. That is a small separation of concerns. A terminal program can print the result. A graphical program could show the same result in a message panel. A test could compare the returned value without reading screen output.

## Tiny Examples Explained Line By Line

```python
door = {"state": "locked"}
if door["state"] == "locked":
    door["state"] = "open"
print(door["state"])
```

The first line creates a dictionary with one state field. The second line reads that field. The indented assignment mutates the existing dictionary, changing the value from `"locked"` to `"open"`. The final line reads the new state. Reading does not change data; assignment does.

```python
def spend(inventory, required):
    if required not in inventory:
        return False
    inventory.remove(required)
    return True
```

The function receives references to an inventory and a required item. The condition rejects the action before mutation when the item is absent. `remove` mutates the list only after validation. The two return statements provide a simple success or failure result.

## Guided Build Tied To The Checkpoint

Read `try_open` from top to bottom. The first condition handles an already-open door. This prevents a second attempt from consuming another key. The second condition asks whether `door["key"]` is in `inventory`. Remember that the dictionary entry named `key` is the required item name; it is not the same concept as a dictionary lookup key.

When the required string is present, `inventory.remove(door["key"])` consumes one copy. Then `door["state"] = "open"` mutates the door dictionary. The function returns `"unlocked"`, which describes what happened. If the condition fails, the final return is `"locked"`; no inventory or door mutation occurs.

In `main`, the inventory contains `"gold"`, matching the door's requirement. The call is inside `print`, so Python evaluates `try_open`, receives `"unlocked"`, and prints it beside the new dictionary state. The next print makes the overlay idea explicit.

This is separation of concerns in miniature. The function owns the rule. `main` owns this demonstration. The terrain is not rebuilt because the connection already exists; only access state changes.

## Complete Checkpoint Walkthrough

Run the checkpoint. The door starts locked. The first condition is false because its state is not open. The inventory contains `"gold"`, so validation succeeds. One gold string is removed, the state becomes open, and the return value is `"unlocked"`. The printed result is:

```text
unlocked open
Terrain remains unchanged; only the door overlay changed.
```

At the end, the inventory is empty even though the checkpoint does not print it. If you inspect it, you will see that the key was consumed. If you call `try_open` again, it returns `"already open"` and does not try to consume anything.

## Common Mistakes

- Removing the key before checking membership makes a failed attempt lose a key.
- Checking the key but forgetting `door["state"] = "open"` reports success without changing state.
- Comparing `"Open"` with `"open"` fails because strings are case-sensitive.
- Printing inside the rule makes it harder to reuse the result in a menu or test.
- Mutating a separate copied dictionary leaves the real door locked.
- Treating the dictionary label `"key"` as if it were the inventory list itself causes confusion.

## Fun Side Quests

1. Change the inventory to `[]` and predict the result before running it.
2. Call `try_open` twice and print the inventory after each call.
3. Add a silver door that requires `"silver"`; test gold, silver, and no key separately.
4. Return a different message for a missing key, but keep the same validation order.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/10_doors_keys.py
```

Expected result:

```text
unlocked open
Terrain remains unchanged; only the door overlay changed.
```

## Learner Questions

- Why should an already-open door not consume a key?
- Which exact line mutates the door state?
- Why is returning a status more reusable than printing from `try_open`?
- What should happen if a player has two matching keys?

## What To Remember

State is the current situation. A state transition should validate first and mutate second. `try_open` changes only the door overlay and inventory resource, leaving terrain concerns separate.

## Exact Reference Game Comparison

The reference game defines a richer `Door` dataclass in `game/doors.py`. Its `locked` attribute is state, `can_open` validates inventory, and `open` consumes one matching key before setting `locked = False`. The reference uses key items with `kind` and `key_id` fields from `game/items.py`, rather than plain strings. `game/game_state.py` stores doors in a dictionary keyed by graph edge position. The checkpoint compresses these responsibilities into one dictionary and one function, but its validate, consume, and mutate sequence is the same.
