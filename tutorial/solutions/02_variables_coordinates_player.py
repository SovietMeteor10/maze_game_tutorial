"""Lesson 02 model answer: draw a player at x, y coordinates."""

# MODEL ANSWER
ROOM = ["+--------+", "|        |", "|        |", "|        |", "+--------+"]


def draw(x, y):
    """Return a copy of ROOM with the player marker at x, y."""
    picture = [list(row) for row in ROOM]
    picture[y][x] = "@"
    return "\n".join("".join(row) for row in picture)


def main():
    x, y = 4, 2
    print(draw(x, y))
    print("The player is at x={}, y={}.".format(x, y))


if __name__ == "__main__":
    main()
