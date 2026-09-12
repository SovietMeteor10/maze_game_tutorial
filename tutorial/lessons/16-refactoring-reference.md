# 16: Refactoring And Comparison

**Coding exercise:** `16_refactoring_reference.py` | **Model answer:** `../solutions/16_refactoring_reference.py`

## What You Will Build

You will finish with a tiny architecture containing three clear pieces: a
plain state dictionary, a movement function, and a renderer. The checkpoint is
`tutorial/checkpoints/16_refactored_game.py`. It creates state with
`new_state()`, moves the player with `move()`, renders text with `render()`,
and prints a short explanation.

This is not a demand to split every five lines into a new file. Refactoring
means improving an existing program's shape without changing its intended
behavior. You will learn to introduce boundaries when they make the code easier
to read, test, and extend.

## Learning Goals

- Define modularity, cohesion, and coupling in practical terms.
- Separate state, rules, and rendering.
- Understand abstraction and reusability.
- Improve interpretability and testability.
- Recognize when duplication or confusion calls for refactoring.
- Compare the small checkpoint with the full reference game.

## New Words

- **Refactoring:** changing code structure while preserving its behavior.
- **Modularity:** organizing a program into understandable parts with clear
  boundaries.
- **Cohesion:** how closely the responsibilities inside one part belong
  together. High cohesion is usually good.
- **Coupling:** how much one part depends on the details of another. Lower
  unnecessary coupling is usually easier to change.
- **Abstraction:** a simple interface that hides details not needed by its user.
- **Reusability:** the ability to use a function or module in another context.
- **Interpretability:** how readily a human can understand what code and data
  mean.
- **Testability:** how easily behavior can be checked with a small, repeatable
  test.
- **Single responsibility:** a part has one main reason to change.

## Why This Matters

An early game can put input, movement, drawing, and rules in one loop. That is
fine while the program is tiny. As features arrive, the loop becomes difficult
to understand: changing a wall symbol might accidentally change collision, or
testing movement might require a real terminal.

The answer is not abstraction for its own sake. A boundary is useful when it
reduces confusion. In the checkpoint, `move(state, "d")` can be tested without
printing. `render(state)` can be tested without changing the player. This gives
high cohesion inside each function and less coupling between game rules and
terminal output.

## Tiny Example, Line by Line

```python
    return {"player": [1, 1], "health": 3,
            "map": ["#####", "#...#", "#####"]}
```

`new_state()` is a factory function, a small abstraction for creating a valid
starting state. The dictionary holds data only. The map is terrain; the player
position and health are entity state. Returning a fresh dictionary each time
prevents one test run from sharing mutations with another.

```python
    x, y = state["player"]
    dx, dy = {"d": (1, 0), "a": (-1, 0),
              "w": (0, -1), "s": (0, 1)}[direction]
    if state["map"][y + dy][x + dx] == ".":
        state["player"] = [x + dx, y + dy]
```

The function reads position, translates a direction into a coordinate change,
checks the destination, and updates state only for floor. It does not print.
That makes the rule reusable from a terminal loop, a test, or a future graphical
front end.

## Guided Build: Tie It To The Checkpoint

Read `tutorial/checkpoints/16_refactored_game.py` from top to bottom. Start with
`new_state()`. Then call `move(state, "d")`. The player begins at `[1, 1]`, and
the cell to the right is floor, so the position becomes `[2, 1]`.

The `render()` function uses nested generator expressions. For each row, it
checks each coordinate. If `[x, y] == state["player"]`, it emits `@`; otherwise
it emits the original cell. `"\n".join(...)` combines the rows. Rendering
reads state but does not modify it, which is a valuable rule.

If the compact expression is hard to read, rewrite it with ordinary `for`
loops first. That is not a step backward. Readability is part of
interpretability, and a clear longer version can be the better abstraction for
a beginner.

## Complete Checkpoint Walkthrough

`new_state()` returns:

```text
player = [1, 1]
health = 3
map = ["#####", "#...#", "#####"]
```

`move(state, "d")` looks up `("d": (1, 0))`. The destination is x 2, y 1.
Because `state["map"][1][2]` is `.`, the player changes to `[2, 1]`.
`render()` walks the three rows. It replaces the floor at x 2, y 1 with `@`.
The screen output is:

```text
#####
#.@.#
#####
Final state is data; movement and rendering are separate functions.
```

The important result is not the map art. It is the boundary: state is data,
movement is a rule, and rendering is a view.

## Cohesion, Coupling, And Reusability In Practice

The movement function has high cohesion because its work is about moving. If it
also printed menus, wrote save files, and spawned monsters, it would have many
reasons to change. That would lower cohesion. The renderer is cohesive because
it turns state into display text.

Coupling is the dependency between parts. `move()` is coupled to the state
keys `player` and `map`, but not to a terminal library. That is reasonable,
small coupling. `render()` depends on the same state shape, which is an
intentional shared interface. A future module can reuse `move()` with scripted
commands because it does not need to imitate keyboard input.

## Common Mistakes

- Moving the player inside `render()`, which makes drawing unexpectedly change
  the game.
- Printing inside `move()`, which makes automated tests inspect terminal text.
- Copying the map into a second variable and letting the copies drift apart.
- Splitting every statement into a module before the responsibilities are clear.
- Calling the data dictionary an abstraction while hiding its keys from the
  reader. An abstraction should simplify, not obscure.
- Forgetting that `map[y][x]` uses row first and column second.

## Side Quests

1. Write a test-like assertion: create `new_state()`, call `move(state, "d")`,
   and assert the position is `[2, 1]`.
2. Add a blocked move into `#` and prove the player does not move.
3. Extract `can_move(state, x, y)` as a reusable rule, then ask whether this
   abstraction makes the code clearer or merely longer.
4. Add an item layer without writing items into the terrain map. Decide how
   `render()` should choose between player, item, floor, and wall.

## Run Command And Expected Result

From the project root, run:

```text
python3 tutorial/checkpoints/16_refactored_game.py
```

Expected result:

```text
#####
#.@.#
#####
Final state is data; movement and rendering are separate functions.
```

## Learner Questions

- Which function can be tested without a terminal?
- Which values are terrain and which are entity state?
- What would become its own module next if the game grew?
- Where is abstraction helping, and where would it be premature?
- How do cohesion and coupling affect future changes?

## Exact Reference Game Comparison

The reference uses more modules because it has more responsibilities. `game/world.py`
owns generated tiles, connections, discovery, viewport rendering, and minimaps.
`game/game_state.py` stores mutable gameplay state. `game/player.py` defines the
player, while `game/monsters.py`, `game/items.py`, `game/doors.py`, and
`game/secrets.py` define separate entity or overlay concepts. `game/game.py`
coordinates gameplay rules, and `game/main.py` plus `game/menu.py` handle the
curses interface and menus. The checkpoint is not a miniature copy of every
module; it demonstrates the same direction of separation in three functions.

## What To Remember

Refactor when a clearer boundary solves a real problem. Keep state as readable
data, put rules in focused functions, and make rendering a read-only view.
Good modularity improves cohesion, reduces unnecessary coupling, supports
reusability, and makes behavior interpretable and testable. The reference game
is a comparison guide, not a structure to copy before you understand the need.
