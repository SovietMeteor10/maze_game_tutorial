import unittest

from game.game import Game
from game.items import ITEM_SYMBOLS, Item


class ItemTests(unittest.TestCase):
    def _game_with_discovered_area(self):
        game = Game(seed=7)
        for _ in range(7):
            game.handle_command("d")
        return game

    def test_item_uses_symbol_for_its_kind(self):
        for kind, symbol in ITEM_SYMBOLS.items():
            self.assertEqual(Item(1, 1, kind.title(), kind).symbol, symbol)

    def test_game_places_items_on_floor_tiles(self):
        game = self._game_with_discovered_area()

        self.assertIn("key", {item.kind for item in game.items})
        for item in game.items:
            tile = game.world.tiles[(item.tile_x, item.tile_y)]
            self.assertNotEqual(tile.render()[item.y][item.x], "#")
            self.assertNotIn(
                (item.tile_x, item.tile_y, item.x, item.y),
                {obstacle.position for obstacle in game.obstacles},
            )

    def test_key_is_in_a_one_opening_room(self):
        game = self._game_with_discovered_area()
        key = next(item for item in game.items if item.kind == "key")
        tile = game.world.tiles[(key.tile_x, key.tile_y)]

        self.assertEqual(tile.kind, "room")
        self.assertEqual(len(tile.openings), 1)

    def test_items_are_dispersed_across_different_floor_positions(self):
        game = self._game_with_discovered_area()
        positions = {item.position for item in game.items}

        self.assertEqual(len(positions), len(game.items))

    def test_items_are_picked_up_automatically(self):
        game = self._game_with_discovered_area()
        item = next(item for item in game.items if item.kind == "key")
        game.player.tile_x, game.player.tile_y = item.tile_x, item.tile_y
        game.player.x, game.player.y = item.x - 2, item.y
        game.room = game.world.tiles[(item.tile_x, item.tile_y)].render()

        message = game.handle_command("d")

        self.assertIn(item.name, message)
        self.assertIn(item, game.player.inventory)
        self.assertNotIn(item, game.items)

    def test_side_entry_can_pick_up_centered_key(self):
        game = self._game_with_discovered_area()
        item = next(item for item in game.items if item.kind == "key")
        game.player.tile_x, game.player.tile_y = item.tile_x, item.tile_y
        game.player.x, game.player.y = item.x - 1, item.y
        game.room = game.world.tiles[(item.tile_x, item.tile_y)].render()

        game.handle_command("d")

        self.assertIn(item, game.player.inventory)

    def test_trophy_is_a_treasure_in_the_inventory(self):
        game = self._game_with_discovered_area()
        game.trophy_tile = (7, 5)
        game.trophy_position = (13, 4)
        game.state.items.append(Item(13, 4, "E trophy", "treasure", 7, 5, symbol="E"))
        game.player.tile_x, game.player.tile_y = game.trophy_tile
        game.player.x, game.player.y = game.trophy_position

        self.assertTrue(game.collect_trophy_if_present())
        self.assertTrue(game.trophy_collected)
        self.assertEqual(game.player.inventory[0].kind, "treasure")


if __name__ == "__main__":
    unittest.main()
