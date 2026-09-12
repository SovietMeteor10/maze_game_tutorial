"""Checkpoint 02: put a player at x, y coordinates over a room."""

ROOM = ["+--------+", "|        |", "|        |", "|        |", "+--------+"]


def draw(x, y):
    picture = [list(row) for row in ROOM]
    picture[y][x] = "@"
    return "\n".join("".join(row) for row in picture)


def main():
    x, y = 4, 2
    print(draw(x, y))
    print("The player is at x={}, y={}.".format(x, y))


if __name__ == "__main__":
    main()
