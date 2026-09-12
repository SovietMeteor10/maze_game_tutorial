"""Player state and movement coordinates."""

from dataclasses import dataclass, field


@dataclass
class Player:
    x: int
    y: int
    tile_x: int = 5
    tile_y: int = 5
    inventory: list = field(default_factory=list)
    max_hp: int = 20
    hp: int = 20
    grenades: int = 0
    holy_grenades: int = 0
