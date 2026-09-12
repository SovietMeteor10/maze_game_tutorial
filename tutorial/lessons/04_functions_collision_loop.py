"""Lesson 04 exercise: use functions and collision-safe movement."""

import sys

# WORKED EXAMPLE: step((1, 1), "d") returns a new position, not hidden state.

ROOM = ["########", "#......#", "#..##..#", "#......#", "########"]


def can_move(x, y):
    """Return whether the destination cell is floor."""
    # TODO: Check the destination, not the current player position.
    return ROOM[y][x] == "."


def step(position, command):
    """Apply one command and return the resulting position."""
    # TODO: Add movement deltas and keep blocked moves at position.
    x, y = position
    change = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
    dx, dy = change.get(command, (0, 0))
    target = (x + dx, y + dy)
    return target if can_move(*target) else position


def draw(position):
    """Return ROOM with the player marker overlaid."""
    # TODO: Use enumerate to compare each cell coordinate with position.
    return "\n".join(
        "".join("@" if (x, y) == position else cell for x, cell in enumerate(row))
        for y, row in enumerate(ROOM)
    )


def main():
    commands = input("Commands (or q): ") if "--play" in sys.argv else "ddssaa"
    position = (1, 1)
    for command in commands:
        # TODO: Make q stop the loop without taking a step.
        if command == "q":
            break
        position = step(position, command.lower())
    print(draw(position))
    print("Collision-safe position:", position)


if __name__ == "__main__":
    main()
