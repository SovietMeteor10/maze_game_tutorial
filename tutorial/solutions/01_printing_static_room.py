"""Lesson 01 model answer: print a fixed ASCII room."""

# MODEL ANSWER
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
    """Print the room and verify its shape."""
    print("Static room")
    print("\n".join(ROOM))
    assert len(ROOM) == 9 and all(len(row) == 26 for row in ROOM)


if __name__ == "__main__":
    main()
