"""Checkpoint 07: a list of lists stores a hand-authored tile map."""

MAP = [
    ["+---+", "     ", "+---+"],
    ["| . |", " . . ", "| . |"],
    ["+---+", "     ", "+---+"],
]


def main():
    print("\n".join("".join(row) for row in MAP))
    print("The map has {} rows and {} columns.".format(len(MAP), len(MAP[0])))


if __name__ == "__main__":
    main()
