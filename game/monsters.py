"""Simple monsters used by the exploration game."""

from dataclasses import dataclass


@dataclass
class Snake:
    """A snake that moves toward the player every other player turn."""

    x: int
    y: int
    tile_x: int
    tile_y: int
    tail: list[tuple[int, int, int, int]]
    max_tail_length: int = 4
    hp: int = 10
    patrol_index: int = 0
    symbol: str = "s"
    head_symbol: str = "S"
    speed: float = 1.0
    is_boss: bool = False
    is_boss_minion: bool = False
    is_subboss: bool = False
    movement_progress: float = 0.0
    spawn_timer: int = 0
    boss_direction: tuple[int, int] | None = None
    boss_direction_moves: int = 0
    boss_route: list[tuple[int, int]] | None = None
    boss_route_index: int = 0
    boss_route_direction: int = 1

    @property
    def tail_length(self) -> int:
        return len(self.tail)

    @property
    def position(self) -> tuple[int, int, int, int]:
        return self.tile_x, self.tile_y, self.x, self.y
