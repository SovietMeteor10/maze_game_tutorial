"""Lesson 01 exercise: print a small, fixed ASCII room."""

# WORKED EXAMPLE: "\n".join(["top", "bottom"]) makes two printed rows.

# TODO: Try changing one of the spaces or border characters, then run the file.
ROOM = [
    "+------------------------+",
    "|                        |",
    "|                        |",
    "|                        |",
    "|                        |",
    "|                        |",
    "|                        |",
    "|                        |",
    "+------------------------+",
]


def main():
    """Print the starter room and check its dimensions."""
    # TODO: Add a title of your own before the room.
    print("Static room exercise")
    print("\n".join(ROOM))
    # TODO: Explain what each part of this assertion checks.
    assert len(ROOM) == 9 and all(len(row) == 26 for row in ROOM)


if __name__ == "__main__":
    main()
