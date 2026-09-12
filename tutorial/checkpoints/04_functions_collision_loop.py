"""Checkpoint 04: functions make collision and the game loop testable."""

import sys

ROOM = ["########", "#......#", "#..##..#", "#......#", "########"]


def can_move(x, y):
    return ROOM[y][x] == "."


def step(position, command):
    x, y = position
    change = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
    dx, dy = change.get(command, (0, 0))
    target = (x + dx, y + dy)
    return target if can_move(*target) else position


def draw(position):
    return "\n".join(
        "".join("@" if (x, y) == position else cell for x, cell in enumerate(row))
        for y, row in enumerate(ROOM)
    )


def main():
    commands = input("Commands (or q): ") if "--play" in sys.argv else "ddssaa"
    position = (1, 1)
    for command in commands:
        if command == "q":
            break
        position = step(position, command)
    print(draw(position))
    print("Collision-safe position:", position)


if __name__ == "__main__":
    main()
