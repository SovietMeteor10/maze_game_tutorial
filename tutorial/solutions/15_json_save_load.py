"""MODEL ANSWER: Lesson 15 JSON save and load.

Serialization turns plain state into text.  Deserialization restores it, but
validation must happen before the loaded state is trusted by the game.
"""

import json


def new_state():
    return {"position": [2, 1], "health": 8, "inventory": ["gold"], "seed": 7}


def serialize_state(state):
    """Make a predictable JSON representation at the persistence boundary."""
    return json.dumps(state, sort_keys=True)


def validate_save(data):
    """Check the save schema and reject impossible or confusing values."""
    if not isinstance(data, dict):
        return False
    position = data.get("position")
    health = data.get("health")
    inventory = data.get("inventory")
    seed = data.get("seed")

    def is_integer(value):
        return isinstance(value, int) and not isinstance(value, bool)

    return (
        isinstance(position, list)
        and len(position) == 2
        and all(is_integer(value) for value in position)
        and is_integer(health)
        and 0 <= health <= 20
        and isinstance(inventory, list)
        and all(isinstance(item, str) for item in inventory)
        and is_integer(seed)
    )


def deserialize_state(text):
    """Decode and validate JSON before returning it to game code."""
    try:
        data = json.loads(text)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError("save is not valid JSON") from error
    if not validate_save(data):
        raise ValueError("save does not match the expected schema")
    return data


def main():
    state = new_state()
    text = serialize_state(state)
    restored = deserialize_state(text)
    assert restored == state
    print("JSON:", text)
    print("Loaded position:", tuple(restored["position"]))


if __name__ == "__main__":
    main()
