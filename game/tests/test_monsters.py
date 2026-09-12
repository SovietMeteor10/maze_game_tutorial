import unittest

from game.game import Game
from game.items import Item
from game.obstacles import Obstacle


class MonsterTests(unittest.TestCase):
    def _game_with_key_room(self):
        game = Game(seed=7)
        for _ in range(7):
            game.handle_command("d")
        return game

    def test_snakes_only_spawn_in_key_rooms(self):
        game = self._game_with_key_room()
        key_rooms = {
            (item.tile_x, item.tile_y) for item in game.items if item.kind == "key"
        }

        self.assertTrue(game.monsters)
        self.assertTrue(
            all((snake.tile_x, snake.tile_y) in key_rooms for snake in game.monsters)
        )
        self.assertTrue(all(4 <= snake.tail_length <= 7 for snake in game.monsters))

    def test_snake_can_detect_player_in_an_adjacent_room(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        graph = game.world.connection_graph()
        adjacent = next(iter(graph[(snake.tile_x, snake.tile_y)]))
        game.player.tile_x, game.player.tile_y = adjacent
        game.player.x, game.player.y = 13, 4

        self.assertEqual(game._room_distance((snake.tile_x, snake.tile_y), adjacent), 1)
        self.assertIsNotNone(game._next_snake_position(snake))

    def test_visible_snake_patrols_outside_its_three_by_three_area(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x - 2, snake.tile_y
        game.player.x, game.player.y = 13, 4
        game.last_snake_update = 100.0
        before = snake.position

        self.assertTrue(game.update_realtime(100.5))
        self.assertNotEqual(snake.position, before)

    def test_snake_body_is_solid(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        _, _, tail_x, tail_y = snake.tail[0]

        self.assertFalse(
            game._snake_can_occupy(
                (snake.tile_x, snake.tile_y),
                tail_x,
                tail_y,
                snake,
            )
        )

    def test_snake_routes_around_a_wall_instead_of_stopping(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x, snake.tile_y
        game.player.x, game.player.y = snake.x + 4, snake.y
        game.state.obstacles.add(
            Obstacle(snake.tile_x, snake.tile_y, snake.x + 2, snake.y)
        )

        next_position = game._next_snake_local_position(snake)

        self.assertIsNotNone(next_position)
        self.assertNotEqual(next_position[2:], (snake.x + 2, snake.y))

    def test_snake_stays_on_player_and_damages_until_defeat(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x, snake.tile_y
        game.player.x, game.player.y = snake.x, snake.y
        game.player.hp = 6
        game.last_snake_update = 100.0
        before = snake.position

        game.update_realtime(100.5)
        self.assertEqual(snake.position, before)
        self.assertEqual(game.player.hp, 3)
        game.last_snake_update = 100.5
        game.update_realtime(101.0)

        self.assertTrue(game.defeated)
        self.assertEqual(snake.position, before)

    def test_snake_moves_every_second_update(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x, snake.tile_y
        game.player.x, game.player.y = snake.x + 4, snake.y
        game.player_turns = 0
        before = snake.position

        game.update_snakes()
        self.assertEqual(snake.position, before)
        game.update_snakes()
        self.assertNotEqual(snake.position, before)
        self.assertEqual(snake.tail[0], before)

    def test_snakes_move_from_realtime_ticks_without_player_input(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x, snake.tile_y
        game.player.x, game.player.y = snake.x + 4, snake.y
        game.last_snake_update = 100.0
        before = snake.position

        self.assertFalse(game.update_realtime(100.49))
        self.assertTrue(game.update_realtime(100.5))
        self.assertNotEqual(snake.position, before)

    def test_health_potion_is_consumed_with_e(self):
        game = Game(seed=7)
        game.player.hp = 10
        potion = Item(1, 1, "Health Potion", "potion")
        game.player.inventory.append(potion)

        message = game.handle_command("e")

        self.assertIn("used", message.lower())
        self.assertEqual(game.player.hp, 15)
        self.assertNotIn(potion, game.player.inventory)

    def test_health_bar_shrinks_with_hp(self):
        game = Game(seed=7)

        game.player.hp = 10

        self.assertEqual(game.health_bar(), "[##########----------]")

    def test_player_input_does_not_trigger_snake_turn(self):
        game = self._game_with_key_room()
        snake = game.monsters[0]
        game.player.tile_x, game.player.tile_y = snake.tile_x, snake.tile_y
        game.player.x, game.player.y = snake.x + 4, snake.y
        game.last_snake_update = 100.0
        before = snake.position

        game.handle_command("w")

        self.assertEqual(snake.position, before)


if __name__ == "__main__":
    unittest.main()
