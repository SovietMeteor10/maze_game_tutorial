"""Checkpoint 15: plain game state can make a JSON save/load round trip."""

import json


def main():
    state = {"position": [2, 1], "health": 8, "inventory": ["gold"], "seed": 7}
    text = json.dumps(state, sort_keys=True)
    restored = json.loads(text)
    assert restored == state
    print("JSON:", text)
    print("Loaded position:", tuple(restored["position"]))


if __name__ == "__main__":
    main()
