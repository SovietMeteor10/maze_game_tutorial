"""Lesson 08 model answer: grow a reproducible dungeon from connected cells."""

# MODEL ANSWER
import random

# WORKED EXAMPLE: a seed makes a random choice repeatable.
# coin = random.Random(4)
# print(coin.choice(["heads", "tails"]))


def make_dungeon(seed, size=7):
    """Return twelve in-bounds cells grown from the center."""
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
