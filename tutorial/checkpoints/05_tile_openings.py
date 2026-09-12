"""Checkpoint 05: dictionaries describe which sides of a tile are open."""

TILES = {
    "room": {"N", "E", "S", "W"},
    "corridor": {"E", "W"},
    "corner": {"E", "S"},
    "dead_end": {"N"},
}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


def connected(left, right):
    return ("E" in left) == ("W" in right)


def main():
    for name, openings in TILES.items():
        print("{}: {}".format(name, "".join(sorted(openings))))
    assert connected(TILES["corridor"], TILES["corridor"])
    assert not connected(TILES["dead_end"], TILES["corridor"])


if __name__ == "__main__":
    main()
