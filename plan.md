# Maze Game Build Plan

This plan turns `TASK.md` into two related deliverables:

1. A complete, modular reference game that is built and tested first.
2. A separate tutorial version that reconstructs the game in beginner-friendly steps.

The reference game is the source of truth for behaviour. The tutorial should explain and rebuild the same ideas, but it does not need to copy the final code line-for-line.

## Project Layout

Keep the two deliverables separate:

```text
maze_game_tutorial/
|
|- TASK.md
|- plan.md
|
|- game/              # Complete reference implementation
|  |- main.py
|  |- constants.py
|  |- tiles.py
|  |- dungeon.py
|  |- entities.py
|  |- items.py
|  |- combat.py
|  |- render.py
|  |- game_state.py
|  |- save.py
|  `- tests/
|
`- tutorial/          # Beginner-facing build, added after game/ is complete
   |- lessons/
   |- checkpoints/
   `- README.md
```

Do not create every module on the first day. Begin with a small working program and split it when a responsibility becomes clear. The final `game/` structure should reflect the architecture, not anticipate it prematurely.

## Reference Game Principles

These rules apply throughout the reference implementation:

- Keep world data, game state, game logic, and rendering separate.
- Store the dungeon as `dungeon[y][x]` and document coordinate conventions.
- Keep the player, monsters, items, and doors outside the terrain grid.
- Give each function one clear responsibility.
- Prefer calculated geometry and named constants over repeated ASCII templates.
- Make tile connections valid by construction and validate them with assertions.
- Keep each milestone playable and runnable.
- Add tests around geometry, connectivity, movement, combat, and save/load as those systems appear.

## Current Product Baseline

The reference game already contains the following shipped product features. This is the
behaviour the tutorial should eventually explain and rebuild in smaller steps. Features
listed here are implemented in `game/`; they are not future requirements.

### Launch and terminal experience

- Launch from the project root with `python3 -m game.main`.
- Use a curses terminal interface with non-blocking key input and terminal key repeat.
- Show a home screen with `START GAME`, `LORE`, `HOW TO PLAY`, and `QUIT` options.
- Show lore and controls/help screens before starting a run.
- Detect terminals that are too small for the game viewport or menu.
- Show contextual status messages, health, grenade counts, boss health, and control hints.
- Show centered confirmation and result dialogs for doors, altar summoning, victory, and defeat.
- Support quitting from the game and the menu.

### World and tile system

- Generate an effectively infinite, lazily created world from a seed.
- Keep world tiles in a graph-compatible coordinate system with reciprocal openings.
- Preserve loops while connecting newly revealed areas into one reachable component.
- Support room, dead-end, straight corridor, corner, T-junction, and cross tile kinds.
- Render tiles at a fixed 26 by 9 geometry with centered openings.
- Weight rooms more heavily near corridor and corner nodes.
- Refresh tile geometry when graph connections expand.
- Maintain a special three-by-three shrine region around the starting area.
- Maintain a special five-by-five boss region created during the summoning sequence.
- Keep terrain, player, items, doors, secret walls, obstacles, monsters, grenades, and explosions as separate state layers.

### Exploration and movement

- Move with `W`, `A`, `S`, and `D`, including ratio-adjusted horizontal movement for terminal character proportions.
- Block movement through walls, shrine altar geometry, obstacles, locked doors, and undiscovered secret walls.
- Move across valid tile openings and automatically reveal a three-by-three area around the player.
- Keep a five-by-five full-tile gameplay viewport centered on the player.
- Mask undiscovered viewport tiles with fog-of-war markers.
- Automatically collect items when the player reaches their floor position.
- Track gameplay time while excluding time spent in the menu.
- Render an ASCII health bar and formatted elapsed time.

### Items and progression

- Place randomized items only on valid floor cells and avoid collisions with obstacles and other items.
- Guarantee a Gold Key in a one-opening room and place a guarding snake there.
- Support health potions, treasure/trophy, grenade pouches, holy grenades, and five unique relics:
  `Amulet`, `Spear`, `Shield`, `Book of the Dead`, and `Snake Skull`.
- Add item symbols to the rendered world and move collected items into the player inventory.
- Add grenade quantities from pouches and holy-grenade quantities from pickups.
- Prevent duplicate relic collection and drop the unique Snake Skull relic from a defeated regular snake.
- Track trophy collection without treating it as immediate victory.
- Provide a shrine altar in the starting region.
- Allow the player to kneel at the altar with `K`.
- Allow the player to place the Gold Key and collected relics with `P`.
- Require the key and all five relics before allowing the summoning ritual.

### Doors and secrets

- Place a locked door overlay on an existing frontier connection after a key exists.
- Keep doors from sealing the only route to the key and avoid placing them on dead ends.
- Render locked north/south doors across openings with `-` and east/west doors with `|`.
- Prompt the player before opening a door.
- Consume the matching key when a prompted door is opened.
- Keep the connection itself in the world graph when a door is locked.
- Create searchable secret-wall overlays on frontier connections.
- Search with `R`, or use the `F` fallback when no grenade is available.
- Reveal and populate the hidden area after a secret wall is found.
- Mark revealed hidden rooms on the map.

### Obstacles and combat

- Add `X` barriers to eligible rooms with a one-in-eight chance.
- Only place barriers when the remaining room floor remains connected.
- Prevent movement through barriers.
- Support regular snakes with solid four-to-seven-cell tails.
- Patrol snakes outside the player-centered three-by-three area.
- Use player-directed local pathfinding when snakes are close enough to pursue.
- Move snakes on an independent real-time clock and support turn-based update calls for tests and non-terminal callers.
- Apply contact damage when the player enters or remains on a snake body.
- Support a giant boss snake, boss sub-boss split, and boss minions.
- Provide an internal close-range `attack()` rule for snake damage, while grenades are the current terminal combat action.
- End the run in defeat when player health reaches zero.

### Grenades and effects

- Drop a standard grenade with `F` when grenades are available.
- Drop a holy grenade with `H`.
- Animate grenades through three visible flash cycles using `+` and `O`.
- Detonate grenades after the timed flash sequence.
- Damage players and snakes within the standard blast area.
- Give holy grenades a larger cross-shaped effect and heavier damage.
- Destroy `X` barriers and non-key items in the blast area.
- Never destroy walls or keys with explosions.
- Render active explosion effects for a short duration.
- Allow explosions to defeat snakes, trigger relic drops, and complete the boss encounter.

### Boss and completion loop

- Require the player to explore, collect the Gold Key and five relics, return to the altar, kneel, place the offerings, and cast with `C`.
- Show a confirmation prompt before the summoning ritual.
- Play a short summoning animation before teleporting the player.
- Generate a five-by-five boss arena and populate it with the giant snake, minions, grenade pouches, and a holy grenade.
- Disable the minimap while the player is in the boss arena.
- Keep the boss moving around an arena route and periodically spawn minions and pickups.
- Split the wounded giant snake into two counter-rotating sub-bosses.
- Win after the boss encounter is defeated.
- Track the trophy as an `E` landmark and inventory item without treating collection as immediate victory.
- Show victory and defeat screens with time, health, and outcome details.

### Map, menu, and inspection views

- Open the paused map and statistics menu with `M`.
- Pause movement, real-time effects, and gameplay time while the menu is open.
- Render a square minimap centered on the player.
- Scroll the minimap with arrow keys while it is open.
- Show the discovered global map, shrine markers, landmarks, world seed, position, health, grenade counts, trophy state, altar progress, boss state, and elapsed time.
- Aggregate duplicate inventory entries by item name and symbol.
- Mark the player, shrine, boss, trophy, and hidden rooms on map views.

### Current command reference

| Command | Action |
| --- | --- |
| `W` `A` `S` `D` | Move |
| `E` | Use a health potion |
| `F` | Drop a grenade, or search when no grenade is available |
| `H` | Drop a holy grenade |
| `R` | Search for a secret wall |
| `K` | Kneel at the altar |
| `P` | Place altar offerings |
| `C` | Begin the boss summoning sequence |
| `M` | Open or close the paused map and inventory menu |
| Arrow keys | Scroll the map menu |
| `Y` / `N` | Confirm or cancel door and summoning prompts |
| `Q` | Quit |

### Deliberately not shipped yet

The following items remain future roadmap work rather than current product behaviour:

- JSON save and load.
- A separate `tutorial/` implementation with preserved lesson checkpoints.
- A fully exposed terminal attack command and a larger equipment/combat system.
- Configurable difficulty settings.
- A formal end-to-end seeded victory test covering every progression step.
- Packaging, distribution, and automated project-level lint/test configuration.

## Part 1: Playable Static Prototype

**Goal:** Build the smallest complete game loop before adding randomness or complex data models.

### 1. Terminal and room rendering

- Define the locked tile dimensions and geometry constants from `TASK.md`.
- Render one static 26 by 9 room that fits inside the five-by-five terminal viewport.
- Add assertions for tile height and line width.
- Keep rendering in a small, directly understandable function.

**Checkpoint:** Running the program displays one correctly aligned room.

### 2. Player and input

- Add a player position using local `x` and `y` coordinates.
- Draw the player as `@` over the room.
- Add `WASD` input and a simple game loop.
- Handle invalid commands without crashing.

**Checkpoint:** The player can move inside the room and the screen redraws after each command.

### 3. Collision and exit

- Add a single `can_move_to()` rule for walls and floor.
- Add an exit position and a win condition.
- Separate movement, rendering, input handling, and win checking.

**Checkpoint:** The player can reach the exit but cannot walk through walls.

### 4. Static multi-tile dungeon

- Introduce tile openings as data: `N`, `E`, `S`, and `W`.
- Implement room, straight corridor, corner, T-junction, cross, and dead-end geometry.
- Build a small hand-authored tile grid with several connected areas.
- Render neighbouring tiles without gaps or mismatched openings.
- Add connection validation for every adjacent tile pair.

**Milestone 1:** A complete static dungeon with rooms, corridors, junctions, player movement, collision, and an exit.

## Part 2: Tile and World Foundations

**Goal:** Replace prototype-specific code with reusable data structures while keeping the static game working.

### 5. Procedural tile renderer

- Generate room and corridor lines from geometry constants.
- Treat `kind` and `openings` as separate properties.
- Add a tile catalogue or factory for supported combinations.
- Test all tile types for dimensions and expected openings.

### 6. World model and coordinate helpers

- Introduce a tile-grid representation using `tile_map[y][x]`.
- Keep a five-by-five full-tile gameplay viewport centred on the player while room tiles shift around it.
- Reveal a 3x3 area around the player and keep unrevealed viewport positions masked as `~~~`.
- Open the complete discovered-world minimap only on demand.
- Add helpers for neighbours, directions, and translating between tile and local coordinates.
- Keep terrain separate from entities and overlays.
- Add explicit comments or documentation for tile coordinates versus local floor coordinates.

### 7. Connected dungeon generation

- Start with an empty tile grid and a selected start position.
- Grow a connected path or graph so reachability is guaranteed by construction.
- Classify nodes by their connected neighbours to choose straight, corner, T, cross, or dead-end geometry.
- Replace selected nodes with rooms.
- Add validation for bounds, connectivity, and matching openings.
- Use a seeded random generator during development so bugs can be reproduced.

**Checkpoint:** A new valid connected dungeon can be generated repeatedly without breaking the renderer or movement rules.

## Part 3: Exploration and Progression

**Goal:** Give the player reasons to explore the generated dungeon.

### 8. Game state and discovery

- Introduce a single game-state object or clearly structured state dictionary.
- Track visited tiles and the player position.
- Add start and exit rooms with placement rules.
- Add a basic minimap showing discovered areas and important landmarks.

### 9. Items and inventory

- Add a base item representation.
- Add pickup behaviour and an inventory list.
- Implement keys, potions, weapons, and treasure in small steps.
- Keep item placement separate from terrain generation.

### 10. Doors and keys

- Represent doors as overlays on existing valid connections.
- Support open, closed, and locked states.
- Add key identifiers and the rule for unlocking a matching door.
- Ensure collision and rendering both use the same door state.

### 11. Hidden rooms

- Add secret walls as stateful overlays rather than changing base terrain data.
- Add a search or discovery action.
- Reveal the entrance and make the hidden area reachable only after discovery.

**Milestone 2:** A replayable generated dungeon with rooms, dead ends, loops, items, keys, doors, an exit, and a minimap.

## Part 4: Enemies and Combat

**Goal:** Add a simple, predictable turn-based encounter system.

### 12. Monster entities

- Add monsters with position, name, HP, and damage.
- Store monsters separately from the dungeon.
- Render monsters as a layer above items and terrain.
- Prevent invalid placement on walls, locked doors, or occupied positions.

### 13. Turns and combat

- Define what counts as a player turn.
- Add a basic attack interaction and damage calculation.
- Let surviving monsters respond after the player acts.
- Remove defeated monsters and handle player death.
- Keep combat rules in `combat.py`, independent from terminal rendering.

### 14. Usable equipment

- Add weapons, armour, and potions using the existing inventory model.
- Keep the first version intentionally simple before adding critical hits or status effects.
- Add tests for damage, healing, defeat, and inventory consumption.

**Milestone 3:** The player can explore, collect equipment, fight monsters, lose HP, and survive or die.

## Part 5: Boss, Completion, and Persistence

**Goal:** Turn the prototype into a complete game with a deliberate ending.

### 15. Boss arena

- Reserve a 3 by 3 tile region during generation.
- Render it as one arena while retaining its world-grid placement.
- Give it limited entrances and place the boss encounter there.
- Optionally close the entrance during combat.
- Reward victory with an exit unlock, key, or treasure.

### 16. Full game completion

- Define the complete progression: start, exploration, locked route, boss, and exit.
- Add victory, defeat, and quit states.
- Add difficulty settings only after the default game is stable.
- Test complete runs using fixed random seeds.

### 17. Save and load

- Serialize plain game state to JSON.
- Save player, dungeon seed or generated map, inventory, doors, discoveries, monsters, and progression state.
- Validate loaded data before replacing the active game state.
- Keep file I/O out of gameplay and rendering functions.

**Milestone 4:** The game is a complete, replayable ASCII roguelike with procedural generation, combat, secrets, a boss, an exit, and save/load.

## Part 6: Reference-Game Quality Pass

Before building the tutorial, stabilize the reference implementation.

- Rename unclear functions and variables.
- Reduce duplicated logic and confirm module responsibilities.
- Add type hints only where they improve readability.
- Add tests for every invariant in `TASK.md`.
- Verify all tile dimensions and opening alignments.
- Verify generated maps are connected and contain required special rooms.
- Verify entities never overwrite terrain data.
- Verify the game can be played from a fresh start to victory.
- Add a short `game/README.md` explaining how the final architecture fits together.

The reference version should be understandable by reading one module at a time, but it may use classes and modules that are introduced later in the tutorial.

## Part 7: Tutorial Construction

Only begin this part after the reference game is playable and stable.

### Tutorial format

Each lesson should contain:

- A clear learning objective.
- The smallest new concept needed for that objective.
- A short implementation task.
- A runnable checkpoint.
- A few questions the learner should be able to answer.
- A comparison to the corresponding reference-game module.

### Tutorial sequence

Use the progression from `TASK.md`, adjusted to match the stable reference game:

1. Printing and strings: display one room.
2. Variables and coordinates: place `@`.
3. `input()` and conditionals: move with WASD.
4. Functions: isolate movement and collision.
5. Dictionaries: describe tile openings.
6. Loops and string construction: generate tile geometry.
7. Lists of lists: assemble a static tile map.
8. Randomness: generate a connected dungeon.
9. Lists and objects: add items and inventory.
10. State: add doors and keys.
11. Classes: introduce `Player`, `Tile`, `Item`, `Door`, and `Monster` when their need is visible.
12. Turn-based logic: add enemies and combat.
13. Exploration state: add secrets and a minimap.
14. Larger structures: add the boss room.
15. File I/O and JSON: add save/load.
16. Refactoring: compare the tutorial code with the final modular reference game.

Do not paste the final implementation into early lessons. Preserve the intermediate versions so the learner can see why each later abstraction was introduced.

## Definition of Done

The project is ready for tutorial work when:

- `game/` runs from a clean checkout with documented commands.
- A player can complete a generated dungeon from start to victory.
- Static and generated maps pass connection and dimension validation.
- Movement, items, doors, combat, boss behaviour, minimap, and save/load work together.
- Tests cover core rules and at least one seeded end-to-end game.
- The module boundaries are stable enough to explain.
- Every major feature has a corresponding tutorial lesson opportunity.

The tutorial is complete when a beginner can build a smaller but fully playable version from the lessons, explain the main systems, and use the finished `game/` implementation as a readable reference rather than a black box.
