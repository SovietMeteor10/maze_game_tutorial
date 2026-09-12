"""Lesson 10 model answer: a key opens a locked door without changing terrain."""


def try_open(door, inventory):
    """Validate, consume one key, and mutate the door state."""
    if door["state"] == "open":
        return "already open"
    if door["key"] not in inventory:
        return "locked"
    inventory.remove(door["key"])
    door["state"] = "open"
    return "unlocked"


def main():
    # MODEL ANSWER
    # A door is an overlay on the map.  Opening it changes door state only.
    door = {"key": "gold", "state": "locked"}
    inventory = ["gold"]
    print(try_open(door, inventory), door["state"])
    print("Inventory after opening:", inventory)
    print("Trying again:", try_open(door, inventory))
    print("Terrain remains unchanged; only the door overlay changed.")


if __name__ == "__main__":
    main()
