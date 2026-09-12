# Maze Game Tutorial

Build a small ASCII maze game one idea at a time. The `game/` directory is the
finished reference product; this tutorial is intentionally simpler and keeps
each milestone readable.

## Start here

If this is a fresh computer, read [`../SETUP.md`](../SETUP.md) first.

1. Read `lessons/README.md`.
2. Read lessons in numerical order.
3. Run the matching learner exercise in `lessons/`, for example:

```text
python3 tutorial/lessons/01_printing_static_room.py
```

Make a real attempt at the `TODO` exercises before opening the matching file in
`solutions/`. Then run the checkpoint as a compact milestone:

```text
python3 tutorial/solutions/01_printing_static_room.py
python3 tutorial/checkpoints/01_static_room.py
```

The lesson files are starter exercises, the solution files are model answers,
and the checkpoints are small demonstrations used to verify the progression.
All of them run a short scripted example without waiting for input. A few also
offer `--play` for experimentation. See `lessons/README.md` and
`checkpoints/README.md` for the full lists.

The reference game is launched from the project root with
`python3 -m game.main`. It uses curses and contains the complete product loop;
the tutorial checkpoints use only the Python standard library and plain text.
