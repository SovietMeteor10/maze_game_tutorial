"""MODEL ANSWER: Lesson 16 refactoring reference.

The state dictionary is the shared, simple abstraction.  Movement has high
cohesion around rules, and rendering has high cohesion around display.  Their
small interface lowers unnecessary coupling and makes both reusable and
testable without a terminal.
"""


def new_state():
    """Create independent state so tests cannot share mutable data."""
    return {"player": [1, 1], "health": 3, "map": ["#####", "#...#", "#####"]}


def can_move(state, x, y):
    """Return whether x, y is an in-bounds floor coordinate."""
    rows = state["map"]
    return 0 <= y < len(rows) and 0 <= x < len(rows[y]) and rows[y][x] == "."


def move(state, direction):
    """Apply one movement rule and report whether state changed."""
    directions = {"d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1)}
    if direction not in directions:
        return False
    x, y = state["player"]
    dx, dy = directions[direction]
    if not can_move(state, x + dx, y + dy):
        return False
    state["player"] = [x + dx, y + dy]
    return True


def render(state):
    """Build a read-only text view from state."""
    rows = []
    player_x, player_y = state["player"]
    for y, row in enumerate(state["map"]):
        rendered_row = []
        for x, cell in enumerate(row):
            rendered_row.append("@" if [x, y] == [player_x, player_y] else cell)
        rows.append("".join(rendered_row))
    return "\n".join(rows)


def main():
    state = new_state()
    move(state, "d")
    print(render(state))
    print("Final state is data; movement and rendering are separate functions.")


if __name__ == "__main__":
    main()
