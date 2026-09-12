# 04: Functions, Collision, Scope, And The Game Loop

**Coding exercise:** `04_functions_collision_loop.py` | **Model answer:** `../solutions/04_functions_collision_loop.py`

## What You Will Build

You will run `tutorial/checkpoints/04_functions_collision_loop.py`. It moves
the player through a room containing `#` walls and `.` floor. The player can
move only when the destination is floor. A `step` function applies one command,
and a loop applies that function repeatedly. The checkpoint also has `--play`
mode, but its default `ddssaa` route is repeatable.

This lesson turns several useful ideas into separate responsibilities. A
function asks whether a cell is open. Another function calculates one attempted
move. Another draws the result. The main loop connects those parts without
making every part know every other detail.

## Learning Goals

- Define functions with parameters.
- Call functions with arguments.
- Return values instead of hiding changes in global variables.
- Understand local scope.
- Check the destination for a collision.
- Read tuples and unpack them with `*`.
- See a game loop as input, rules, and display repeated in order.

## New Words

- A **parameter** is a named input slot in a function definition.
- An **argument** is the actual value supplied to a parameter.
- **Return** sends a result from a function back to its caller.
- **Scope** is the part of a program where a name can be used.
- A **local variable** is a name created inside a function.
- A **collision** is an attempted contact with something that blocks movement.
- A **game loop** repeatedly handles input, applies rules, and displays state.
- **Modularity** means dividing a program into understandable parts.
- **Pure** describes a function whose result depends on its inputs and which
  does not change hidden outside state.
- A **target** is the destination a move is trying to reach.

## Why This Matters

Without functions, movement, drawing, input, and collision rules tend to become
one long block. A long block may work for a few lines, but it is hard to explain
or test. Small functions give names to ideas. `can_move` answers one question.
`step` applies one movement rule. `draw` creates one display. If drawing breaks,
you can still test `step` with a tuple and a command.

Returning a new position also makes the flow visible. The caller owns the
current state and chooses to store the returned value. No hidden function is
allowed to reach into a global player variable and change it unexpectedly.
That style is especially helpful when later features add doors, items,
obstacles, and monsters.

## Tiny Examples Explained Line By Line

```python
def add(left, right):
    total = left + right
    return total

answer = add(2, 3)
```

The first line defines a function with two parameters. The indented body makes
a local variable named `total`. `return` sends the value to the caller. The
last line calls the function with two arguments and stores the result in
`answer`. Defining `add` did not run it; the call did.

```python
def bump(value):
    value = value + 1
    return value

number = 4
number = bump(number)
```

`value` is local to `bump`. Changing local `value` does not rename or mutate
the caller's `number` automatically. The caller explicitly stores the returned
result back into `number`. This makes the state transition easy to see.

## Guided Build Tied To The Actual Checkpoint

Open `tutorial/checkpoints/04_functions_collision_loop.py`. `ROOM` contains a
border of `#`, open floor as `.`, and a central pair of wall cells. The
`can_move(x, y)` function looks up `ROOM[y][x]` and returns whether that cell is
`.`. Notice that it checks the destination coordinate, not the current one.

The `step(position, command)` function first unpacks the tuple into x and y.
The `change` dictionary translates commands into `(dx, dy)` pairs. Unknown
commands get `(0, 0)`, which means wait. The target is calculated by adding the
change to the current position. `can_move(*target)` uses star unpacking: a
target like `(3, 2)` becomes `can_move(3, 2)`. If the target is floor, `step`
returns it. Otherwise it returns the original position, so the wall blocks the
move.

The `draw` function uses `enumerate` twice. `enumerate(row)` supplies x and the
cell symbol. The outer `enumerate(ROOM)` supplies y and the row. The matching
coordinate becomes `@`; every other cell keeps its original symbol. This is
rendering, not movement: it reads state and builds text.

## Complete Checkpoint Walkthrough

1. Run the checkpoint without options.
2. `main` sets `position = (1, 1)` and chooses `ddssaa`.
3. The loop takes one command at a time.
4. Each command calls `step(position, command)`.
5. `step` creates a target and checks that target with `can_move`.
6. A floor target replaces `position`; a wall target leaves it unchanged.
7. After the loop, `draw(position)` overlays `@` on the room.
8. The final tuple is printed for inspection.

Try `--play` and aim at the central `##`. The reported position stays unchanged
when a target is a wall. Try an unknown letter; it also leaves the position
unchanged. The fixed outer border keeps ordinary commands inside the list, but
the checkpoint does not yet have a separate bounds check before indexing. That
is acceptable for this focused milestone. Later terrain rules can make bounds
and doors explicit.

## Common Mistakes

- Defining a function does not call it.
- Forgetting `return` makes the caller receive `None`.
- Reading `ROOM[x][y]` reverses the grid convention.
- Checking the old position instead of the target allows walking through walls.
- Mutating a global position inside every function creates hidden coupling.
- Forgetting that a tuple is ordered can swap dx and dy.
- A command string in a loop supplies one character per iteration.

## Fun Side Quests

- Add a second interior wall and test it with direct `step` calls.
- Write three calls to `step` and print each returned position.
- Add a `wait` command that deliberately returns the same position.
- Add an assertion that walking into `#` leaves state unchanged.
- Write a tiny test table: command, expected position, and reason.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/04_functions_collision_loop.py
python3 tutorial/checkpoints/04_functions_collision_loop.py --play
```

Expected result: the first command prints a collision-safe room and a final
position. The second prints `Commands (or q): `, waits for a command string,
then prints the room and resulting tuple.

## Learner Questions

- Which function would you test if the final picture were wrong?
- Why is returning a position easier to test than printing a position?
- Why must collision check the target cell?
- What names are local to `step`?
- Is a locked door a terrain rule, an interaction rule, or both?
- Could a slow snail have a game loop with one turn every five seconds?

## What To Remember

Parameters make functions reusable. Returns make results explicit. Local scope
reduces accidental changes. Collision is a rule about the destination. A game
loop is not mysterious: it repeats input, rule application, and display in a
known order.

## Exact Reference Game Comparison

The checkpoint's `can_move` is the small teaching version of
`game/room.py:is_floor` and the floor portion of `game/game.py:Game.can_move_to`.
Its `step` represents the movement decision inside `game/game.py:Game`, while
its `draw` represents the rendering responsibility exposed by
`game/main.py:draw_screen`. The reference game adds world tiles, doors,
obstacles, secret walls, and entity layers, but the boundary remains the same:
terrain is checked, player state is updated, and a renderer displays the
combined state without becoming the movement rule.
