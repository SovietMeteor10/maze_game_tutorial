"""Lesson 05 model answer: describe tile openings with dictionaries and sets."""

# MODEL ANSWER
# WORKED EXAMPLE: a dictionary connects a name to related data.
# door = {"state": "locked", "key": "gold"}
# print(door["state"])

TILES = {
    "room": {"N", "E", "S", "W"},
    "corridor": {"E", "W"},
    "corner": {"E", "S"},
    "dead_end": {"N"},
}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


def connected(left, right):
    """Return whether the east and west sides have matching states."""
    return ("E" in left) == ("W" in right)


def main():
    for name, openings in TILES.items():
        print("{}: {}".format(name, "".join(sorted(openings))))
    assert connected(TILES["corridor"], TILES["corridor"])
    assert not connected(TILES["dead_end"], TILES["corridor"])


if __name__ == "__main__":
    main()
