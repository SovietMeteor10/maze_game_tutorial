"""Tile data, geometry classification, and large ASCII tile rendering."""

from dataclasses import dataclass
from itertools import combinations

from .constants import (
    BOTTOM_WALL_HEIGHT,
    EAST_WEST_OPENING_HEIGHT,
    FLOOR_SYMBOL,
    LEFT_WALL_WIDTH,
    NORTH_SOUTH_OPENING_WIDTH,
    RIGHT_WALL_WIDTH,
    TILE_HEIGHT,
    TILE_WIDTH,
    TOP_WALL_HEIGHT,
    WALL_SYMBOL,
)

DIRECTIONS = ("N", "E", "S", "W")
OPPOSITE_PAIRS = ({"N", "S"}, {"E", "W"})


@dataclass(frozen=True)
class Tile:
    """A tile with a visual kind and compatible cardinal openings."""

    kind: str
    openings: frozenset[str]

    def is_open(self, direction: str) -> bool:
        return direction in self.openings

    def render(self) -> list[list[str]]:
        """Render the tile using shared dimensions and opening geometry."""
        if self.kind == "room":
            rows = [[FLOOR_SYMBOL] * TILE_WIDTH for _ in range(TILE_HEIGHT)]
            self._add_room_walls(rows)
        else:
            rows = [[WALL_SYMBOL] * TILE_WIDTH for _ in range(TILE_HEIGHT)]
            self._carve_corridor(rows)

        assert len(rows) == TILE_HEIGHT
        assert all(len(row) == TILE_WIDTH for row in rows)
        return rows

    def _add_room_walls(self, rows: list[list[str]]) -> None:
        opening_left, opening_right, opening_top, opening_bottom = _opening_bounds()
        for x in range(TILE_WIDTH):
            if not self.is_open("N") or not opening_left <= x < opening_right:
                for y in range(TOP_WALL_HEIGHT):
                    rows[y][x] = WALL_SYMBOL
            if not self.is_open("S") or not opening_left <= x < opening_right:
                for y in range(TILE_HEIGHT - BOTTOM_WALL_HEIGHT, TILE_HEIGHT):
                    rows[y][x] = WALL_SYMBOL
        for y in range(TILE_HEIGHT):
            if not self.is_open("W") or not opening_top <= y < opening_bottom:
                for x in range(LEFT_WALL_WIDTH):
                    rows[y][x] = WALL_SYMBOL
            if not self.is_open("E") or not opening_top <= y < opening_bottom:
                for x in range(TILE_WIDTH - RIGHT_WALL_WIDTH, TILE_WIDTH):
                    rows[y][x] = WALL_SYMBOL

    def _carve_corridor(self, rows: list[list[str]]) -> None:
        opening_left, opening_right, opening_top, opening_bottom = _opening_bounds()
        if self.is_open("N") or self.is_open("S"):
            for y in range(TILE_HEIGHT):
                for x in range(opening_left, opening_right):
                    rows[y][x] = FLOOR_SYMBOL
            if not self.is_open("N"):
                for y in range(TOP_WALL_HEIGHT):
                    for x in range(opening_left, opening_right):
                        rows[y][x] = WALL_SYMBOL
            if not self.is_open("S"):
                for y in range(TILE_HEIGHT - BOTTOM_WALL_HEIGHT, TILE_HEIGHT):
                    for x in range(opening_left, opening_right):
                        rows[y][x] = WALL_SYMBOL
        if self.is_open("E") or self.is_open("W"):
            for y in range(opening_top, opening_bottom):
                for x in range(TILE_WIDTH):
                    rows[y][x] = FLOOR_SYMBOL
            if not self.is_open("W"):
                for y in range(opening_top, opening_bottom):
                    for x in range(LEFT_WALL_WIDTH):
                        rows[y][x] = WALL_SYMBOL
            if not self.is_open("E"):
                for y in range(opening_top, opening_bottom):
                    for x in range(TILE_WIDTH - RIGHT_WALL_WIDTH, TILE_WIDTH):
                        rows[y][x] = WALL_SYMBOL


def _opening_bounds() -> tuple[int, int, int, int]:
    opening_left = (TILE_WIDTH - NORTH_SOUTH_OPENING_WIDTH) // 2
    opening_right = opening_left + NORTH_SOUTH_OPENING_WIDTH
    opening_top = (TILE_HEIGHT - EAST_WEST_OPENING_HEIGHT) // 2
    opening_bottom = opening_top + EAST_WEST_OPENING_HEIGHT
    return opening_left, opening_right, opening_top, opening_bottom


def opening_cells(direction: str) -> tuple[tuple[int, int], ...]:
    """Return the exact boundary cells used by an opening direction."""
    opening_left, opening_right, opening_top, opening_bottom = _opening_bounds()
    if direction == "N":
        return tuple((x, 0) for x in range(opening_left, opening_right))
    if direction == "S":
        return tuple((x, TILE_HEIGHT - 1) for x in range(opening_left, opening_right))
    if direction == "W":
        return tuple((0, y) for y in range(opening_top, opening_bottom))
    if direction == "E":
        return tuple((TILE_WIDTH - 1, y) for y in range(opening_top, opening_bottom))
    raise ValueError(f"Unknown direction: {direction}")


OPENING_CELLS = {direction: opening_cells(direction) for direction in DIRECTIONS}


def classify_openings(openings: set[str] | frozenset[str]) -> str:
    """Return the standard tile kind for an opening combination."""
    opening_set = frozenset(openings)
    count = len(opening_set)
    if count <= 1:
        return "dead_end"
    if count == 2:
        return "straight" if opening_set in OPPOSITE_PAIRS else "corner"
    if count == 3:
        return "t_junction"
    if count == 4:
        return "cross"
    raise ValueError("A tile cannot have more than four openings")


def room_for_openings(
    openings: set[str] | frozenset[str],
    kind: str | None = None,
) -> Tile:
    """Create a room or classified tile for a validated opening set."""
    invalid = set(openings) - set(DIRECTIONS)
    if invalid:
        raise ValueError(f"Unknown directions: {sorted(invalid)}")
    return Tile(kind or "room", frozenset(openings))


def build_tile_catalogue() -> dict[str, list[Tile]]:
    """Build every opening combination for rooms and standard tile kinds."""
    catalogue = {"room": []}
    for size in range(5):
        for opening_tuple in combinations(DIRECTIONS, size):
            openings = frozenset(opening_tuple)
            kind = classify_openings(openings)
            catalogue.setdefault(kind, []).append(Tile(kind, openings))
            catalogue["room"].append(Tile("room", openings))
    return catalogue


TILE_CATALOGUE = build_tile_catalogue()
