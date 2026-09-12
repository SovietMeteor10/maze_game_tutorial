"""Paused full-screen map and statistics menu."""

from typing import TYPE_CHECKING
from collections import Counter

if TYPE_CHECKING:
    import curses

    from .game import Game


def draw_menu(screen: "curses.window", game: "Game", message: str) -> None:
    """Draw the global map and game statistics inside one screen border."""
    screen.erase()
    height, width = screen.getmaxyx()
    if height < 8 or width < 45:
        screen.addstr(0, 0, "Terminal too small for the menu. Press M to return.")
        screen.refresh()
        return

    _draw_border(screen, height, width)
    screen.addstr(0, 3, " MAZE GAME MENU ")
    screen.addstr(2, 3, "GLOBAL MAP")

    map_left = 3
    map_top = 4
    map_width = max(3, width // 2 - map_left - 2)
    map_size = min(map_width // 3, height - map_top - 4)
    map_size = max(1, map_size)
    map_lines = game.render_minimap_window(map_size).splitlines()
    for row_number, line in enumerate(map_lines, start=map_top):
        if row_number >= height - 2:
            break
        screen.addstr(row_number, map_left, line)
    screen.addstr(map_top + map_size + 1, map_left, "Arrow keys scroll")

    stats_left = max(width // 2, 42)
    screen.addstr(2, stats_left, "GAME STATS")
    stats = [
        f"Time:       {game.formatted_time()}",
        f"World seed: {game.world.seed}",
        f"Position:   ({game.player.tile_x}, {game.player.tile_y})",
        f"Health:     {game.health_bar()} {game.player.hp}/{game.player.max_hp}",
        f"Grenades:   {game.player.grenades} (+{game.player.holy_grenades} holy)",
        f"Discovered: {len(game.world.discovered)} tiles",
        f"Trophy:     {'Collected' if game.trophy_collected else 'Not collected'}",
        f"Altar:      {len(game.altar_slots)}/5 relics",
        f"Boss:       {'Defeated' if game.state.boss_defeated else 'Active' if game.boss_active else 'Not summoned'}",
    ]
    for row_number, line in enumerate(stats, start=4):
        if row_number < height - 2:
            screen.addstr(row_number, stats_left, line[: width - stats_left - 3])

    inventory_top = 11
    screen.addstr(inventory_top, stats_left, "INVENTORY")
    inventory = game.player.inventory or []
    item_counts = Counter((item.name, item.symbol) for item in inventory)
    inventory_lines = [
        f"{name} ({symbol}) x {count}" for (name, symbol), count in item_counts.items()
    ]
    if not inventory_lines:
        inventory_lines = ["(empty)"]
    for row_number, line in enumerate(inventory_lines, start=inventory_top + 1):
        if row_number < height - 2:
            screen.addstr(row_number, stats_left, line[: width - stats_left - 3])

    screen.addstr(height - 2, 3, message[: width - 6])
    screen.addstr(height - 1, 3, "M return to game | Q quit")
    screen.refresh()


def _draw_border(screen: "curses.window", height: int, width: int) -> None:
    """Draw a border around the entire terminal menu area."""
    screen.border()
