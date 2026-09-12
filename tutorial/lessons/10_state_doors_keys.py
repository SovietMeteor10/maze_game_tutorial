"""Lesson 10 exercise: validate a key before mutating a door's state."""


def try_open(door, inventory):
    """Try to open a door dictionary and return a status word."""
    # State means the current facts, such as "locked" or "open".
    # TODO: Return "already open" without consuming another key.
    # TODO: Check for the required key before changing either object.
    if door["key"] in inventory:
        inventory.remove(door["key"])
        door["state"] = "open"  # This mutates the door overlay in place.
        return "unlocked"
    return "locked"


def main():
    # WORKED EXAMPLE: validation happens before mutation.
    door = {"key": "gold", "state": "locked"}
    inventory = ["gold"]
    print(try_open(door, inventory), door["state"])
    print("Inventory after opening:", inventory)
    print("Terrain remains unchanged; only the door overlay changed.")
    # TODO: Try opening the same door again and observe its state.


if __name__ == "__main__":
    main()
