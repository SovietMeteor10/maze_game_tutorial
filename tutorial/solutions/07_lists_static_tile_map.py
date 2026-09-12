"""Lesson 07 model answer: compose a static map from tile fragments."""

# MODEL ANSWER
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
    return "\n".join("".join(row) for row in tile_map)


def map_dimensions(tile_map):
    """Return the number of rows and columns in a rectangular map."""
    if not tile_map:
        return 0, 0
    columns = len(tile_map[0])
    if any(len(row) != columns for row in tile_map):
        raise ValueError("map must be rectangular")
    return len(tile_map), columns


def main():
    print(render_map(MAP))
    rows, columns = map_dimensions(MAP)
    print("The map has {} rows and {} columns.".format(rows, columns))


if __name__ == "__main__":
    main()
