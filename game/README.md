# Reference Game

For complete installation, virtual-environment, Windows, testing, and
troubleshooting instructions, see [`../SETUP.md`](../SETUP.md).

This is the first playable slice of the reference implementation. It uses the terminal's non-blocking input mode, so the screen stays in place and movement responds to individual key events and terminal key repeat. Run it from the project root with:

```text
python3 -m game.main
```

Run its tests with:

```text
python3 -m unittest discover -s game/tests -t .
```

The current version contains larger 26x9 tiles, an infinite lazily generated connected world, a moving five-by-five full-tile viewport with three-by-three fog-of-war discovery, a connected undirected world graph that preserves loops while preventing isolated revealed areas, a `GameState` object containing the player, world, items, discovery, doors, secret walls, obstacles, monsters, grenades, explosions, and progression state, graph-compatible room, dead-end, straight, corner, T-junction, and cross tile kinds with rooms weighted 2x near corridor or corner nodes, safe `X` room barriers generated at a 1-in-8 chance per eligible room, refreshed active-room geometry after graph expansion, ratio-adjusted movement, an empty spawn area, discovery-driven randomized item placement, one-opening room tiles, keys restricted to those rooms, collectible keyed items, grenade pouches, frontier doors created after a key exists, full-gap locked door overlays using `-` across north/south gaps and `|` across east/west gaps, searchable secret-wall overlays created as new areas are entered, collectible potions and treasure, snakes with solid 4-7 segment tails that patrol while visible in the five-by-five viewport, switch to player-directed pathfinding inside the player-centered three-by-three big-tile area, and move on an independent real-time clock, timed grenades dropped with `F`, three grenade flashes rendered as `+ O + O + O`, 3x3 explosion damage, a top-right HP bar and grenade count, and a paused square minimap centered on the player with arrow-key scrolling and an aggregated inventory menu opened with `M`. Explosions damage players and snakes by 10, destroy `X` barriers and non-key items, and never destroy walls or keys. Doors preserve the underlying graph connection, do not seal dead ends, and are placed only when the key remains reachable before crossing them. Room barriers do not alter graph connectivity and are only placed when the remaining floor stays connected. Trying to cross a door with its matching key opens a centered Y/N confirmation popup; confirming consumes one key and opens the door. Trying to cross it without a key shows a centered locked-door popup. Press `F` beside a concealed wall to reveal its hidden room when no grenades are available and `H` minimap landmark. Press `E` to use a Health Potion. Inventory entries use the format `Health Potion (!) x 1`. Finding the trophy adds it to the inventory but does not end the game. Pass a seed to `Game` when a repeatable dungeon is needed for tests. Future stages will add combat depth, a boss room, and save/load.
