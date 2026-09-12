import unittest

from game.game import Game
from game.tiles import OPENING_CELLS


class SecretRoomTests(unittest.TestCase):
    def _game_with_discovered_area(self):
        game = Game(seed=7)
        for _ in range(7):
            game.handle_command("d")
        return game

    def test_secret_wall_hides_a_room_until_search(self):
        game = self._game_with_discovered_area()
        wall = next(iter(game.secret_walls.values()))
        game.player.tile_x, game.player.tile_y = wall.tile_x, wall.tile_y
        game.player.x, game.player.y = OPENING_CELLS[wall.direction][-1]
        game.room = game.world.tiles[(wall.tile_x, wall.tile_y)].render()

        blocked = game.handle_command(
            {"N": "w", "E": "d", "S": "s", "W": "a"}[wall.direction]
        )

        self.assertIn("secret wall", blocked.lower())
        self.assertFalse(wall.found)
        self.assertNotIn(wall.hidden_tile, game.world.discovered)

        message = game.handle_command("f")

        self.assertIn("hidden room", message.lower())
        self.assertTrue(wall.found)
        self.assertIn(wall.hidden_tile, game.world.discovered)
        self.assertEqual(game.world.landmarks[wall.hidden_tile], "H")

    def test_search_without_a_secret_wall_is_safe(self):
        game = Game(seed=7)

        self.assertIn("no secret wall", game.handle_command("f").lower())


if __name__ == "__main__":
    unittest.main()
