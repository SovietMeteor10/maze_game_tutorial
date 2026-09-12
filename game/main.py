"""Terminal entry point for the first playable game slice."""

import curses

from .game import Game
from .menu import draw_menu


def draw_screen(screen: "curses.window", game: Game, message: str) -> None:
    """Draw the complete game state in one terminal frame."""
    if game.show_minimap:
        draw_menu(screen, game, message)
        return

    screen.erase()
    screen.addstr(0, 0, "Maze Game | WASD move | H holy grenade | F grenade | R search | K kneel | P altar | C cast | M menu | Q quit")

    viewport_lines = game.render().splitlines()
    height, width = screen.getmaxyx()
    if height < len(viewport_lines) + 4 or width < len(viewport_lines[0]):
        screen.erase()
        screen.addstr(0, 0, f"Terminal too small. Need at least {len(viewport_lines[0])}x{len(viewport_lines) + 3}.")
        screen.refresh()
        return

    health_text = f"HP {game.health_bar()} {game.player.hp}/{game.player.max_hp}"
    screen.addstr(0, max(0, width - len(health_text) - 1), health_text)
    grenade_text = f"Grenades: {game.player.grenades} | Holy: {game.player.holy_grenades}"
    screen.addstr(1, max(0, width - len(grenade_text) - 1), grenade_text)

    for row_number, line in enumerate(viewport_lines, start=2):
        screen.addstr(row_number, 0, line)

    if game.pending_door is not None:
        _draw_door_popup(screen, height, width, game.door_prompt_mode)
    if game.state.summon_prompt:
        _draw_summon_popup(screen, height, width)
    if game.defeated:
        _draw_game_over_popup(screen, height, width, game)
    elif game.won:
        _draw_victory_popup(screen, height, width, game)

    status_row = len(viewport_lines) + 2
    screen.addstr(status_row, 0, "Viewport: @ player, K key, ! potion, = pouch, R relic, A altar, B boss | M menu")
    if game.boss_active:
        screen.addstr(status_row, max(0, width - 28), f"BOSS HP: {game.boss_health}/100")
    screen.addstr(status_row + 1, 0, message)
    screen.refresh()


def _draw_game_over_popup(screen: "curses.window", height: int, width: int, game: "Game") -> None:
    """Draw the centered defeat dialog."""
    lines = [
        "GAME OVER",
        "You were defeated.",
        f"HP: {game.player.hp}/{game.player.max_hp}",
        f"Time: {game.formatted_time()}",
        f"Position: ({game.player.tile_x}, {game.player.tile_y})",
        f"Discovered: {len(game.world.discovered)} tiles",
        f"Trophy: {'Collected' if game.trophy_collected else 'Not collected'}",
        f"Grenades: {game.player.grenades}",
        "Press any key to quit",
    ]
    popup_width = max(len(line) for line in lines) + 4
    popup_height = len(lines) + 2
    left = max(0, (width - popup_width) // 2)
    top = max(0, (height - popup_height) // 2)
    border = "+" + "-" * (popup_width - 2) + "+"
    screen.addstr(top, left, border)
    for row, line in enumerate(lines, start=1):
        screen.addstr(top + row, left, f"| {line.ljust(popup_width - 4)} |")
    screen.addstr(top + popup_height - 1, left, border)


def _draw_victory_popup(screen: "curses.window", height: int, width: int, game: "Game") -> None:
    """Draw the completion screen after the boss encounter."""
    message = (
        "The giant snake and its brood are defeated!"
        if game.state.boss_defeated
        else "You found the exit."
    )
    lines = [
        "VICTORY",
        message,
        f"Time: {game.formatted_time()}",
        f"HP: {game.player.hp}/{game.player.max_hp}",
        "Press any key to close",
    ]
    popup_width = max(len(line) for line in lines) + 4
    popup_height = len(lines) + 2
    left = max(0, (width - popup_width) // 2)
    top = max(0, (height - popup_height) // 2)
    border = "+" + "-" * (popup_width - 2) + "+"
    screen.addstr(top, left, border)
    for row, line in enumerate(lines, start=1):
        screen.addstr(top + row, left, f"| {line.ljust(popup_width - 4)} |")
    screen.addstr(top + popup_height - 1, left, border)


def _show_victory_screen(screen: "curses.window", game: "Game") -> None:
    """Show a standalone victory screen until the player acknowledges it."""
    screen.nodelay(False)
    screen.erase()
    height, width = screen.getmaxyx()
    lines = [
        "VICTORY",
        "The giant snake and its brood are defeated!",
        f"Time: {game.formatted_time()}",
        f"HP: {game.player.hp}/{game.player.max_hp}",
        "Press any key to close",
    ]
    top = max(0, (height - len(lines)) // 2)
    for offset, line in enumerate(lines):
        left = max(0, (width - len(line)) // 2)
        screen.addstr(top + offset, left, line[: max(0, width - left)])
    screen.refresh()
    screen.getch()


def _draw_door_popup(screen: "curses.window", height: int, width: int, mode: str) -> None:
    """Draw a centered confirmation dialog over the current game view."""
    if mode == "locked":
        lines = [
            "DOOR LOCKED",
            "The door is locked and you lack a key.",
            "Press N to close",
        ]
    else:
        lines = [
            "DOOR",
            "Do you want to open the door?",
            "Press Y to open, N to cancel",
        ]
    popup_width = max(len(line) for line in lines) + 4
    popup_height = len(lines) + 2
    left = max(0, (width - popup_width) // 2)
    top = max(0, (height - popup_height) // 2)
    border = "+" + "-" * (popup_width - 2) + "+"
    screen.addstr(top, left, border)
    for row, line in enumerate(lines, start=1):
        screen.addstr(top + row, left, f"| {line.ljust(popup_width - 4)} |")
    screen.addstr(top + popup_height - 1, left, border)


def _draw_summon_popup(screen: "curses.window", height: int, width: int) -> None:
    """Draw the altar's summon confirmation dialog."""
    lines = [
        "ALTAR RITUAL",
        "Summon the giant snake boss?",
        "Press Y to confirm, N to cancel",
    ]
    popup_width = max(len(line) for line in lines) + 4
    popup_height = len(lines) + 2
    left = max(0, (width - popup_width) // 2)
    top = max(0, (height - popup_height) // 2)
    border = "+" + "-" * (popup_width - 2) + "+"
    screen.addstr(top, left, border)
    for row, line in enumerate(lines, start=1):
        screen.addstr(top + row, left, f"| {line.ljust(popup_width - 4)} |")
    screen.addstr(top + popup_height - 1, left, border)


def run_curses(screen: "curses.window") -> None:
    """Run a non-blocking loop that responds to terminal key events."""
    curses.curs_set(0)
    screen.nodelay(True)
    screen.keypad(True)

    game = Game()
    message = "Reach E. Hold a movement key to use terminal key repeat."
    draw_screen(screen, game, message)

    while not game.won and not game.quit:
        key = screen.getch()
        if key == -1:
            if game.update_realtime():
                if game.event_message:
                    message = game.event_message
                draw_screen(screen, game, message)
            # A zero timeout keeps the loop responsive without waiting for input.
            curses.napms(1)
            continue

        # Drain all key events already waiting so fast key combinations are not
        # delayed behind a redraw for each individual event.
        while key != -1 and not game.won and not game.quit:
            message = game.handle_key(key)
            key = screen.getch()

        if game.update_realtime() and game.event_message:
            message = game.event_message
        draw_screen(screen, game, message)

    if game.won:
        _show_victory_screen(screen, game)
    elif game.defeated:
        draw_screen(screen, game, "Game over.")
        screen.nodelay(False)
        screen.getch()


def run() -> None:
    """Start the game using the terminal's real-time input mode."""
    curses.wrapper(run_curses)


if __name__ == "__main__":
    run()
