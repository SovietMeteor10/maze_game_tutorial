"""Geometry and display constants for the first game slice."""

TILE_WIDTH = 26
TILE_HEIGHT = 9

TOP_WALL_HEIGHT = 1
BOTTOM_WALL_HEIGHT = 1
LEFT_WALL_WIDTH = 2
RIGHT_WALL_WIDTH = 2

NORTH_SOUTH_OPENING_WIDTH = 10
EAST_WEST_OPENING_HEIGHT = 5

PLAYER_SYMBOL = "@"
EXIT_SYMBOL = "E"
WALL_SYMBOL = "#"
FLOOR_SYMBOL = " "

# Terminal glyphs are approximately twice as tall as they are wide.
CHARACTER_HEIGHT_TO_WIDTH = 2.0
HORIZONTAL_MOVE_STEPS = max(1, round(CHARACTER_HEIGHT_TO_WIDTH))
