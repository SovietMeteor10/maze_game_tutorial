import unittest

from game.game import Game
from game.items import Item
from game.obstacles import Obstacle


class GrenadeTests(unittest.TestCase):
    def test_grenade_pouch_adds_three_grenades(self):
        game = Game(seed=7)
        pouch = Item(13, 4, "Grenade Pouch", "grenade_pouch", quantity=3)
        game.state.items.append(pouch)

        game.collect_items_if_present()

        self.assertEqual(game.player.grenades, 3)

    def test_f_drops_grenade_and_uses_one(self):
        game = Game(seed=7)
        game.player.grenades = 1

        message = game.handle_command("f")

        self.assertIn("dropped", message.lower())
        self.assertEqual(game.player.grenades, 0)
        self.assertEqual(len(game.grenades), 1)

    def test_grenade_flashes_three_times_then_explodes(self):
        game = Game(seed=7)
        game.player.grenades = 1
        game.player.hp = 20
        game.state.items.extend([
            Item(15, 4, "Health Potion", "potion", 5, 5),
            Item(15, 4, "Gold Key", "key", 5, 5, key_id="gold"),
        ])
        game.state.obstacles.add(Obstacle(5, 5, 14, 4))
        game.handle_command("f")

        for _ in range(6):
            game._update_effects_tick()

        self.assertFalse(game.grenades)
        self.assertTrue(game.explosions)
        self.assertEqual(game.player.hp, 10)
        self.assertFalse(any(item.kind == "potion" for item in game.items))
        self.assertTrue(any(item.kind == "key" for item in game.items))
        self.assertFalse(game.obstacles)

    def test_explosion_can_defeat_the_player(self):
        game = Game(seed=7)
        game.player.grenades = 1
        game.player.hp = 5
        game.handle_command("f")

        for _ in range(6):
            game._update_effects_tick()

        self.assertTrue(game.defeated)
        self.assertIn("explosion", game.event_message.lower())


if __name__ == "__main__":
    unittest.main()
