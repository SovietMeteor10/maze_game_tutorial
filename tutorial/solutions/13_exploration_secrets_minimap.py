"""MODEL ANSWER: Lesson 13 exploration, secrets, and a minimap.

Discovery is state: it records what the player knows.  Rendering is derived
from that state and leaves the underlying terrain alone.
"""


def new_exploration():
    """Return known coordinates and one coordinate hidden by fog of war."""
    return {(1, 1), (2, 1)}, (3, 1)


def reveal_secret(discovered, secret):
    """Add a secret to the set and report whether this search changed state."""
    if secret in discovered:
        return False
    discovered.add(secret)
    return True


def render_minimap(discovered, x_values, y=1):
    """Render a read-only view of known and unknown positions."""
    symbols = []
    for x in x_values:
        # The secret is an overlay on the world, not a replacement for terrain.
        symbols.append("." if (x, y) in discovered else "?")
    return " ".join(symbols)


def main():
    discovered, secret = new_exploration()
    print("Before search:", render_minimap(discovered, range(1, 4)))
    if reveal_secret(discovered, secret):
        print("A secret wall is found.")
    print("Minimap:", render_minimap(discovered, range(1, 4)))


if __name__ == "__main__":
    main()
