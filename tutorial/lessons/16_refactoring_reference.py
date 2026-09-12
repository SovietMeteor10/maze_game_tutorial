"""Lesson 16 exercise: refactor state, movement, and rendering into boundaries.

Refactoring changes structure without changing intended behavior.  Focused
functions improve modularity, cohesion, reusability, interpretability, and
testability while avoiding unnecessary coupling.
"""


# WORKED EXAMPLE:
# state = new_state()
# move(state, "d")
# print(render(state))
# Movement changes state; rendering only reads it.


def new_state():
    """Create a fresh, readable state dictionary for each run or test."""
    # TODO: Return player, health, and terrain data.
    return {"player": [1, 1], "health": 3, "map": ["#####", "#...#", "#####"]}


def can_move(state, x, y):
    """Return whether a coordinate contains floor."""
    # TODO: Keep collision knowledge in this small reusable rule.
    return state["map"][y][x] == "."


def move(state, direction):
    """Move one step when the direction is valid and the destination is floor."""
    # TODO: Translate WASD, then use can_move before changing state.
    directions = {"d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1)}
    if direction not in directions:
        return False
    x, y = state["player"]
    dx, dy = directions[direction]
    if can_move(state, x + dx, y + dy):
        state["player"] = [x + dx, y + dy]
        return True
    return False


def render(state):
    """Return display text without changing state."""
    # TODO: Draw @ over the player while preserving the terrain.
    return "\n".join(
        "".join(
            "@" if [x, y] == state["player"] else cell for x, cell in enumerate(row)
        )
        for y, row in enumerate(state["map"])
    )


def main():
    state = new_state()
    move(state, "d")
    print(render(state))
    print("Final state is data; movement and rendering are separate functions.")


if __name__ == "__main__":
    main()
