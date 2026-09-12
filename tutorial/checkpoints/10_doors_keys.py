"""Checkpoint 10: a door is overlay state, and a key changes that state."""


def try_open(door, inventory):
    if door["state"] == "open":
        return "already open"
    if door["key"] in inventory:
        inventory.remove(door["key"])
        door["state"] = "open"
        return "unlocked"
    return "locked"


def main():
    door = {"key": "gold", "state": "locked"}
    inventory = ["gold"]
    print(try_open(door, inventory), door["state"])
    print("Terrain remains unchanged; only the door overlay changed.")


if __name__ == "__main__":
    main()
