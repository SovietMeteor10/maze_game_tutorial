"""Checkpoint 08: seeded random growth creates one connected dungeon."""

import random


def make_dungeon(seed, size=7):
    randomizer = random.Random(seed)
    cells = {(size // 2, size // 2)}
    while len(cells) < 12:
        x, y = randomizer.choice(tuple(cells))
        nx, ny = randomizer.choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
        if 0 <= nx < size and 0 <= ny < size:
            cells.add((nx, ny))
    return cells


def main():
    cells = make_dungeon(7)
    for y in range(7):
        print("".join("." if (x, y) in cells else "#" for x in range(7)))
    print("Seed 7 created {} connected cells.".format(len(cells)))


if __name__ == "__main__":
    main()
