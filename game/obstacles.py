"""Solid room-floor obstacles that do not alter the world graph."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Obstacle:
    """An impassable X marker at a local floor coordinate."""

    tile_x: int
    tile_y: int
    x: int
    y: int

    @property
    def position(self) -> tuple[int, int, int, int]:
        return self.tile_x, self.tile_y, self.x, self.y
