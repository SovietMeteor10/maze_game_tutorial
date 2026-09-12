"""Secret-wall overlays for hidden graph-connected rooms."""

from dataclasses import dataclass

from .doors import DELTA, OPPOSITE, edge_key


@dataclass
class SecretWall:
    """An undiscovered wall hiding an existing connection."""

    tile_x: int
    tile_y: int
    direction: str
    found: bool = False

    def __post_init__(self) -> None:
        if self.direction not in DELTA:
            raise ValueError(f"Unknown direction: {self.direction}")

    @property
    def position(self) -> tuple[int, int, str]:
        return edge_key(self.tile_x, self.tile_y, self.direction)

    @property
    def hidden_tile(self) -> tuple[int, int]:
        dx, dy = DELTA[self.direction]
        return self.tile_x + dx, self.tile_y + dy

    @property
    def opposite_direction(self) -> str:
        return OPPOSITE[self.direction]
