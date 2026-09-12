# 01: Printing A Static Room

**Coding exercise:** `01_printing_static_room.py` | **Model answer:** `../solutions/01_printing_static_room.py`

## What You Will Build

You will run `tutorial/checkpoints/01_static_room.py` and print a small room in
the terminal. The room is nine rows high and 26 characters wide. Its border is
made from `+`, `-`, and `|`, while its empty floor is made from spaces. Nothing
moves yet. That is deliberate: before a game can react, it needs a screen.

This first checkpoint is a tiny ASCII game scene. ASCII means ordinary text
characters are used as the picture. A terminal does not need a graphics card to
show a room. It needs rows of characters, printed in the right order. You will
also see a short title above the room and an assertion that checks its shape.

## Learning Goals

- Run a Python file from the project root.
- Recognize strings, lists, variables, and functions.
- Combine a list of rows with `join`.
- Understand why spaces and line lengths are real game data.
- Read an assertion as an automatic safety check.
- Notice that defining a function and calling a function are different actions.

## New Words

- A **program** is a set of instructions that a computer follows.
- A **terminal** is a text-based window where you type commands and see output.
- A **string** is text surrounded by quotes, such as `"maze"`.
- A **list** is an ordered collection written with square brackets.
- A **variable** is a name that refers to a value.
- A **function** is a named recipe for doing a task.
- An **argument** is a value placed inside a function call's parentheses.
- A **method** is an operation attached to a value, such as the string method
  `.join`.
- An **assertion** is a check that stops the program if a condition is false.
- A **newline** is the move to the next output row. In a string, `\n` means a
  newline.
- **ASCII** is a small, widely supported set of text characters. Here it is our
  very simple art material.

## Why This Matters

Every later game feature needs a way to display state. A player, a wall, a key,
and an enemy are only useful to the learner if the program can show them. A
terminal room is like a very small version of a graphical scene: rows are like
screen lines, characters are like tiny tiles, and their positions matter.

Starting with a fixed room also keeps the first problem small. You do not need
input, random numbers, collision rules, or classes to answer one question: can
Python display the map we described? The tradeoff is that this room is not
reusable yet. If you want a different width, you must edit the rows. That
limitation gives us a reason to learn better techniques in later lessons.

## Tiny Examples

```python
name = "Moss"
print("Hello, " + name)
```

Line 1 assigns the string `"Moss"` to the variable `name`. Line 2 calls
`print`, joins two strings with `+`, and sends the result to the terminal. The
quotes mark text. The equals sign assigns; it does not ask a question.

```python
rows = ["top", "bottom"]
picture = "\n".join(rows)
print(picture)
```

Line 1 creates a list containing two strings. Line 2 uses `join`: the string
before `.join`, here `"\n"`, is placed between list items. The result is one
string containing two lines. Line 3 displays it. `join` does not print by
itself.

## Guided Build Tied To The Actual Checkpoint

Open `tutorial/checkpoints/01_static_room.py`. `ROOM` is a list. Each item is
one complete screen row. The first row is `+------------------------+` and
the last row is the same. The middle rows begin and end with `|` and contain
spaces between them. Do not remove a space just because it looks empty: that
space is one cell of the room.

The `main` function is the checkpoint's small plan. First it prints `Static
room`. Next it evaluates `"\n".join(ROOM)` and prints the resulting picture.
Finally, it checks that the list contains nine rows and that every row contains
26 characters. The `all(...)` expression means every row must pass the length
test. If the check succeeds, Python prints nothing for the assertion.

The final two lines are also important. `if __name__ == "__main__":` asks
whether this file is being run directly. If it is, `main()` is called. This
pattern lets a file have a runnable example without forcing that example to run
when another file imports it later.

## Complete Checkpoint Walkthrough

1. Open a terminal.
2. Move to the project root, the folder containing `tutorial`.
3. Run the command in the section below.
4. Python loads the list named `ROOM`.
5. Python defines `main`, then calls it because the file was run directly.
6. The title appears first.
7. The nine room rows appear below the title.
8. The assertion checks the geometry after printing.

You should see a rectangular room with eight interior rows. There is no prompt
because this checkpoint has no input. There is no player because the checkpoint
only teaches representation. If you change one row to have 25 characters, the
room may look almost correct, but the assertion will fail. That failure is
useful: it tells you the map no longer has the promised dimensions.

## Common Mistakes

- Running the command from the wrong folder causes a file-not-found error.
- Forgetting `print` creates a value but does not show it.
- Removing a visible-looking space changes the row width.
- Using a comma where a string needs a closing quote causes a syntax error.
- Mixing tabs and spaces can put a line in the wrong function block.
- Writing `main` without parentheses refers to the function; `main()` calls it.
- Changing only the top border can make the room wider than the other rows.

## Fun Side Quests

- Change the title to `Moss Cavern` without changing the room data.
- Replace one interior space with `@`, `k`, or `!` and invent a meaning.
- Add a tenth row, run the checkpoint, and explain the assertion failure.
- Use `"".join(ROOM)` once and observe why all rows run together.
- Draw a tiny three-row room on paper before editing the list.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/01_static_room.py
```

Expected result: `Static room` followed by a fixed 9-row by 26-character ASCII
room. The program exits normally and prints no assertion message.

## Learner Questions

- Why is one string per row easier to inspect than many `print` calls?
- What does `"".join(ROOM)` do differently from `"\n".join(ROOM)`?
- Why does a space count even though it is hard to see?
- What does the assertion protect, and what does it not protect?
- Why is `main()` at the bottom instead of at the top?

## What To Remember

Text can be a game screen. A list can hold map rows, `join` can combine those
rows, and `print` can display the result. Keep the first representation small
enough that you can count it and check it. A reliable fixed room is a better
starting point than a complicated room that you cannot debug.

## Exact Reference Game Comparison

The checkpoint's `ROOM` list is the simplest ancestor of the reference game's
room data. `game/room.py:build_room` creates a room from reusable tile-opening
data instead of storing one fixed picture. `game/room.py:opening_bounds` keeps
openings centered, and `game/main.py:draw_screen` is the reference game's
display boundary. Both designs turn world data into visible rows, but the
reference game uses calculated geometry and a curses screen rather than one
literal list printed by `print`.
