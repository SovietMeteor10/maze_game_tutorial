"""Mutable gameplay state shared by game rules and rendering."""

from dataclasses import dataclass, field

from .doors import Door
from .items import Item
from .grenades import Explosion, Grenade
from .monsters import Snake
from .obstacles import Obstacle
from .player import Player
from .secrets import SecretWall
from .world import WorldMap


@dataclass
class GameState:
    """The parts of a game that change while the player explores."""

    player: Player
    world: WorldMap
    items: list[Item] = field(default_factory=list)
    obstacles: set[Obstacle] = field(default_factory=set)
    monsters: list[Snake] = field(default_factory=list)
    grenades: list[Grenade] = field(default_factory=list)
    explosions: list[Explosion] = field(default_factory=list)
    doors: dict[tuple[int, int, str], Door] = field(default_factory=dict)
    secret_walls: dict[tuple[int, int, str], SecretWall] = field(default_factory=dict)
    trophy_tile: tuple[int, int] | None = None
    trophy_position: tuple[int, int] | None = None
    trophy_collected: bool = False
    won: bool = False
    defeated: bool = False
    quit: bool = False
    altar_slots: dict[str, Item] = field(default_factory=dict)
    altar_key_placed: bool = False
    altar_position: tuple[int, int] = (13, 4)
    altar_tile: tuple[int, int] = (5, 4)
    kneeling: bool = False
    summon_prompt: bool = False
    summon_animation_frames: int = 0
    shrine_tiles: set[tuple[int, int]] = field(default_factory=set)
    shrine_center: tuple[int, int] = (5, 5)
    shrine_room_size: tuple[int, int] = (3, 3)
    boss_tiles: set[tuple[int, int]] = field(default_factory=set)
    boss_room_size: tuple[int, int] | None = None
    boss_center: tuple[int, int] | None = None
    boss_active: bool = False
    boss_defeated: bool = False
    boss_split: bool = False
    boss_pickup_timer: int = 0

    @property
    def discovered(self) -> set[tuple[int, int]]:
        """Return the tiles revealed during exploration."""
        return self.world.discovered

    @property
    def progression(self) -> dict[str, bool]:
        """Return named progression flags for menus and future save files."""
        return {
            "trophy_collected": self.trophy_collected,
            "won": self.won,
            "altar_filled": self.altar_key_placed and len(self.altar_slots) == 5,
            "boss_active": self.boss_active,
            "boss_defeated": self.boss_defeated,
        }
