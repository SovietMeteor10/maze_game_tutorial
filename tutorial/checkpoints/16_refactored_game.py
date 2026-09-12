"""Checkpoint 16: a tiny final architecture separates state, rules, and rendering."""


def new_state():
    return {"player": [1, 1], "health": 3, "map": ["#####", "#...#", "#####"]}


def move(state, direction):
    x, y = state["player"]
    dx, dy = {"d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1)}[direction]
    if state["map"][y + dy][x + dx] == ".":
        state["player"] = [x + dx, y + dy]


def render(state):
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
