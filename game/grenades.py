"""Timed grenade and explosion effects."""

from dataclasses import dataclass


@dataclass
class Grenade:
    tile_x: int
    tile_y: int
    x: int
    y: int
    flash: int = 0
    holy: bool = False

    @property
    def position(self) -> tuple[int, int, int, int]:
        return self.tile_x, self.tile_y, self.x, self.y


@dataclass
class Explosion:
    tile_x: int
    tile_y: int
    x: int
    y: int
    remaining: float = 0.35
    holy: bool = False
