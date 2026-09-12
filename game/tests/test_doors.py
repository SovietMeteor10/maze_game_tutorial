import unittest

from game.doors import Door, edge_key
from game.game import Game
from game.items import Item
from game.tiles import OPENING_CELLS
from game.world import DELTA, OPPOSITE


class DoorTests(unittest.TestCase):
    def _game_with_discovered_area(self):
        game = Game(seed=7)
        for _ in range(7):
            game.handle_command("d")
        return game

    def test_edge_key_is_shared_by_both_sides(self):
        self.assertEqual(edge_key(4, 4, "E"), edge_key(5, 4, "W"))

    def test_door_is_an_overlay_on_an_existing_open_connection(self):
        game = self._game_with_discovered_area()
        door = next(iter(game.doors.values()))
        dx, dy = DELTA[door.direction]
        neighbour = (door.tile_x + dx, door.tile_y + dy)

        self.assertIn(
            door.direction, game.world.connections[(door.tile_x, door.tile_y)]
        )
        self.assertIn(OPPOSITE[door.direction], game.world.connections[neighbour])
        glyph = "-" if door.direction in ("N", "S") else "|"
        self.assertIn(glyph, game.render())
        self.assertGreaterEqual(
            game.render().count(glyph), len(OPENING_CELLS[door.direction])
        )

    def test_locked_door_does_not_seal_the_key_route(self):
        game = self._game_with_discovered_area()
        door = next(iter(game.doors.values()))
        key = next(item for item in game.items if item.kind == "key")

        self.assertGreater(len(game.world.connections[(door.tile_x, door.tile_y)]), 1)
        self.assertTrue(
            game._reachable_without_edge(key.tile_x, key.tile_y, door.position)
        )

    def test_matching_key_unlocks_door_without_consuming_key(self):
        door = Door(4, 4, "E", key_id="gold")
        key = Item(1, 1, "Gold key", "key", key_id="gold")

        inventory = [key]
        self.assertFalse(door.can_open([]))
        self.assertTrue(door.unlock(inventory))
        self.assertFalse(door.locked)
        self.assertEqual(inventory, [key])

    def test_movement_prompts_then_consumes_key_when_opening_door(self):
        game = self._game_with_discovered_area()
        door = next(iter(game.doors.values()))
        command = {"N": "w", "E": "d", "S": "s", "W": "a"}[door.direction]
        x, y = OPENING_CELLS[door.direction][-1]
        game.player.tile_x, game.player.tile_y = door.tile_x, door.tile_y
        game.player.x, game.player.y = x, y
        game.room = game.world.tiles[(door.tile_x, door.tile_y)].render()
        key = Item(1, 1, "Gold key", "key", key_id="gold")
        game.player.inventory.append(key)

        prompt = game.handle_command(command)

        self.assertIn("open", prompt.lower())
        self.assertIs(game.pending_door, door)
        self.assertTrue(door.locked)

        result = game.handle_command("y")

        self.assertIn("opened", result.lower())
        self.assertFalse(door.locked)
        self.assertNotIn(key, game.player.inventory)

    def test_locked_door_without_key_uses_popup_state(self):
        game = self._game_with_discovered_area()
        door = next(iter(game.doors.values()))
        command = {"N": "w", "E": "d", "S": "s", "W": "a"}[door.direction]
        game.player.tile_x, game.player.tile_y = door.tile_x, door.tile_y
        game.player.x, game.player.y = OPENING_CELLS[door.direction][-1]
        game.room = game.world.tiles[(door.tile_x, door.tile_y)].render()

        message = game.handle_command(command)

        self.assertIn("locked", message.lower())
        self.assertIn("lack", message.lower())
        self.assertEqual(game.door_prompt_mode, "locked")
        self.assertIsNotNone(game.pending_door)

        game.handle_command("n")
        self.assertIsNone(game.pending_door)


if __name__ == "__main__":
    unittest.main()
