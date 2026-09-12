"""Room geometry for the first static game area."""

from .constants import (
    EAST_WEST_OPENING_HEIGHT,
    NORTH_SOUTH_OPENING_WIDTH,
    TILE_HEIGHT,
    TILE_WIDTH,
    WALL_SYMBOL,
)


def opening_bounds() -> tuple[int, int, int, int]:
    """Return the centred opening bounds as left, right, top, bottom."""
    opening_left = (TILE_WIDTH - NORTH_SOUTH_OPENING_WIDTH) // 2
    opening_right = opening_left + NORTH_SOUTH_OPENING_WIDTH
    opening_top = (TILE_HEIGHT - EAST_WEST_OPENING_HEIGHT) // 2
    opening_bottom = opening_top + EAST_WEST_OPENING_HEIGHT
    return opening_left, opening_right, opening_top, opening_bottom


def build_room() -> list[list[str]]:
    """Build a room with centred openings on all four sides."""
    from .tiles import room_for_openings

    return room_for_openings({"N", "E", "S", "W"}).render()


def is_floor(room: list[list[str]], x: int, y: int) -> bool:
    """Return whether a coordinate can be occupied by an entity."""
    if not (0 <= y < len(room) and 0 <= x < len(room[y])):
        return False
    return room[y][x] != WALL_SYMBOL
