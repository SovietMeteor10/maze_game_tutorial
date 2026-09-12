"""Lesson 06 exercise: use loops and strings to render one ASCII tile."""

# WORKED EXAMPLE: range(3) produces 0, 1, and 2, not 3.
# numbers = []
# for number in range(3):
#     numbers.append(str(number))
# print("-".join(numbers))


def render(openings):
    """Return a five-row tile whose edges match openings."""
    rows = [
        list("+-----+"),
        list("|     |"),
        list("|     |"),
        list("|     |"),
        list("+-----+"),
    ]
    # TODO: open the middle cell of each requested edge.
    if "N" in openings:
        rows[0][3] = " "
    if "S" in openings:
        rows[4][3] = " "
    if "W" in openings:
        rows[2][0] = " "
    if "E" in openings:
        rows[2][6] = " "
    return "\n".join("".join(row) for row in rows)


def main():
    # TODO: render a north-only dead end as another experiment.
    print(render({"E", "W"}))
    print(render({"N", "E", "S", "W"}))


if __name__ == "__main__":
    main()
