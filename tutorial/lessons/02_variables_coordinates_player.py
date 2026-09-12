"""Lesson 02 exercise: store and draw a player position."""

# WORKED EXAMPLE: a grid uses picture[y][x], because rows come before columns.

ROOM = ["+--------+", "|        |", "|        |", "|        |", "+--------+"]


def draw(x, y):
    """Return a copy of ROOM with the player marker at x, y."""
    # TODO: Keep ROOM unchanged while putting @ in the copied picture.
    picture = [list(row) for row in ROOM]
    picture[y][x] = "@"
    return "\n".join("".join(row) for row in picture)


def main():
    # TODO: Try several valid x and y values and predict the marker position.
    x, y = 4, 2
    print(draw(x, y))
    print("The player is at x={}, y={}.".format(x, y))


if __name__ == "__main__":
    main()
