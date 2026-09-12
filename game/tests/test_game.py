import unittest

from game.constants import TILE_HEIGHT, TILE_WIDTH, WALL_SYMBOL
from game.game import Game
from game.game_state import GameState
from game.items import Item
from game.room import build_room, is_floor


class RoomTests(unittest.TestCase):
    def test_room_has_locked_dimensions(self):
        room = build_room()

        self.assertEqual(len(room), TILE_HEIGHT)
        self.assertTrue(all(len(row) == TILE_WIDTH for row in room))

    def test_room_has_walls_and_floor(self):
        room = build_room()

        self.assertEqual(room[0][0], WALL_SYMBOL)
        self.assertTrue(is_floor(room, TILE_WIDTH // 2, TILE_HEIGHT // 2))
        self.assertFalse(is_floor(room, 0, 0))


class GameTests(unittest.TestCase):
    def test_game_state_is_the_source_of_gameplay_state(self):
        game = Game(seed=7)

        self.assertIsInstance(game.state, GameState)
        self.assertIs(game.state.player, game.player)
        self.assertIs(game.state.world, game.world)
        self.assertIs(game.state.items, game.items)
        self.assertIs(game.state.discovered, game.world.discovered)

    def test_player_starts_on_floor(self):
        game = Game()

        self.assertTrue(game.can_move_to(game.player.x, game.player.y))
        self.assertFalse(game.won)

    def test_player_can_move_on_floor(self):
        game = Game()
        start = (game.player.x, game.player.y)

        self.assertTrue(game.move_player("w"))
        self.assertEqual((game.player.x, game.player.y), (start[0], start[1] - 1))

    def test_start_room_allows_horizontal_movement(self):
        game = Game(seed=7)
        start_x = game.player.x

        self.assertTrue(game.move_player("a"))
        self.assertEqual(game.player.x, start_x - 2)

    def test_all_start_room_openings_allow_tile_entry(self):
        openings = {
            "N": ("w", 13, 0, (5, 4)),
            "E": ("d", 25, 4, (6, 5)),
            "S": ("s", 13, 8, (5, 6)),
            "W": ("a", 0, 4, (4, 5)),
        }
        for command, x, y, expected_tile in openings.values():
            game = Game(seed=7)
            game.player.x = x
            game.player.y = y

            self.assertTrue(game.move_player(command))
            self.assertEqual((game.player.tile_x, game.player.tile_y), expected_tile)

    def test_clear_start_openings_are_not_blocked_by_room_state(self):
        for command, x, y in (
            ("w", 13, 0),
            ("d", 25, 4),
            ("s", 13, 8),
            ("a", 0, 4),
        ):
            game = Game(seed=7)
            game.player.x, game.player.y = x, y
            game.state.doors.clear()
            game.state.secret_walls.clear()
            game.state.obstacles.clear()

            self.assertTrue(game.move_player(command))

    def test_wall_blocks_player(self):
        game = Game()
        game.player.x = 1
        game.player.y = 0

        self.assertFalse(game.move_player("a"))
        self.assertEqual((game.player.x, game.player.y), (1, 0))

    def test_trophy_is_not_in_the_starting_tile(self):
        game = Game()

        self.assertNotEqual(game.trophy_tile, (game.player.tile_x, game.player.tile_y))
        self.assertFalse(game.trophy_collected)
        self.assertFalse(game.won)

    def test_collecting_trophy_does_not_end_game(self):
        game = Game()
        game.trophy_tile = (6, 5)
        game.trophy_position = (13, 4)
        game.state.items.append(Item(13, 4, "E trophy", "treasure", 6, 5, symbol="E"))
        game.player.tile_x, game.player.tile_y = game.trophy_tile
        game.player.x, game.player.y = game.trophy_position

        self.assertTrue(game.collect_trophy_if_present())
        self.assertTrue(game.trophy_collected)
        self.assertFalse(game.won)

    def test_invalid_command_does_not_move(self):
        game = Game()
        start = (game.player.x, game.player.y)

        message = game.handle_command("x")

        self.assertEqual((game.player.x, game.player.y), start)
        self.assertIn("Use", message)

    def test_key_events_can_be_processed_without_line_input(self):
        game = Game()
        start = (game.player.x, game.player.y)

        game.handle_key(ord("w"))
        game.handle_key("a")

        self.assertEqual((game.player.x, game.player.y), (start[0] - 2, start[1] - 1))

    def test_viewport_is_always_five_by_five(self):
        game = Game(seed=7)

        self.assertEqual(len(game.world.discovered), 9)
        viewport = game.render_world_map().splitlines()
        self.assertEqual(len(viewport), 45)
        self.assertTrue(all(len(line) == 130 for line in viewport))
        self.assertIn("~", "".join(viewport))

    def test_crossing_room_edge_reveals_neighbouring_world_tile(self):
        game = Game(seed=7)
        game.player.x = 25
        game.player.y = 4
        discovered_before = len(game.world.discovered)

        self.assertTrue(game.move_player("d"))
        self.assertEqual(game.player.tile_x, 6)
        self.assertEqual(game.player.x, 1)
        self.assertGreater(len(game.world.discovered), discovered_before)

    def test_entered_tile_has_a_reciprocal_opening(self):
        game = Game(seed=7)
        game.player.x = 25
        game.player.y = 4

        self.assertTrue(game.move_player("d"))
        self.assertIn("W", game.world.connections[(6, 5)])

    def test_minimap_is_closed_until_requested(self):
        game = Game()

        self.assertFalse(game.show_minimap)
        self.assertIn("opened", game.handle_command("m"))
        self.assertTrue(game.show_minimap)
        self.assertIn("closed", game.handle_command("m"))
        self.assertFalse(game.show_minimap)

    def test_minimap_window_is_square_and_starts_centered_on_player(self):
        game = Game(seed=7)
        window = game.render_minimap_window(5).splitlines()

        self.assertEqual(len(window), 5)
        self.assertTrue(all(len(line) == 15 for line in window))
        self.assertEqual(window[2][6:9], "[@]")

    def test_minimap_scrolls_in_both_directions_while_menu_is_open(self):
        game = Game(seed=7)
        game.handle_command("m")

        game.handle_key(259)
        game.handle_key(261)

        self.assertEqual(game.minimap_scroll_y, -1)
        self.assertEqual(game.minimap_scroll_x, 1)

    def test_menu_pauses_movement_and_has_a_frozen_time_value(self):
        game = Game(seed=7)
        start = (game.player.x, game.player.y)

        game.handle_command("m")
        frozen_time = game.elapsed_seconds(now=game.menu_started_at + 100)
        message = game.handle_command("d")

        self.assertEqual((game.player.x, game.player.y), start)
        self.assertIn("Menu open", message)
        self.assertEqual(game.elapsed_seconds(now=game.menu_started_at + 100), frozen_time)

    def test_discovered_landmarks_are_visible_on_the_minimap(self):
        game = Game()
        game.world.add_landmark(4, 4, "B")
        game.world.reveal_around(4, 4)

        self.assertIn("[B]", game.render_minimap())


if __name__ == "__main__":
    unittest.main()
