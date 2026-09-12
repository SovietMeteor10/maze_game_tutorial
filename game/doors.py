"""Door overlays that sit on top of existing graph connections."""

from dataclasses import dataclass


DELTA = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


def edge_key(tile_x: int, tile_y: int, direction: str) -> tuple[int, int, str]:
    """Return one stable key for either side of a graph edge."""
    if direction not in DELTA:
        raise ValueError(f"Unknown direction: {direction}")
    dx, dy = DELTA[direction]
    neighbour = (tile_x + dx, tile_y + dy)
    current = (tile_x, tile_y)
    if neighbour < current:
        return neighbour[0], neighbour[1], OPPOSITE[direction]
    return tile_x, tile_y, direction


@dataclass
class Door:
    """A door occupying an already-open connection between two tiles."""

    tile_x: int
    tile_y: int
    direction: str
    key_id: str | None = None
    locked: bool = True

    def __post_init__(self) -> None:
        if self.direction not in DELTA:
            raise ValueError(f"Unknown direction: {self.direction}")

    @property
    def position(self) -> tuple[int, int, str]:
        return edge_key(self.tile_x, self.tile_y, self.direction)

    def can_open(self, inventory) -> bool:
        """Return whether inventory contains this door's required key."""
        if not self.locked:
            return True
        if self.key_id is None:
            return False
        return any(
            item.kind == "key" and item.key_id == self.key_id
            for item in inventory
        )

    def unlock(self, inventory) -> bool:
        """Unlock this door when the player carries its matching key."""
        if not self.can_open(inventory):
            return False
        self.locked = False
        return True

    def open(self, inventory) -> bool:
        """Open the door and consume one matching key."""
        if not self.locked:
            return True
        for index, item in enumerate(inventory):
            if item.kind == "key" and item.key_id == self.key_id:
                del inventory[index]
                self.locked = False
                return True
        return False
