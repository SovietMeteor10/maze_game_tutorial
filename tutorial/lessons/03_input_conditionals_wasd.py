"""Lesson 03 exercise: move a player with WASD and safe boundaries."""

import sys

# WORKED EXAMPLE: move(1, 1, "d") returns (2, 1), while an unknown command waits.

WIDTH, HEIGHT = 10, 5


def move(x, y, command):
    """Return the next position, clamped inside the room."""
    # TODO: Add or explain the horizontal and vertical command rules.
    dx = {"a": -1, "d": 1}.get(command, 0)
    dy = {"w": -1, "s": 1}.get(command, 0)
    return max(1, min(WIDTH - 2, x + dx)), max(1, min(HEIGHT - 2, y + dy))


def draw(x, y):
    """Return the room with @ at x, y."""
    # TODO: Change the floor character and observe what stays the same.
    return "\n".join(
        "#"
        + "".join("@" if (col, row) == (x, y) else "." for col in range(1, WIDTH - 1))
        + "#"
        for row in range(HEIGHT)
    )


def main():
    # The scripted route makes this exercise runnable without blocking.
    commands = list(input("WASD (or q): ") if "--play" in sys.argv else "ddssaaw")
    x, y = 1, 1
    for command in commands:
        # TODO: Decide whether q should quit before movement.
        if command == "q":
            break
        x, y = move(x, y, command.lower())
    print(draw(x, y))
    print("Final position:", x, y)


if __name__ == "__main__":
    main()
