"""Lesson 07 exercise: compose a static map from a list of tile fragments."""

# WORKED EXAMPLE: the first index selects a row, then the second selects a column.
# grid = [["A", "B"], ["C", "D"]]
# print(grid[1][0])

MAP = [
    ["+---+", "     ", "+---+"],
    ["| . |", " . . ", "| . |"],
    ["+---+", "     ", "+---+"],
]


def render_map(tile_map):
    """Join tile fragments into the text shown on screen."""
    # TODO: join each row horizontally, then join the rows vertically.
    return "\n".join("".join(row) for row in tile_map)


def map_dimensions(tile_map):
    """Return the number of rows and columns in a non-empty map."""
    # TODO: protect the rectangular-map invariant before using these lengths.
    return len(tile_map), len(tile_map[0])


def main():
    # TODO: change the center fragment and observe the composed screen.
    print(render_map(MAP))
    rows, columns = map_dimensions(MAP)
    print("The map has {} rows and {} columns.".format(rows, columns))


if __name__ == "__main__":
    main()
