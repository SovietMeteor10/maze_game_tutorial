# 03: Input, Conditionals, Booleans, And WASD

**Coding exercise:** `03_input_conditionals_wasd.py` | **Model answer:** `../solutions/03_input_conditionals_wasd.py`

## What You Will Build

You will run `tutorial/checkpoints/03_wasd_conditionals.py`. It moves `@` using
WASD commands, keeps the marker inside the room, and stops when it sees `q`.
The normal run uses the repeatable command sequence `ddssaaw`, so you can test
the program without typing. The `--play` option switches to interactive input.

This is the point where a picture becomes a program. The room responds to an
instruction, but every instruction still follows a small, understandable rule.

## Learning Goals

- Read text with `input`.
- Inspect command-line arguments with `sys.argv`.
- Use `if`, `else`, `for`, and `break`.
- Understand booleans and comparisons.
- Translate a command into a coordinate change.
- Clamp coordinates to the room's inner boundary.
- Give unknown commands a safe behavior.

## New Words

- **Input** is information supplied while a program runs.
- A **conditional** chooses code based on a condition.
- A **boolean** is one of two values: `True` or `False`.
- A **comparison** asks a question, such as `x == 3`.
- A **command-line argument** is text typed after the script name.
- `sys.argv` is Python's list of command-line arguments.
- A **loop** repeats a block of code.
- `break` leaves the nearest loop immediately.
- **Clamping** keeps a value between a minimum and maximum.
- A **command** is a small input instruction, such as `w` or `d`.

## Why This Matters

Input turns a static display into an interactive system. A game is largely a
cycle of receiving information, applying rules, and showing the result. The
rules here are simple: a moves left, d moves right, w moves up, s moves down,
and q quits. The border rule says the player must remain inside the room.

It is useful that movement is a function receiving normal values. Tests can
call `move(3, 2, "d")` without a keyboard. The program can also use a scripted
sequence for a smoke test. Interactive play and repeatable tests use the same
movement rule rather than two separate implementations.

## Tiny Examples Explained Line By Line

```python
answer = input("Name: ")
if answer == "Ada":
    print("Welcome")
else:
    print("Hello")
```

Line 1 displays a prompt and stores the typed text. `input` returns a string.
Line 2 compares that string with `"Ada"`; `==` asks a question while `=`
assigns. The indented line runs only when the comparison is true. `else` covers
every other answer.

```python
inside = 1 <= x <= 8
if not inside:
    print("wall")
```

The chained comparison checks both limits and produces a boolean. `not` changes
true to false or false to true. The second line prints only when the coordinate
is outside the allowed range. Python's chained comparison is read as x is at
least 1 and at most 8.

## Guided Build Tied To The Actual Checkpoint

The checkpoint imports `sys` because `sys.argv` contains the words used to run
the script. In `main`, the expression `"--play" in sys.argv` chooses between
interactive input and the default string `"ddssaaw"`. `list(...)` changes the
chosen string into one command per loop item.

The `move` function uses two small dictionaries. The horizontal dictionary maps
`a` to -1 and `d` to 1. The vertical dictionary maps `w` to -1 and `s` to 1.
`.get(command, 0)` means an unknown command adds zero. The return expression
uses `max` and `min` to keep x between 1 and `WIDTH - 2`, and y between 1 and
`HEIGHT - 2`. The outer wall occupies coordinate 0 and the final coordinate,
so the player is allowed only in the inside cells.

The `draw` function uses nested iteration. The outer `for row in range(HEIGHT)`
creates each row. The inner range creates each inside column. The conditional
expression prints `@` only when `(col, row) == (x, y)` and `.` everywhere else.
In `main`, the loop processes commands in order. It checks for q before calling
`move`, so quitting does not accidentally move the player.

## Complete Checkpoint Walkthrough

1. Run without `--play` to use `ddssaaw`.
2. The player starts at `(1, 1)`.
3. Each command changes one coordinate or leaves it unchanged.
4. The result is clamped before it is returned.
5. The final map is drawn after all commands finish.
6. The final position is printed as extra feedback.

Run with `--play` and type `ddwq`. The player moves right twice, moves up once,
then stops at q. Try `z`: it is an unknown command, so both changes are zero
and the player stays still. Try moving toward an outer wall many times. The
coordinate stops at the inner edge. This checkpoint has no interior obstacles,
so every cell inside the border is walkable.

## Common Mistakes

- Use `==` for comparison and `=` for assignment.
- `input` returns text, even when the user types a number.
- Forgetting a colon after `if`, `for`, or `def` causes a syntax error.
- The loop variable is one command, not the whole input string.
- Checking q after movement makes q perform an unintended move.
- Forgetting `.lower()` makes uppercase W, A, S, and D behave differently.
- Allowing coordinate 0 lets the player overwrite the wall.

## Fun Side Quests

- Add `x` as a second quit command.
- Add `h` to print a help message, then decide whether it should move.
- Make the room wider by changing `WIDTH` and explain both inner bounds.
- Add `.` as a no-op wait command.
- Print every position after each command to watch the state change.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/03_wasd_conditionals.py
python3 tutorial/checkpoints/03_wasd_conditionals.py --play
```

Expected result: the first command prints a room and the final position after
the scripted route. The second prints `WASD (or q): ` and waits for a command
line, then prints the resulting room.

## Learner Questions

- Which expressions in `move` produce booleans?
- What should an unknown key do, and why is staying still safe?
- Why is q checked before movement?
- Is a wall only a picture, or is it also a movement rule?
- Would a mouse click need a different rule, or could it become a command value?

## What To Remember

Input becomes values. Conditionals turn values into choices. A movement
function can translate a command, enforce bounds, and return a new position
without owning the keyboard. Safe defaults make experiments less frightening.

## Exact Reference Game Comparison

The checkpoint's `move` function is the small teaching version of movement in
`game/game.py:Game.handle_key` and `game/game.py:Game.can_move_to`. The reference
game receives real key codes through curses in `game/main.py:run_curses`, while
the checkpoint receives a line of text. The reference also uses
`game/room.py:is_floor` and world openings to decide whether a target is floor.
Both versions translate input, validate a destination, update player state, and
then render it; the reference simply has more world rules and a live terminal.
