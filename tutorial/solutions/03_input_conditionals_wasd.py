"""Lesson 03 model answer: move with WASD and conditionals."""

# MODEL ANSWER
import sys

WIDTH, HEIGHT = 10, 5


def move(x, y, command):
    """Return the next position, clamped inside the room."""
    dx = {"a": -1, "d": 1}.get(command, 0)
    dy = {"w": -1, "s": 1}.get(command, 0)
    return max(1, min(WIDTH - 2, x + dx)), max(1, min(HEIGHT - 2, y + dy))


def draw(x, y):
    """Return the room with @ at x, y."""
    return "\n".join(
        "#"
        + "".join("@" if (col, row) == (x, y) else "." for col in range(1, WIDTH - 1))
        + "#"
        for row in range(HEIGHT)
    )


def main():
    commands = list(input("WASD (or q): ") if "--play" in sys.argv else "ddssaaw")
    x, y = 1, 1
    for command in commands:
        if command == "q":
            break
        x, y = move(x, y, command.lower())
    print(draw(x, y))
    print("Final position:", x, y)


if __name__ == "__main__":
    main()
