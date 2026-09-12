"""Checkpoint 13: discovery reveals a secret and updates a minimap."""


def main():
    discovered = {(1, 1), (2, 1)}
    secret = (3, 1)
    print("Before search: . . ?")
    if secret not in discovered:
        print("A secret wall is found.")
        discovered.add(secret)
    print(
        "Minimap:", " ".join("." if (x, 1) in discovered else "?" for x in range(1, 4))
    )


if __name__ == "__main__":
    main()
