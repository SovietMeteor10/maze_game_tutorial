"""Lesson 13 exercise: remember discovered coordinates and draw a minimap.

State is the information the game remembers.  The minimap is a view derived
from that state, so drawing it does not need to change the world.
"""


# WORKED EXAMPLE:
# discovered = {(1, 1), (2, 1)}
# discovered.add((3, 1))
# "in" checks membership, and a set keeps each coordinate only once.


def new_exploration():
    """Return the starter discovery state and the hidden coordinate."""
    return {(1, 1), (2, 1)}, (3, 1)


def reveal_secret(discovered, secret):
    """Reveal a secret coordinate and return whether it was newly found."""
    # TODO: Check membership and add the secret when it is not known.
    was_new = secret not in discovered
    discovered.add(secret)
    return was_new


def render_minimap(discovered, x_values, y=1):
    """Return dots for known coordinates and question marks for unknown ones."""
    # TODO: Build the row with a loop or a generator expression.
    return " ".join("." if (x, y) in discovered else "?" for x in x_values)


def main():
    discovered, secret = new_exploration()
    print("Before search:", render_minimap(discovered, range(1, 4)))
    if reveal_secret(discovered, secret):
        print("A secret wall is found.")
    print("Minimap:", render_minimap(discovered, range(1, 4)))


if __name__ == "__main__":
    main()
