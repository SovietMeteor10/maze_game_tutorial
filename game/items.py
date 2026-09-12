"""Collectible items that exist separately from the dungeon terrain."""

from dataclasses import dataclass


ITEM_SYMBOLS = {
    "key": "K",
    "potion": "!",
    "treasure": "$",
    "grenade_pouch": "=",
    "relic": "R",
    "holy_grenade": "H",
}

RELIC_NAMES = ("Amulet", "Spear", "Shield", "Book of the Dead", "Snake Skull")


@dataclass
class Item:
    """An item at a local floor position inside a world tile."""

    x: int
    y: int
    name: str
    kind: str
    tile_x: int = 5
    tile_y: int = 5
    symbol: str | None = None
    key_id: str | None = None
    quantity: int = 1

    def __post_init__(self) -> None:
        if self.kind not in ITEM_SYMBOLS:
            raise ValueError(f"Unknown item kind: {self.kind}")
        if self.kind == "key" and self.key_id is None:
            self.key_id = self.name.lower().replace(" ", "_")
        if self.symbol is None:
            self.symbol = ITEM_SYMBOLS[self.kind]

    @property
    def position(self) -> tuple[int, int, int, int]:
        """Return world tile and local floor coordinates as one value."""
        return self.tile_x, self.tile_y, self.x, self.y
