import unittest

from game.game import Game


class ObstacleTests(unittest.TestCase):
    def _game_with_discovered_area(self):
        game = Game(seed=7)
        for _ in range(7):
            game.handle_command("d")
        return game

    def test_rooms_can_contain_visible_x_barriers(self):
        game = self._game_with_discovered_area()

        self.assertTrue(game.obstacles)
        self.assertIn("X", game.render())

    def test_x_barrier_blocks_movement(self):
        game = self._game_with_discovered_area()
        obstacle = next(iter(game.obstacles))
        game.player.tile_x, game.player.tile_y = obstacle.tile_x, obstacle.tile_y
        game.player.x, game.player.y = obstacle.x - 1, obstacle.y
        game.room = game.world.tiles[(obstacle.tile_x, obstacle.tile_y)].render()

        self.assertFalse(game.can_move_to(obstacle.x, obstacle.y))


if __name__ == "__main__":
    unittest.main()
