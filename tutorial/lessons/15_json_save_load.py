"""Lesson 15 exercise: serialize, validate, and restore a small game state.

JSON is a readable persistence format.  Keep file I/O at the edge and pass
plain dictionaries through the save/load boundary.
"""

import json


# WORKED EXAMPLE:
# text = json.dumps({"health": 8})
# restored = json.loads(text)
# The round trip changes data to text and back again.


def new_state():
    """Return JSON-friendly game state."""
    return {"position": [2, 1], "health": 8, "inventory": ["gold"], "seed": 7}


def serialize_state(state):
    """Return deterministic JSON text for state."""
    # TODO: Convert the dictionary to JSON text with sorted keys.
    return json.dumps(state, sort_keys=True)


def validate_save(data):
    """Return True when loaded data has the expected safe shape."""
    # TODO: Check the dictionary, position, health, inventory, and seed.
    return (
        isinstance(data, dict)
        and isinstance(data.get("position"), list)
        and len(data["position"]) == 2
        and all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in data["position"]
        )
        and isinstance(data.get("health"), int)
        and not isinstance(data["health"], bool)
        and 0 <= data["health"] <= 20
        and isinstance(data.get("inventory"), list)
        and all(isinstance(item, str) for item in data["inventory"])
        and isinstance(data.get("seed"), int)
    )


def deserialize_state(text):
    """Parse JSON and reject data that does not match the save schema."""
    # TODO: Load first, validate second, and return only validated data.
    data = json.loads(text)
    if not validate_save(data):
        raise ValueError("invalid save data")
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
