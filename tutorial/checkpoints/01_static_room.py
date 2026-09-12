"""Checkpoint 01: print one fixed ASCII room."""

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
    print("Static room")
    print("\n".join(ROOM))
    assert len(ROOM) == 9 and all(len(line) == 26 for line in ROOM)


if __name__ == "__main__":
    main()
