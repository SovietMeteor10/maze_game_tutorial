# Checkpoints

Run these from the project root with `python3 tutorial/checkpoints/NAME.py`.
They are non-interactive by default, so this smoke test is also valid:

```text
for file in tutorial/checkpoints/*.py; do python3 "$file"; done
```

Use `--play` with checkpoints 03 and 04 to type WASD commands until `q`.

| File | Demonstrates |
| --- | --- |
| 01_static_room.py | A fixed 26 by 9 room |
| 02_player_coordinates.py | Coordinates and `@` |
| 03_wasd_conditionals.py | Scripted and interactive movement |
| 04_functions_collision_loop.py | Functions, collision, loop |
| 05_tile_openings.py | Direction dictionaries |
| 06_tile_renderer.py | Generated tile geometry |
| 07_static_tile_map.py | A list of lists |
| 08_connected_dungeon.py | Seeded connected growth |
| 09_items_inventory.py | Pickups and inventory |
| 10_doors_keys.py | Locked and open door state |
| 11_entities.py | Classes for game objects |
| 12_turn_combat.py | Enemy turns and combat |
| 13_secrets_minimap.py | Discovery and minimap |
| 14_boss_arena.py | Larger structure and boss state |
| 15_json_save_load.py | JSON round trip |
| 16_refactored_game.py | Small separated architecture |
