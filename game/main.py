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


def _show_home_screen(screen: "curses.window") -> str:
    """Show the title menu and return the selected action."""
    options = ("START GAME", "LORE", "HOW TO PLAY", "QUIT")
    selected = 0
    screen.nodelay(False)
    while True:
        screen.erase()
        height, width = screen.getmaxyx()
        title = [
            "================================",
            "          MAZE GAME             ",
            "================================",
            "",
            "The shrine waits. The brood stirs.",
            "",
        ]
        top = max(0, (height - len(title) - len(options)) // 2)
        for offset, line in enumerate(title):
            screen.addstr(top + offset, max(0, (width - len(line)) // 2), line[:width])
        for index, option in enumerate(options):
            label = f"> {option} <" if index == selected else f"  {option}  "
            screen.addstr(top + len(title) + index, max(0, (width - len(label)) // 2), label[:width])
        screen.addstr(height - 2, 2, "Use W/S or arrow keys. Press Enter to select. Q quits.")
        screen.refresh()
        key = screen.getch()
        if key in (ord("w"), 259):
            selected = (selected - 1) % len(options)
        elif key in (ord("s"), 258):
            selected = (selected + 1) % len(options)
        elif key in (10, 13, 32):
            return ("start", "lore", "help", "quit")[selected]
        elif key in (ord("1"), ord("2"), ord("3"), ord("4")):
            return ("start", "lore", "help", "quit")[key - ord("1")]
        elif key in (ord("q"), 27):
            return "quit"


def _show_info_screen(screen: "curses.window", title: str, lines: list[str]) -> None:
    """Show a text panel until the player returns to the home screen."""
    screen.nodelay(False)
    screen.erase()
    height, width = screen.getmaxyx()
    all_lines = [title, "", *lines, "", "Press any key to return to the home screen."]
    top = max(0, (height - len(all_lines)) // 2)
    for offset, line in enumerate(all_lines):
        screen.addstr(top + offset, max(0, (width - len(line)) // 2), line[:width])
    screen.refresh()
    screen.getch()


def _show_defeat_screen(screen: "curses.window", game: Game) -> None:
    _show_info_screen(
        screen,
        "GAME OVER",
        ["The dungeon has claimed you.", f"Time: {game.formatted_time()}", f"HP: {game.player.hp}/{game.player.max_hp}"],
    )


def run_curses(screen: "curses.window") -> None:
    """Run a non-blocking loop that responds to terminal key events."""
    curses.curs_set(0)
    screen.keypad(True)
    while True:
        choice = _show_home_screen(screen)
        if choice == "quit":
            return
        if choice == "lore":
            _show_info_screen(
                screen,
                "DUNGEON LORE",
                [
                    "Long ago, a serpent cult built a shrine beneath the maze.",
                    "Five relics and a key can awaken the altar.",
                    "Beyond it waits a giant snake and its endless brood.",
                    "The brood hunts intruders while the giant serpent circles its arena.",
                ],
            )
            continue
        if choice == "help":
            _show_info_screen(
                screen,
                "HOW TO PLAY",
                [
                    "W/A/S/D: move      E: potion      F: grenade",
                    "H: holy grenade    R: search      M: map",
                    "K: kneel at altar  P: place items C: cast",
                    "Explore to find the Gold Key and five unique relics.",
                    "Place them at the shrine, summon the boss, and survive.",
                ],
            )
            continue

        screen.nodelay(True)
        game = Game()
        message = "Reach the shrine altar. Hold a movement key to use terminal repeat."
        draw_screen(screen, game, message)
        while not game.won and not game.quit and not game.defeated:
            key = screen.getch()
            if key == -1:
                if game.update_realtime():
                    if game.event_message:
                        message = game.event_message
                    draw_screen(screen, game, message)
                curses.napms(1)
                continue
            while key != -1 and not game.won and not game.quit and not game.defeated:
                message = game.handle_key(key)
                key = screen.getch()
            if game.update_realtime() and game.event_message:
                message = game.event_message
            draw_screen(screen, game, message)

        if game.won:
            _show_victory_screen(screen, game)
        elif game.defeated:
            _show_defeat_screen(screen, game)
        elif game.quit:
            return


def run() -> None:
    """Start the game using the terminal's real-time input mode."""
    curses.wrapper(run_curses)


if __name__ == "__main__":
    run()
