"""Checkpoint 06: loops construct a small tile from its openings."""


def render(openings):
    rows = [
        list("+-----+"),
        list("|     |"),
        list("|     |"),
        list("|     |"),
        list("+-----+"),
    ]
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
    print(render({"E", "W"}))
    print(render({"N", "E", "S", "W"}))


if __name__ == "__main__":
    main()
