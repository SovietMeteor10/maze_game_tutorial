"""Rules and state for the first playable game slice."""

import random
import time

from .constants import EXIT_SYMBOL, HORIZONTAL_MOVE_STEPS, PLAYER_SYMBOL, TILE_HEIGHT, TILE_WIDTH, WALL_SYMBOL
from .doors import DELTA as DOOR_DELTA, Door, edge_key
from .game_state import GameState
from .grenades import Explosion, Grenade
from .items import Item, RELIC_NAMES
from .monsters import Snake
from .obstacles import Obstacle
from .player import Player
from .room import build_room, is_floor, opening_bounds
from .secrets import SecretWall
from .tiles import OPENING_CELLS, room_for_openings
from .world import DELTA, OPPOSITE, WorldMap


class Game:
    """A generated room world with movement, items, and an inventory."""

    def __init__(self, seed: int | None = None) -> None:
        self.room = build_room()
        left, right, top, bottom = opening_bounds()
        player = Player(
            x=(left + right) // 2,
            y=(top + bottom) // 2,
        )
        world = WorldMap(seed=seed)
        self.state = GameState(player=player, world=world)
        self.state.shrine_tiles = {
            (player.tile_x + dx, player.tile_y + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
        }
        self.state.shrine_center = (player.tile_x, player.tile_y)
        self.world.add_landmark(self.player.tile_x, self.player.tile_y, "S")
        self.world.reveal_around(self.player.tile_x, self.player.tile_y)
        self.room = self.world.render_region_tile(
            (self.player.tile_x, self.player.tile_y),
            (self.state.shrine_tiles,),
        )
        self.item_rng = random.Random(self.world.seed)
        self.populated_tiles: set[tuple[int, int]] = set(self.state.shrine_tiles)
        self._place_obstacles(self.item_rng)
        self.show_minimap = False
        self.minimap_scroll_x = 0
        self.minimap_scroll_y = 0
        self.started_at = time.monotonic()
        self.paused_seconds = 0.0
        self.menu_started_at: float | None = None
        self.pending_door: Door | None = None
        self.pending_door_direction: str | None = None
        self.door_prompt_mode: str | None = None
        self.player_turns = 0
        self.last_snake_update = time.monotonic()
        self.snake_interval = 0.5
        self.last_effect_update = time.monotonic()
        self.last_summon_update = time.monotonic()
        self.effect_interval = 0.4
        self.event_message = ""

    @property
    def altar_slots(self) -> dict[str, Item]:
        return self.state.altar_slots

    @property
    def boss_room_size(self) -> tuple[int, int] | None:
        return self.state.boss_room_size

    @property
    def boss_active(self) -> bool:
        return self.state.boss_active

    @property
    def boss_health(self) -> int | None:
        bosses = [monster.hp for monster in self.monsters if monster.is_boss]
        return sum(bosses) if bosses else None

    def _holy_grenade_visible(self) -> bool:
        """Return whether a floor holy grenade is within the current viewport."""
        return any(
            item.kind == "holy_grenade"
            and abs(item.tile_x - self.player.tile_x) <= 2
            and abs(item.tile_y - self.player.tile_y) <= 2
            for item in self.items
        )

    def _ensure_key_room(self, possible_tiles: list[tuple[int, int]]) -> tuple[int, int]:
        """Choose or create a room with exactly one graph opening for the key."""
        key_rooms = [
            position for position in possible_tiles
            if self.world.tiles[position].kind == "room"
            and len(self.world.tiles[position].openings) == 1
        ]
        if key_rooms:
            return key_rooms[0]
        one_opening = [
            position for position in possible_tiles
            if len(self.world.tiles[position].openings) == 1
        ]
        if not one_opening:
            sources = list(dict.fromkeys(
                list(possible_tiles) + sorted(self.world.connections)
            ))
            for source in sources:
                if source not in self.world.connections:
                    continue
                openings = self.world.connections[source]
                for direction in openings:
                    dx, dy = DELTA[direction]
                    position = (source[0] + dx, source[1] + dy)
                    if position in self.world.tiles:
                        continue
                    known_neighbours = sum(
                        (position[0] + neighbour_dx, position[1] + neighbour_dy)
                        in self.world.connections
                        for neighbour_dx, neighbour_dy in DELTA.values()
                    )
                    if known_neighbours > 1:
                        continue
                    self.world.ensure_tile(position, OPPOSITE[direction])
                    self.world.connections[position] = {OPPOSITE[direction]}
                    self.world.tiles[position] = room_for_openings(
                        {OPPOSITE[direction]},
                        "room",
                    )
                    return position
            raise RuntimeError("Unable to create a one-opening key room")
        position = one_opening[0]
        tile = self.world.tiles[position]
        self.world.tiles[position] = type(tile)("room", tile.openings)
        return position

    def _random_floor_position(
        self,
        tile_position: tuple[int, int],
        rng: random.Random,
    ) -> tuple[int, int]:
        """Choose an interior floor coordinate instead of a doorway cell."""
        tile = self.world.tiles[tile_position]
        rendered = tile.render()
        doorway_cells = {
            cell for direction in tile.openings for cell in OPENING_CELLS[direction]
        }
        blocked_cells = {
            (obstacle.x, obstacle.y)
            for obstacle in self.obstacles
            if (obstacle.tile_x, obstacle.tile_y) == tile_position
        }
        floor_cells = [
            (x, y)
            for y, row in enumerate(rendered)
            for x, symbol in enumerate(row)
            if (
                symbol != WALL_SYMBOL
                and (x, y) not in doorway_cells
                and (x, y) not in blocked_cells
            )
        ]
        return rng.choice(floor_cells)

    def _random_item_position(
        self,
        tile_position: tuple[int, int],
        rng: random.Random,
    ) -> tuple[int, int]:
        """Choose an item cell that is not already occupied by another item."""
        tile = self.world.tiles[tile_position]
        occupied = {
            (item.x, item.y)
            for item in self.items
            if (item.tile_x, item.tile_y) == tile_position
        }
        rendered = tile.render()
        floor_cells = [
            (x, y)
            for y, row in enumerate(rendered)
            for x, symbol in enumerate(row)
            if symbol != WALL_SYMBOL and (x, y) not in occupied
        ]
        return rng.choice(floor_cells)

    def _populate_new_tiles(self, positions: set[tuple[int, int]]) -> None:
        """Randomly populate newly discovered rooms and corridors."""
        positions -= self.populated_tiles
        positions.discard((self.player.tile_x, self.player.tile_y))
        if not positions:
            return
        self._place_obstacles(self.item_rng)
        key_exists = any(item.kind == "key" for item in self.items + self.player.inventory)
        if not key_exists:
            key_tile = self._ensure_key_room(sorted(positions))
            if key_tile not in self.world.discovered:
                self.world.discovered.add(key_tile)
                positions.add(key_tile)
            self.state.items.append(
                Item(
                    *self._random_floor_position(key_tile, self.item_rng),
                    "Gold Key",
                    "key",
                    *key_tile,
                    key_id="gold",
                )
            )
            key_position = next(
                item.position[2:]
                for item in self.items
                if item.kind == "key" and (item.tile_x, item.tile_y) == key_tile
            )
            self._spawn_snake(key_tile, key_position)
        occupied_tiles = {(item.tile_x, item.tile_y) for item in self.items}
        for position in sorted(positions):
            if position in occupied_tiles or self.item_rng.random() >= 0.50:
                continue
            kind = self.item_rng.choice(
                ("potion", "treasure", "grenade_pouch", "grenade_pouch",
                 "grenade_pouch", "grenade_pouch", "grenade_pouch")
            )
            item_position = self._random_floor_position(position, self.item_rng)
            if kind == "treasure" and any(item.kind == "treasure" for item in self.items):
                kind = "potion"
            name = {
                "potion": "Health Potion",
                "treasure": "Trophy",
                "grenade_pouch": "Grenade Pouch",
            }[kind]
            item = Item(
                *item_position,
                name,
                kind,
                *position,
                symbol=EXIT_SYMBOL if kind == "treasure" else None,
                quantity=3 if kind == "grenade_pouch" else 1,
            )
            self.state.items.append(item)
            occupied_tiles.add(position)
            if kind == "treasure":
                self.trophy_tile = position
                self.trophy_position = item_position
                self.world.add_landmark(*position, "E")
            if (
                kind != "treasure"
                and self.world.tiles[position].kind == "room"
                and self.item_rng.random() < 0.10
                and not any(
                    (monster.tile_x, monster.tile_y) == position
                    for monster in self.monsters
                )
            ):
                self._spawn_snake(position, item_position)
        owned_relics = {
            item.name
            for item in self.items + self.player.inventory
            if item.kind == "relic"
        } | set(self.altar_slots)
        missing_relics = [name for name in RELIC_NAMES if name not in owned_relics]
        available = [position for position in sorted(positions) if position not in occupied_tiles]
        if missing_relics and available and self.item_rng.random() < 0.35:
            relic_name = self.item_rng.choice(missing_relics)
            relic_tile = self.item_rng.choice(available)
            relic_position = self._random_item_position(relic_tile, self.item_rng)
            self.state.items.append(
                Item(*relic_position, relic_name, "relic", *relic_tile)
            )
            occupied_tiles.add(relic_tile)
            owned_relics.add(relic_name)
        available = [position for position in sorted(positions) if position not in occupied_tiles]
        fallback_tile = sorted(positions)[0] if positions else None
        known_items = self.items + self.player.inventory
        grenade_count = sum(item.kind == "grenade_pouch" for item in known_items)
        if (available or fallback_tile is not None) and grenade_count < 3:
            grenade_tile = available.pop(0) if available else fallback_tile
            grenade_position = self._random_item_position(grenade_tile, self.item_rng)
            self.state.items.append(
                Item(*grenade_position, "Grenade Pouch", "grenade_pouch", *grenade_tile, quantity=3)
            )
            occupied_tiles.add(grenade_tile)
        self.populated_tiles.update(positions)

    @property
    def obstacles(self) -> set[Obstacle]:
        return self.state.obstacles

    @property
    def monsters(self) -> list[Snake]:
        return self.state.monsters

    @property
    def grenades(self) -> list[Grenade]:
        return self.state.grenades

    @property
    def explosions(self) -> list[Explosion]:
        return self.state.explosions

    def _spawn_snake(
        self,
        tile_position: tuple[int, int],
        key_position: tuple[int, int],
    ) -> None:
        if any(
            (monster.tile_x, monster.tile_y) == tile_position
            for monster in self.monsters
        ):
            return
        snake_position = self._random_floor_position(tile_position, self.item_rng)
        for _ in range(20):
            if snake_position != key_position:
                break
            snake_position = self._random_floor_position(tile_position, self.item_rng)
        tile = self.world.tiles[tile_position]
        floor_cells = {
            (x, y)
            for y, row in enumerate(tile.render())
            for x, symbol in enumerate(row)
            if symbol != WALL_SYMBOL and (x, y) != snake_position
        }
        tail_length = self.item_rng.randint(4, 7)
        tail = []
        occupied = {snake_position}
        previous = snake_position
        for _ in range(tail_length):
            candidates = [
                (previous[0] - 2, previous[1]),
                (previous[0] + 2, previous[1]),
                (previous[0], previous[1] - 1),
                (previous[0], previous[1] + 1),
            ]
            candidate = next(
                (cell for cell in candidates if cell in floor_cells and cell not in occupied),
                None,
            )
            if candidate is None:
                break
            tail.append((*tile_position, *candidate))
            occupied.add(candidate)
            previous = candidate
        if len(tail) < tail_length:
            remaining = [cell for cell in floor_cells if cell not in occupied]
            self.item_rng.shuffle(remaining)
            tail.extend(
                (*tile_position, *cell)
                for cell in remaining[: tail_length - len(tail)]
            )
        self.monsters.append(
            Snake(*snake_position, *tile_position, tail, tail_length)
        )

    def _spawn_boss(
        self,
        tile_position: tuple[int, int],
        arena_center: tuple[int, int] | None = None,
    ) -> None:
        """Place the giant snake in the centre of the summoned arena."""
        tile = self.world.tiles[tile_position]
        centre = (len(tile.render()[0]) // 2, len(tile.render()) // 2)
        tail = [
            (*tile_position, centre[0] - 4, centre[1]),
            (*tile_position, centre[0] - 2, centre[1]),
        ]
        center_tile = arena_center or tile_position
        cx, cy = center_tile
        route = (
            [(cx - 2, y) for y in range(cy - 2, cy + 3)]
            + [(x, cy + 2) for x in range(cx - 1, cx + 3)]
            + [(cx + 2, y) for y in range(cy + 1, cy - 3, -1)]
            + [(x, cy - 2) for x in range(cx + 1, cx - 2, -1)]
        )
        self.monsters.append(
            Snake(
                *centre,
                *tile_position,
                tail,
                max_tail_length=12,
                hp=100,
                symbol="b",
                head_symbol="B",
                speed=4.0,
                is_boss=True,
                boss_route=route,
                boss_route_index=route.index(tile_position),
                boss_route_direction=1,
            )
        )

    def _split_boss(self, boss: Snake) -> None:
        """Replace the wounded boss with two counter-rotating sub-bosses."""
        if self.state.boss_split or not boss.boss_route:
            return
        self.state.boss_split = True
        route = boss.boss_route
        first_index = boss.boss_route_index
        second_index = (first_index + len(route) // 2) % len(route)
        self.monsters.remove(boss)
        for route_index, direction in ((first_index, 1), (second_index, -1)):
            tile_x, tile_y = route[route_index]
            self.monsters.append(
                Snake(
                    13, 4, tile_x, tile_y, [],
                    max_tail_length=6,
                    hp=25,
                    symbol="b",
                    head_symbol="B",
                    speed=4.0,
                    is_boss=True,
                    is_subboss=True,
                    boss_route=route,
                    boss_route_index=route_index,
                    boss_route_direction=direction,
                )
            )

    def _spawn_boss_minion(self, tile_position: tuple[int, int]) -> None:
        """Spawn a fast small snake near the boss."""
        tile = self.world.tiles[tile_position]
        floor = [
            (x, y)
            for y, row in enumerate(tile.render())
            for x, symbol in enumerate(row)
            if symbol != WALL_SYMBOL
        ]
        occupied = {(monster.x, monster.y) for monster in self.monsters if (monster.tile_x, monster.tile_y) == tile_position}
        boss = next(
            (monster for monster in self.monsters if monster.is_boss and (monster.tile_x, monster.tile_y) == tile_position),
            None,
        )
        spawn_near = []
        if boss is not None:
            spawn_near = [
                (boss.x + dx, boss.y + dy)
                for dx, dy in ((-4, 0), (4, 0), (0, -2), (0, 2))
            ]
            occupied.update(
                (body_x, body_y)
                for body_tile_x, body_tile_y, body_x, body_y in boss.tail + [boss.position]
                if body_tile_x == tile_position[0] and body_tile_y == tile_position[1]
                for body_x in (body_x, body_x + 1)
                for body_y in (body_y, body_y + 1)
            )
        choices = [position for position in spawn_near if position in floor and position not in occupied]
        if not choices:
            choices = [position for position in floor if position not in occupied]
        if not choices:
            return
        x, y = self.item_rng.choice(choices)
        self.monsters.append(
            Snake(
                x, y, *tile_position, [], max_tail_length=2, hp=5,
                speed=1.5, is_boss_minion=True,
            )
        )

    def summon_boss_room(self) -> str:
        """Ask for confirmation before beginning the summoning ritual."""
        if not self.state.kneeling:
            return "Kneel before the altar first by pressing K."
        missing = self._altar_remaining()
        if missing:
            return "The altar is missing: " + ", ".join(missing) + "."
        if self.boss_room_size is not None:
            return "The boss room has already been summoned."
        self.state.summon_prompt = True
        return "Summon the giant snake? Press Y to confirm or N to cancel."

    def _begin_summoning(self) -> str:
        """Start the short altar animation before teleporting."""
        self.state.summon_prompt = False
        self.state.summon_animation_frames = 8
        self.last_summon_update = time.monotonic()
        return "The altar begins to glow. The summoning ritual has begun..."

    def _teleport_to_boss_room(self) -> str:
        """Teleport to a generated 5x5 arena after the ritual completes."""
        centre = (self.player.tile_x + 12, self.player.tile_y)
        self.state.boss_tiles = self.world.create_special_region(centre, 5, 5)
        self.state.boss_room_size = (5, 5)
        self.state.boss_center = centre
        self.state.items = [
            item for item in self.items
            if (item.tile_x, item.tile_y) not in self.state.boss_tiles
        ]
        self._spawn_boss_pickups(initial=True)
        self.state.boss_active = True
        self.player.tile_x, self.player.tile_y = centre
        self.player.x = len(self.world.tiles[centre].render()[0]) // 2
        self.player.y = len(self.world.tiles[centre].render()) // 2 + 2
        self.room = self.world.render_region_tile(centre, (self.state.boss_tiles,))
        corner = self.item_rng.choice(
            [
                (centre[0] - 2, centre[1] - 2),
                (centre[0] + 2, centre[1] - 2),
                (centre[0] - 2, centre[1] + 2),
                (centre[0] + 2, centre[1] + 2),
            ]
        )
        self._spawn_boss(corner, centre)
        self._spawn_boss_minion(corner)
        self._spawn_boss_minion(corner)
        self.world.add_landmark(*centre, "B")
        return "The altar flares. You are teleported to the boss room!"

    def _spawn_boss_pickups(self, initial: bool = False) -> None:
        """Keep only grenade resources available inside the boss arena."""
        if not self.state.boss_tiles:
            return
        existing = [item for item in self.items if (item.tile_x, item.tile_y) in self.state.boss_tiles]
        normal_count = sum(item.kind == "grenade_pouch" for item in existing)
        target_count = 5 if initial else 6
        for _ in range(max(0, target_count - normal_count)):
            tile = self.item_rng.choice(sorted(self.state.boss_tiles))
            x, y = self._random_item_position(tile, self.item_rng)
            self.state.items.append(
                Item(x, y, "Grenade Pouch", "grenade_pouch", *tile, quantity=3)
            )
        if initial or not any(item.kind == "holy_grenade" for item in existing):
            tile = self.state.boss_center or self.item_rng.choice(sorted(self.state.boss_tiles))
            x, y = (19, 5)
            occupied = {
                (item.x, item.y)
                for item in self.items
                if (item.tile_x, item.tile_y) == tile
            }
            if (x, y) in occupied:
                x, y = self._random_item_position(tile, self.item_rng)
            self.state.items.append(
                Item(x, y, "Holy Hand Grenade", "holy_grenade", *tile)
            )

    def place_relics_on_altar(self) -> str:
        """Place every carried relic when standing at the shrine altar."""
        if not self._near_altar():
            return "The altar is in the shrine room."
        if not self.state.kneeling:
            return "Press K to kneel before the altar."
        placed = []
        if not self.state.altar_key_placed:
            key = next(
                (item for item in self.player.inventory
                 if item.kind == "key" and item.key_id == "gold"),
                None,
            )
            if key is not None:
                self.player.inventory.remove(key)
                self.state.altar_key_placed = True
                placed.append("Gold Key")
        for name in RELIC_NAMES:
            if name in self.altar_slots:
                continue
            item = next((item for item in self.player.inventory if item.name == name), None)
            if item is not None:
                self.player.inventory.remove(item)
                self.altar_slots[name] = item
                placed.append(name)
        remaining = self._altar_remaining()
        if not placed:
            return "The altar still needs: " + ", ".join(remaining) + "."
        if not remaining:
            return "All five relics fill the altar. Press C to cast the spell."
        return "Placed: " + ", ".join(placed) + ". Remaining: " + ", ".join(remaining) + "."

    def _altar_remaining(self) -> list[str]:
        """Return the key and relic offerings still required by the altar."""
        remaining = [] if self.state.altar_key_placed else ["Gold Key"]
        remaining.extend(name for name in RELIC_NAMES if name not in self.altar_slots)
        return remaining

    def _near_altar(self) -> bool:
        """Return whether the player is beside the shrine altar."""
        if (self.player.tile_x, self.player.tile_y) != self.state.altar_tile:
            return False
        x, y = self.player.x, self.player.y
        altar_x, altar_y = self.state.altar_position
        return (
            (y in {altar_y - 1, altar_y + 1} and altar_x - 2 <= x <= altar_x + 2)
            or (x in {altar_x - 4, altar_x + 4} and y == altar_y)
        )

    def _place_obstacles(self, rng: random.Random) -> None:
        """Add visible X barriers only to rooms with connected remaining floor."""
        start = (self.player.tile_x, self.player.tile_y)
        eligible = [
            position for position in sorted(self.world.discovered)
            if position != start and self.world.tiles[position].kind == "room"
        ]
        for position in eligible:
            if rng.random() >= 1 / 8 or any(
                obstacle.tile_x == position[0] and obstacle.tile_y == position[1]
                for obstacle in self.obstacles
            ):
                continue
            tile = self.world.tiles[position]
            rendered = tile.render()
            candidates = [
                (x, y)
                for y, row in enumerate(rendered)
                for x, symbol in enumerate(row)
                if symbol != WALL_SYMBOL
                and (x, y) not in {
                    cell for direction in tile.openings for cell in OPENING_CELLS[direction]
                }
            ]
            rng.shuffle(candidates)
            for x, y in candidates:
                obstacle = Obstacle(position[0], position[1], x, y)
                if self._floor_is_connected(tile, {(x, y)}):
                    self.obstacles.add(obstacle)
                    break

    def _floor_is_connected(self, tile, blocked: set[tuple[int, int]]) -> bool:
        rendered = tile.render()
        floor = {
            (x, y)
            for y, row in enumerate(rendered)
            for x, symbol in enumerate(row)
            if symbol != WALL_SYMBOL and (x, y) not in blocked
        }
        if not floor:
            return False
        reached = {next(iter(floor))}
        queue = list(reached)
        while queue:
            x, y = queue.pop()
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                neighbour = (x + dx, y + dy)
                if neighbour in floor and neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)
        return reached == floor

    @property
    def player(self) -> Player:
        """Expose the player through the state object."""
        return self.state.player

    @property
    def world(self) -> WorldMap:
        """Expose the world through the state object."""
        return self.state.world

    @property
    def items(self) -> list[Item]:
        """Expose world items through the state object."""
        return self.state.items

    @property
    def doors(self) -> dict[tuple[int, int, str], Door]:
        return self.state.doors

    @property
    def secret_walls(self) -> dict[tuple[int, int, str], SecretWall]:
        return self.state.secret_walls

    @property
    def trophy_tile(self) -> tuple[int, int] | None:
        return self.state.trophy_tile

    @trophy_tile.setter
    def trophy_tile(self, value: tuple[int, int]) -> None:
        self.state.trophy_tile = value

    @property
    def trophy_position(self) -> tuple[int, int] | None:
        return self.state.trophy_position

    @trophy_position.setter
    def trophy_position(self, value: tuple[int, int]) -> None:
        self.state.trophy_position = value

    @property
    def trophy_collected(self) -> bool:
        return self.state.trophy_collected

    @trophy_collected.setter
    def trophy_collected(self, value: bool) -> None:
        self.state.trophy_collected = value

    @property
    def won(self) -> bool:
        return self.state.won

    @won.setter
    def won(self, value: bool) -> None:
        self.state.won = value

    @property
    def defeated(self) -> bool:
        return self.state.defeated

    @defeated.setter
    def defeated(self, value: bool) -> None:
        self.state.defeated = value

    @property
    def quit(self) -> bool:
        return self.state.quit

    @quit.setter
    def quit(self, value: bool) -> None:
        self.state.quit = value

    def can_move_to(self, x: int, y: int) -> bool:
        """Return whether the player can move to a floor coordinate."""
        if (self.player.tile_x, self.player.tile_y) == self.state.altar_tile:
            altar_x, altar_y = self.state.altar_position
            if altar_y == y and altar_x - 2 <= x <= altar_x + 2:
                return False
        player_tile = (self.player.tile_x, self.player.tile_y)
        if player_tile == self.state.shrine_center and y == 0 and x <= 1:
            return False
        terrain = (
            self.world.render_region_tile(
                player_tile,
                (self.state.shrine_tiles, self.state.boss_tiles),
            )
            if player_tile in self.state.shrine_tiles | self.state.boss_tiles
            else self.world.tiles[player_tile].render()
        )
        if not is_floor(terrain, x, y):
            return False
        return not any(
            obstacle.tile_x == self.player.tile_x
            and obstacle.tile_y == self.player.tile_y
            and obstacle.x == x
            and obstacle.y == y
            for obstacle in self.obstacles
        )

    def use_health_potion(self) -> str:
        """Use the first health potion in the inventory."""
        if self.player.hp >= self.player.max_hp:
            return "Your health is already full."
        potion = next(
            (item for item in self.player.inventory if item.kind == "potion"),
            None,
        )
        if potion is None:
            return "You have no health potion."
        self.player.inventory.remove(potion)
        self.player.hp = min(self.player.max_hp, self.player.hp + 5)
        return "You used a Health Potion."

    def drop_grenade(self) -> str:
        """Drop a grenade at the player's current floor position."""
        if self.player.grenades <= 0:
            return "You have no grenades."
        self.player.grenades -= 1
        self.grenades.append(
            Grenade(
                self.player.tile_x,
                self.player.tile_y,
                self.player.x,
                self.player.y,
            )
        )
        return "Grenade dropped."

    def drop_holy_grenade(self) -> str:
        """Drop a holy hand grenade at the player's current position."""
        if self.player.holy_grenades <= 0:
            return "You have no holy hand grenades."
        self.player.holy_grenades -= 1
        self.grenades.append(
            Grenade(
                self.player.tile_x,
                self.player.tile_y,
                self.player.x,
                self.player.y,
                holy=True,
            )
        )
        return "Holy hand grenade dropped."

    def update_snakes(self) -> None:
        """Move visible snakes every second player turn for turn-based callers."""
        self.player_turns += 1
        if self.player_turns % 2:
            return
        self._move_snakes_once()

    def update_realtime(self, now: float | None = None) -> bool:
        """Advance snakes and grenade effects from the real-time loop."""
        self.event_message = ""
        if self.show_minimap or self.defeated:
            self.last_snake_update = time.monotonic() if now is None else now
            self.last_effect_update = self.last_snake_update
            return False
        current = time.monotonic() if now is None else now
        changed = False
        if self.state.summon_animation_frames:
            elapsed = current - self.last_summon_update
            if elapsed >= 0.25:
                steps = min(self.state.summon_animation_frames, int(elapsed / 0.25))
                self.last_summon_update += steps * 0.25
                self.state.summon_animation_frames -= steps
                if self.state.summon_animation_frames:
                    self.event_message = "The altar flashes " + ("." * (8 - self.state.summon_animation_frames))
                else:
                    self.event_message = self._teleport_to_boss_room()
                changed = True
            return changed
        effect_elapsed = current - self.last_effect_update
        if effect_elapsed >= self.effect_interval:
            effect_steps = int(effect_elapsed / self.effect_interval)
            self.last_effect_update += effect_steps * self.effect_interval
            for _ in range(effect_steps):
                self._update_effects_tick()
            changed = True
        elapsed = current - self.last_snake_update
        if elapsed >= self.snake_interval:
            steps = int(elapsed / self.snake_interval)
            self.last_snake_update += steps * self.snake_interval
            for _ in range(steps):
                changed = self._move_snakes_once() or changed
        return changed

    def _update_effects_tick(self) -> None:
        """Advance grenade flashes and keep active explosion visuals alive."""
        active_explosions = []
        for explosion in self.explosions:
            explosion.remaining -= self.effect_interval
            if explosion.remaining > 0:
                active_explosions.append(explosion)
        self.state.explosions = active_explosions
        active_grenades = []
        for grenade in self.grenades:
            grenade.flash += 1
            if grenade.flash >= 6:
                self._explode(grenade)
            else:
                active_grenades.append(grenade)
        self.state.grenades = active_grenades

    def _explode(self, grenade: Grenade) -> None:
        """Apply ten damage and destruction rules to a local 5x3 zone."""
        zone = {
            (x, y)
            for x in range(grenade.x - 2, grenade.x + 3)
            for y in range(grenade.y - 1, grenade.y + 2)
        }
        grenade_global_x = grenade.tile_x * TILE_WIDTH + grenade.x
        grenade_global_y = grenade.tile_y * TILE_HEIGHT + grenade.y
        player_global_x = self.player.tile_x * TILE_WIDTH + self.player.x
        player_global_y = self.player.tile_y * TILE_HEIGHT + self.player.y
        holy_player_hit = grenade.holy and (
            abs(player_global_x - grenade_global_x) <= 2
            or abs(player_global_y - grenade_global_y) <= 1
        )
        if holy_player_hit or (
            not grenade.holy
            and (self.player.tile_x, self.player.tile_y) == (grenade.tile_x, grenade.tile_y)
            and (self.player.x, self.player.y) in zone
        ):
            self.player.hp = max(0, self.player.hp - (50 if grenade.holy else 10))
        defeated_snakes = 0
        for snake in self.monsters:
            body_cells = self._monster_body_cells(snake)
            holy_hit = grenade.holy and any(
                abs(tile_x * TILE_WIDTH + body_x - grenade_global_x) <= 2
                or abs(tile_y * TILE_HEIGHT + body_y - grenade_global_y) <= 1
                for tile_x, tile_y, body_x, body_y in body_cells
            )
            if holy_hit or (not grenade.holy and (snake.tile_x, snake.tile_y) == (grenade.tile_x, grenade.tile_y) and any(
                (body_x, body_y) in zone
                for _, _, body_x, body_y in body_cells
            )):
                snake.hp -= 50 if grenade.holy else 10
        wounded_boss = next(
            (snake for snake in self.monsters
             if snake.is_boss and not snake.is_subboss and 0 < snake.hp <= 50),
            None,
        )
        if wounded_boss is not None:
            self._split_boss(wounded_boss)
        living_snakes = len(self.monsters)
        defeated_monsters = [snake for snake in self.monsters if snake.hp <= 0]
        self.state.monsters = [snake for snake in self.monsters if snake.hp > 0]
        defeated_snakes = living_snakes - len(self.state.monsters)
        for snake in defeated_monsters:
            if not snake.is_boss:
                self._drop_snake_skull(snake)
        if self.state.boss_active and not any(snake.is_boss for snake in self.monsters):
            self.state.boss_active = False
            self.state.boss_defeated = True
            self.won = True
        destroyed_obstacles = {
            obstacle for obstacle in self.obstacles
            if (obstacle.tile_x, obstacle.tile_y) == (grenade.tile_x, grenade.tile_y)
            and (obstacle.x, obstacle.y) in zone
        }
        self.state.obstacles.difference_update(destroyed_obstacles)
        self.state.items = [
            item for item in self.items
            if item.kind == "key"
            or (item.tile_x, item.tile_y) != (grenade.tile_x, grenade.tile_y)
            or (item.x, item.y) not in zone
        ]
        self.explosions.append(
            Explosion(grenade.tile_x, grenade.tile_y, grenade.x, grenade.y, holy=grenade.holy)
        )
        if self.player.hp <= 0:
            self.defeated = True
            self.event_message = "You were caught in the explosion."
        elif defeated_snakes:
            self.event_message = f"Snake defeated. ({defeated_snakes})"
        else:
            self.event_message = "Explosion!"

    def _monster_body_cells(self, monster: Snake) -> list[tuple[int, int, int, int]]:
        """Return every occupied cell, expanding boss bodies to their 2x2 footprint."""
        cells = []
        for tile_x, tile_y, x, y in monster.tail + [monster.position]:
            size = 2 if monster.is_boss else 1
            cells.extend(
                (tile_x, tile_y, x + dx, y + dy)
                for dx in range(size)
                for dy in range(size)
            )
        return cells

    def _drop_snake_skull(self, snake: Snake) -> None:
        """Drop the unique Snake Skull relic when a regular snake dies."""
        already_owned = any(
            item.name == "Snake Skull"
            for item in self.items + self.player.inventory
        ) or "Snake Skull" in self.altar_slots
        if already_owned:
            return
        tile_position = (snake.tile_x, snake.tile_y)
        x, y = self._random_item_position(tile_position, self.item_rng)
        self.state.items.append(
            Item(x, y, "Snake Skull", "relic", *tile_position)
        )

    def _move_snakes_once(self) -> bool:
        """Move all snakes that can currently see the player."""
        moved = False
        if self.state.boss_active:
            self.state.boss_pickup_timer += 1
            if self.state.boss_pickup_timer % 4 == 0:
                self._spawn_boss_pickups()
        for snake in self.monsters:
            snake.movement_progress += snake.speed
            if snake.movement_progress < 1:
                continue
            snake.movement_progress -= 1
            if snake.is_boss:
                snake.spawn_timer += 1
                if snake.spawn_timer >= 4 and len(self.monsters) < 12:
                    snake.spawn_timer = 0
                    self._spawn_boss_minion((snake.tile_x, snake.tile_y))
            if (
                (self.player.tile_x, self.player.tile_y, self.player.x, self.player.y)
                in {
                    (tile_x, tile_y, body_x, body_y)
                    for tile_x, tile_y, body_x, body_y in self._monster_body_cells(snake)
                }
            ):
                self.player.hp = max(0, self.player.hp - (6 if snake.is_boss else 3))
                if self.player.hp <= 0:
                    self.defeated = True
                    self.event_message = "The snake defeated you."
                continue
            tile_distance_x = abs(snake.tile_x - self.player.tile_x)
            tile_distance_y = abs(snake.tile_y - self.player.tile_y)
            if not snake.is_boss and not snake.is_boss_minion and (tile_distance_x > 2 or tile_distance_y > 2):
                continue
            active = snake.is_boss_minion or (tile_distance_x <= 1 and tile_distance_y <= 1)
            next_position = (
                self._next_boss_position(snake)
                if snake.is_boss
                else self._next_snake_position(snake)
                if active
                else self._next_snake_patrol_position(snake)
            )
            if next_position is None and not snake.is_boss:
                next_position = self._next_snake_patrol_position(snake)
            if next_position is not None:
                old_position = snake.position
                snake.tail.insert(0, old_position)
                snake.tail = snake.tail[: snake.max_tail_length]
                snake.tile_x, snake.tile_y, snake.x, snake.y = next_position
                moved = True
                if snake.is_boss:
                    for _ in range(3):
                        next_step = self._next_boss_position(snake)
                        if next_step is None:
                            break
                        snake.tail.insert(0, snake.position)
                        snake.tail = snake.tail[: snake.max_tail_length]
                        snake.tile_x, snake.tile_y, snake.x, snake.y = next_step
            if (
                (self.player.tile_x, self.player.tile_y, self.player.x, self.player.y)
                in {
                    (tile_x, tile_y, body_x, body_y)
                    for tile_x, tile_y, body_x, body_y in self._monster_body_cells(snake)
                }
            ):
                damage = 6 if snake.is_boss else 3
                self.player.hp = max(0, self.player.hp - damage)
                if self.player.hp <= 0:
                    self.defeated = True
                    self.event_message = "The giant snake defeated you." if snake.is_boss else "The snake defeated you."
        return moved

    def attack(self) -> str:
        """Strike the nearest snake in the player's local room."""
        targets = [
            snake for snake in self.monsters
            if (snake.tile_x, snake.tile_y) == (self.player.tile_x, self.player.tile_y)
            and abs(snake.x - self.player.x) <= 2
            and abs(snake.y - self.player.y) <= 1
        ]
        if not targets:
            return "There is nothing in reach."
        target = min(
            targets,
            key=lambda snake: abs(snake.x - self.player.x) + abs(snake.y - self.player.y),
        )
        target.hp -= 10 if target.is_boss else 5
        if target.hp > 0:
            return f"You hit the {'giant snake' if target.is_boss else 'snake'} ({target.hp} hp left)."
        self.monsters.remove(target)
        if not target.is_boss:
            self._drop_snake_skull(target)
        if target.is_boss:
            self.state.boss_active = False
            self.state.boss_defeated = True
            self.won = True
            return "The giant snake is defeated!"
        return "A snake is defeated."

    def _next_snake_patrol_position(
        self,
        snake: Snake,
    ) -> tuple[int, int, int, int] | None:
        """Choose a valid local step so visible inactive snakes keep moving."""
        steps = ((-2, 0), (-1, 0), (1, 0), (2, 0), (0, -1), (0, 1))
        for offset in range(len(steps)):
            index = (snake.patrol_index + offset) % len(steps)
            dx, dy = steps[index]
            candidate = (snake.x + dx, snake.y + dy)
            if self._snake_can_occupy((snake.tile_x, snake.tile_y), *candidate, snake):
                snake.patrol_index = (index + 1) % len(steps)
                return snake.tile_x, snake.tile_y, *candidate
        return None

    def _room_distance(
        self,
        start: tuple[int, int],
        target: tuple[int, int],
    ) -> int:
        if start == target:
            return 0
        queue = [(start, 0)]
        reached = {start}
        graph = self.world.connection_graph()
        while queue:
            position, distance = queue.pop(0)
            for neighbour in graph.get(position, set()):
                if neighbour == target:
                    return distance + 1
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append((neighbour, distance + 1))
        return 999999

    def _next_snake_position(self, snake: Snake) -> tuple[int, int, int, int] | None:
        if snake.is_boss:
            return self._next_boss_position(snake)
        if snake.is_boss_minion:
            return self._next_boss_minion_position(snake)
        snake_tile = (snake.tile_x, snake.tile_y)
        player_tile = (self.player.tile_x, self.player.tile_y)
        if snake_tile == player_tile:
            return self._next_snake_local_position(snake)
        next_tile = self._next_room_on_path(
            snake_tile,
            player_tile,
            None if snake.is_boss_minion else player_tile,
        )
        if next_tile is None:
            return None
        direction = next(
            direction
            for direction, (dx, dy) in DOOR_DELTA.items()
            if (snake.tile_x + dx, snake.tile_y + dy) == next_tile
        )
        opening = OPENING_CELLS[direction]
        target_x, target_y = opening[len(opening) // 2]
        if (snake.x, snake.y) in opening:
            door = self._door_for(snake.tile_x, snake.tile_y, direction)
            if door is not None and door.locked:
                return None
            wall = self._secret_wall_for(snake.tile_x, snake.tile_y, direction)
            if wall is not None and not wall.found:
                return None
            opposite_opening = OPENING_CELLS[OPPOSITE[direction]]
            index = min(
                range(len(opposite_opening)),
                key=lambda index: abs(opposite_opening[index][1] - snake.y)
                + abs(opposite_opening[index][0] - snake.x),
            )
            x, y = opposite_opening[index]
            if not self._snake_can_occupy(next_tile, x, y, snake):
                return self._next_snake_patrol_position(snake)
            return next_tile[0], next_tile[1], x, y
        path_step = self._snake_local_path_step(snake, (target_x, target_y))
        return (
            (snake.tile_x, snake.tile_y, *path_step)
            if path_step is not None
            else self._next_snake_patrol_position(snake)
        )

    def _next_boss_minion_position(self, snake: Snake) -> tuple[int, int, int, int] | None:
        """Pathfind a boss minion directly toward the player without patrol fallback."""
        target = (self.player.x, self.player.y)
        if (snake.tile_x, snake.tile_y) != (self.player.tile_x, self.player.tile_y):
            return self._next_snake_position_without_minion_dispatch(snake)
        step = self._snake_local_path_step(snake, target)
        if step is not None:
            return snake.tile_x, snake.tile_y, *step
        for dx, dy in ((2, 0), (-2, 0), (0, 1), (0, -1)):
            candidate = (snake.x + dx, snake.y + dy)
            snake_tile = (snake.tile_x, snake.tile_y)
            rendered = (
                self.world.render_region_tile(snake_tile, (self.state.boss_tiles,))
                if snake_tile in self.state.boss_tiles
                else self.world.tiles[snake_tile].render()
            )
            if 0 <= candidate[1] < len(rendered) and 0 <= candidate[0] < len(rendered[0]):
                if rendered[candidate[1]][candidate[0]] != WALL_SYMBOL:
                    return snake.tile_x, snake.tile_y, *candidate
        return None

    def _next_snake_position_without_minion_dispatch(
        self,
        snake: Snake,
    ) -> tuple[int, int, int, int] | None:
        """Use the room graph for a minion that is not in the player's tile."""
        next_tile = self._next_room_on_path(
            (snake.tile_x, snake.tile_y),
            (self.player.tile_x, self.player.tile_y),
            None,
        )
        if next_tile is None:
            return None
        direction = next(
            direction for direction, (dx, dy) in DOOR_DELTA.items()
            if (snake.tile_x + dx, snake.tile_y + dy) == next_tile
        )
        opening = OPENING_CELLS[direction]
        if (snake.x, snake.y) in opening:
            opposite = OPENING_CELLS[OPPOSITE[direction]]
            x, y = opposite[len(opposite) // 2]
            return next_tile[0], next_tile[1], x, y
        step = self._snake_local_path_step(snake, opening[len(opening) // 2])
        return (snake.tile_x, snake.tile_y, *step) if step is not None else None
    def _next_snake_local_position(self, snake: Snake) -> tuple[int, int, int, int] | None:
        path_step = self._snake_local_path_step(snake, (self.player.x, self.player.y))
        return (
            (snake.tile_x, snake.tile_y, *path_step)
            if path_step is not None
            else self._next_snake_patrol_position(snake)
        )

    def _snake_local_path_step(
        self,
        snake: Snake,
        target: tuple[int, int],
    ) -> tuple[int, int] | None:
        """Return the first walkable step along a local floor path."""
        start = (snake.x, snake.y)
        if target == start:
            return None
        queue = [start]
        parent = {start: None}
        steps = ((-2, 0), (0, -1), (2, 0), (0, 1))
        while queue:
            current = queue.pop(0)
            if current == target:
                break
            for dx, dy in steps:
                neighbour = (current[0] + dx, current[1] + dy)
                if neighbour in parent:
                    continue
                if self._snake_can_occupy(
                    (snake.tile_x, snake.tile_y), *neighbour, snake
                ):
                    parent[neighbour] = current
                    queue.append(neighbour)
        if target not in parent:
            return None
        current = target
        while parent[current] != start:
            current = parent[current]
        return current

    def _next_boss_position(self, boss: Snake) -> tuple[int, int, int, int] | None:
        """Move one step along the boss arena's counter-clockwise perimeter."""
        if not boss.boss_route:
            return None
        current = (boss.tile_x, boss.tile_y)
        target = boss.boss_route[
            (boss.boss_route_index + boss.boss_route_direction) % len(boss.boss_route)
        ]
        direction = next(
            direction for direction, delta in DELTA.items()
            if (current[0] + delta[0], current[1] + delta[1]) == target
        ) if target != current else None
        if direction is None:
            boss.boss_route_index = (boss.boss_route_index + 1) % len(boss.boss_route)
            target = boss.boss_route[
                (boss.boss_route_index + boss.boss_route_direction) % len(boss.boss_route)
            ]
            direction = next(
                direction for direction, delta in DELTA.items()
                if (current[0] + delta[0], current[1] + delta[1]) == target
            )
        opening = OPENING_CELLS[direction]
        if (boss.x, boss.y) in opening:
            opposite = OPENING_CELLS[OPPOSITE[direction]]
            x, y = opposite[len(opposite) // 2]
            boss.boss_route_index = (
                boss.boss_route_index + boss.boss_route_direction
            ) % len(boss.boss_route)
            return target[0], target[1], x, y
        target_x, target_y = opening[len(opening) // 2]
        next_x, next_y = boss.x, boss.y
        if direction in {"E", "W"} and boss.y != target_y:
            next_y += 1 if target_y > boss.y else -1
        elif boss.x != target_x:
            if abs(target_x - boss.x) <= 2:
                next_x = target_x
            else:
                next_x += 2 if target_x > boss.x else -2
        elif boss.y != target_y:
            next_y += 1 if target_y > boss.y else -1
        candidate = (next_x, next_y)
        if not self._snake_can_occupy((boss.tile_x, boss.tile_y), *candidate, None):
            # The boss ignores its own trailing body while following the arena wall.
            rendered = self.world.render_region_tile(
                (boss.tile_x, boss.tile_y), (self.state.boss_tiles,)
            )
            if not (0 <= next_y < len(rendered) and 0 <= next_x < len(rendered[next_y])):
                return None
            if rendered[next_y][next_x] == WALL_SYMBOL:
                return None
        return boss.tile_x, boss.tile_y, next_x, next_y

    def _next_room_on_path(
        self,
        start: tuple[int, int],
        target: tuple[int, int],
        center: tuple[int, int] | None = None,
    ) -> tuple[int, int] | None:
        queue = [start]
        parent = {start: None}
        graph = self.world.connection_graph()
        while queue:
            position = queue.pop(0)
            if position == target:
                break
            for neighbour in graph.get(position, set()):
                if center is not None and (
                    abs(neighbour[0] - center[0]) > 1
                    or abs(neighbour[1] - center[1]) > 1
                ):
                    continue
                direction = next(
                    direction
                    for direction, (dx, dy) in DOOR_DELTA.items()
                    if (position[0] + dx, position[1] + dy) == neighbour
                )
                door = self._door_for(position[0], position[1], direction)
                if door is not None and door.locked:
                    continue
                wall = self._secret_wall_for(position[0], position[1], direction)
                if wall is not None and not wall.found:
                    continue
                if neighbour not in parent:
                    parent[neighbour] = position
                    queue.append(neighbour)
        if target not in parent:
            return None
        position = target
        while parent[position] != start:
            position = parent[position]
        return position

    def _snake_can_occupy(
        self,
        tile_position: tuple[int, int],
        x: int,
        y: int,
        moving_snake: Snake | None = None,
    ) -> bool:
        rendered = (
            self.world.render_region_tile(tile_position, (self.state.boss_tiles,))
            if tile_position in self.state.boss_tiles
            else self.world.tiles[tile_position].render()
        )
        if not (0 <= y < len(rendered) and 0 <= x < len(rendered[y])):
            return False
        if rendered[y][x] == WALL_SYMBOL:
            return False
        if any(
            body_tile_x == tile_position[0]
            and body_tile_y == tile_position[1]
            and body_x == x
            and body_y == y
            for monster in self.monsters
            for index, (body_tile_x, body_tile_y, body_x, body_y) in enumerate(
                monster.tail
            )
            if not (monster is moving_snake and index == len(monster.tail) - 1)
        ) or any(
            body_tile_x == tile_position[0]
            and body_tile_y == tile_position[1]
            and body_x == x
            and body_y == y
            for monster in self.monsters
            for body_tile_x, body_tile_y, body_x, body_y in [monster.position]
            if monster is not moving_snake
            or (body_x, body_y) != (moving_snake.x, moving_snake.y)
        ):
            return False
        return not any(
            obstacle.tile_x == tile_position[0]
            and obstacle.tile_y == tile_position[1]
            and obstacle.x == x
            and obstacle.y == y
            for obstacle in self.obstacles
        )

    def move_player(self, command: str) -> bool:
        """Move the player once, returning whether the move succeeded."""
        offsets = {
            "w": (0, -1),
            "a": (-1, 0),
            "s": (0, 1),
            "d": (1, 0),
        }
        if command not in offsets:
            return False

        dx, dy = offsets[command]
        steps = HORIZONTAL_MOVE_STEPS if dx else 1
        moved = False
        for _ in range(steps):
            if not self._move_one(dx, dy):
                break
            moved = True
        return moved

    def _move_one(self, dx: int, dy: int) -> bool:
        """Move one logical floor position, including room transitions."""
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if not (0 <= new_x < len(self.room[0]) and 0 <= new_y < len(self.room)):
            return self.move_to_neighbouring_tile(dx, dy)
        if not self.can_move_to(new_x, new_y):
            return False

        self.player.x = new_x
        self.player.y = new_y
        self._apply_snake_contact_damage()
        return True

    def _apply_snake_contact_damage(self) -> None:
        """Damage the player immediately when occupying a snake body cell."""
        player_position = (
            self.player.tile_x,
            self.player.tile_y,
            self.player.x,
            self.player.y,
        )
        for snake in self.monsters:
            if player_position not in self._monster_body_cells(snake):
                continue
            self.player.hp = max(0, self.player.hp - (6 if snake.is_boss else 3))
            if self.player.hp <= 0:
                self.defeated = True
                self.event_message = "The snake defeated you."
                return

    def _place_default_door(self) -> None:
        """Place a locked overlay at the frontier after a key is available."""
        start = (self.player.tile_x, self.player.tile_y)
        keys = [item for item in self.items if item.kind == "key"]
        if not keys or self.doors:
            return
        key = keys[0]
        seen_edges = set()
        for position in sorted(self.world.discovered):
            if position == start:
                continue
            tile = self.world.tiles[position]
            for direction, (dx, dy) in sorted(DOOR_DELTA.items()):
                neighbour = (position[0] + dx, position[1] + dy)
                edge = edge_key(*position, direction)
                if (
                    edge not in seen_edges
                    and tile.is_open(direction)
                    and neighbour not in self.world.discovered
                    and neighbour != start
                    and len(self.world.connections[position]) > 1
                ):
                    seen_edges.add(edge)
                    self.world.ensure_tile(neighbour, OPPOSITE[direction])
                    if not self._reachable_without_edge(key.tile_x, key.tile_y, edge):
                        continue
                    door = Door(*position, direction, key_id="gold")
                    self.state.doors[door.position] = door
                    return

    def _reachable_without_edge(
        self,
        target_x: int,
        target_y: int,
        blocked_edge: tuple[int, int, str],
    ) -> bool:
        """Return whether a target remains reachable when one edge is locked."""
        graph = self.world.connection_graph()
        start = (self.player.tile_x, self.player.tile_y)
        reached = {start}
        queue = [start]
        while queue:
            current = queue.pop()
            for neighbour in graph.get(current, set()):
                direction = next(
                    direction
                    for direction, (dx, dy) in DOOR_DELTA.items()
                    if (current[0] + dx, current[1] + dy) == neighbour
                )
                if edge_key(*current, direction) == blocked_edge:
                    continue
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)
        return (target_x, target_y) in reached

    def _door_for(self, tile_x: int, tile_y: int, direction: str) -> Door | None:
        return self.state.doors.get(edge_key(tile_x, tile_y, direction))

    def _secret_wall_for(self, tile_x: int, tile_y: int, direction: str) -> SecretWall | None:
        return self.state.secret_walls.get(edge_key(tile_x, tile_y, direction))

    def _place_default_secret_wall(self) -> None:
        """Place one searchable wall over a frontier connection."""
        start = (self.player.tile_x, self.player.tile_y)
        door_edges = set(self.doors)
        for position in sorted(self.world.discovered):
            if position == start or len(self.world.connections[position]) <= 1:
                continue
            for direction, (dx, dy) in sorted(DOOR_DELTA.items()):
                neighbour = (position[0] + dx, position[1] + dy)
                edge = edge_key(*position, direction)
                if (
                    edge in door_edges
                    or not self.world.tiles[position].is_open(direction)
                    or neighbour in self.world.discovered
                ):
                    continue
                self.world.ensure_tile(neighbour, OPPOSITE[direction])
                self.world.tiles[neighbour] = room_for_openings(
                    self.world.tiles[neighbour].openings,
                    "room",
                )
                wall = SecretWall(*position, direction)
                self.secret_walls[wall.position] = wall
                return

    def _can_cross_door(self, direction: str) -> tuple[bool, str | None]:
        door = self._door_for(self.player.tile_x, self.player.tile_y, direction)
        if door is None or not door.locked:
            return True, None
        self.pending_door = door
        self.pending_door_direction = direction
        if door.can_open(self.player.inventory):
            self.door_prompt_mode = "open"
        else:
            self.door_prompt_mode = "locked"
        return False, "A locked door blocks your path."

    def move_to_neighbouring_tile(self, dx: int, dy: int) -> bool:
        """Cross an open room edge and reveal the neighbouring world tile."""
        direction = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}[(dx, dy)]
        current_tile = (self.player.tile_x, self.player.tile_y)
        next_tile = (self.player.tile_x + dx, self.player.tile_y + dy)
        internal_boss_edge = (
            current_tile in self.state.boss_tiles
            and next_tile in self.state.boss_tiles
        )
        internal_shrine_edge = (
            current_tile in self.state.shrine_tiles
            and next_tile in self.state.shrine_tiles
            and not (
                current_tile == self.state.shrine_center
                and (self.player.x, self.player.y) in OPENING_CELLS[direction]
            )
            and not (
                current_tile == self.state.shrine_center
                and direction == "W"
                and self.player.y == 0
            )
        )
        internal_special_edge = internal_boss_edge or internal_shrine_edge
        if not internal_special_edge and (self.player.x, self.player.y) not in OPENING_CELLS[direction]:
            return False
        secret_wall = None if internal_special_edge else self._secret_wall_for(
            self.player.tile_x, self.player.tile_y, direction
        )
        if secret_wall is not None and not secret_wall.found:
            return False
        can_cross_door, _ = (True, None) if internal_special_edge else self._can_cross_door(direction)
        if not can_cross_door:
            return False
        if not internal_special_edge and not self.world.can_cross(
            self.player.tile_x, self.player.tile_y, direction
        ):
            return False

        next_tile_x = self.player.tile_x + dx
        next_tile_y = self.player.tile_y + dy
        if dx < 0:
            self.player.x = len(self.room[0]) - 1
        elif dx > 0:
            self.player.x = 0
        if dy < 0:
            self.player.y = len(self.room) - 1
        elif dy > 0:
            self.player.y = 0

        self.player.tile_x = next_tile_x
        self.player.tile_y = next_tile_y
        if internal_special_edge:
            self.room = self.world.render_region_tile(
                (next_tile_x, next_tile_y),
                (self.state.shrine_tiles, self.state.boss_tiles),
            )
            return True
        discovered_before = set(self.world.discovered)
        self.world.reveal_around(next_tile_x, next_tile_y)
        self.room = self.world.render_region_tile(
            (next_tile_x, next_tile_y),
            (self.state.shrine_tiles, self.state.boss_tiles),
        )
        new_positions = set(self.world.discovered) - discovered_before
        new_positions.add((next_tile_x, next_tile_y))
        self._populate_new_tiles(new_positions)
        self._place_default_door()
        self._place_default_secret_wall()
        return True

    def collect_trophy_if_present(self) -> bool:
        """Collect the trophy without ending the current game."""
        collected = self.collect_items_if_present()
        return any(item.kind == "treasure" for item in collected)

    def search(self) -> str:
        """Reveal a secret wall touching the player's current tile."""
        for wall in self.secret_walls.values():
            if wall.found:
                continue
            if (wall.tile_x, wall.tile_y) not in {
                (self.player.tile_x, self.player.tile_y),
                wall.hidden_tile,
            }:
                continue
            wall.found = True
            self.world.discovered.add(wall.hidden_tile)
            self._populate_new_tiles({wall.hidden_tile})
            self.world.add_landmark(*wall.hidden_tile, "H")
            self._place_default_door()
            return "You found a hidden room."
        return "You find no secret wall here."

    def collect_items_if_present(self) -> list[Item]:
        """Move items at the player's position into the player's inventory."""
        player_position = (
            self.player.tile_x,
            self.player.tile_y,
            self.player.x,
            self.player.y,
        )
        owned_relics = {
            item.name for item in self.player.inventory if item.kind == "relic"
        } | set(self.altar_slots)
        collected = []
        for item in self.items:
            if (
                (item.tile_x, item.tile_y) != player_position[:2]
                or item.y != player_position[3]
                or abs(item.x - player_position[2]) >= HORIZONTAL_MOVE_STEPS
                or item.kind == "relic" and item.name in owned_relics
            ):
                continue
            collected.append(item)
            if item.kind == "relic":
                owned_relics.add(item.name)
        if not collected:
            return []
        self.state.items = [item for item in self.items if item not in collected]
        self.player.inventory.extend(collected)
        self.player.grenades += sum(
            item.quantity
            for item in collected
            if item.kind == "grenade_pouch"
        )
        self.player.holy_grenades += sum(
            item.quantity for item in collected if item.kind == "holy_grenade"
        )
        if any(item.kind == "treasure" for item in collected):
            self.trophy_collected = True
        return collected

    def handle_command(self, command: str) -> str:
        """Apply a command and return a short message for the terminal."""
        command = command.strip().lower()
        if command == "q":
            self.quit = True
            return "Goodbye."
        if self.state.summon_prompt:
            if command == "n":
                self.state.summon_prompt = False
                return "The summoning is cancelled."
            if command == "y":
                return self._begin_summoning()
            return "Summon the giant snake? Press Y to confirm or N to cancel."
        if self.state.summon_animation_frames:
            return "The summoning ritual is in progress..."
        if self.pending_door is not None:
            if self.door_prompt_mode == "locked":
                if command == "n":
                    self.pending_door = None
                    self.pending_door_direction = None
                    self.door_prompt_mode = None
                    return "The locked door remains closed."
                return "The door is locked and you lack a key."
            if command == "n":
                self.pending_door = None
                self.pending_door_direction = None
                self.door_prompt_mode = None
                return "You leave the door closed."
            if command == "y":
                door = self.pending_door
                movement_command = {
                    "N": "w",
                    "E": "d",
                    "S": "s",
                    "W": "a",
                }[self.pending_door_direction]
                if not door.open(self.player.inventory):
                    self.pending_door = None
                    self.pending_door_direction = None
                    self.door_prompt_mode = None
                    return "The door is locked and you lack a key."
                self.pending_door = None
                self.pending_door_direction = None
                self.door_prompt_mode = None
                self.move_player(movement_command)
                collected = self.collect_items_if_present()
                if collected:
                    names = ", ".join(item.name for item in collected)
                    return f"Door opened. Picked up: {names}."
                return "You opened the door."
            return "Open the door? Press Y to open it or N to cancel."
        if command == "f":
            if self.player.grenades > 0:
                return self.drop_grenade()
            # R is the primary search binding; retain the old empty-hand
            # fallback so existing command-line sessions remain usable.
            return self.search()
        if command == "h":
            return self.drop_holy_grenade()
        if command == "r":
            return self.search()
        if command == "p":
            return self.place_relics_on_altar()
        if command == "c":
            return self.summon_boss_room()
        if command == "k":
            if self._near_altar():
                self.state.kneeling = True
                remaining = self._altar_remaining()
                return (
                    "You kneel before the altar. Remaining: "
                    + ", ".join(remaining)
                    + ". Press P to place items or C to cast."
                )
            return "There is nothing here to kneel before."
        if command == "e":
            return self.use_health_potion()
        if command == "m":
            if self.boss_active:
                return "The boss arena has no minimap."
            if self.show_minimap:
                self.paused_seconds += time.monotonic() - self.menu_started_at
                self.menu_started_at = None
                self.show_minimap = False
                return "Menu closed."
            self.menu_started_at = time.monotonic()
            self.minimap_scroll_x = 0
            self.minimap_scroll_y = 0
            self.show_minimap = True
            return "Menu opened."
        if self.show_minimap:
            scroll_offsets = {
                "up": (0, -1),
                "down": (0, 1),
                "left": (-1, 0),
                "right": (1, 0),
            }
            if command in scroll_offsets:
                dx, dy = scroll_offsets[command]
                self.minimap_scroll_x += dx
                self.minimap_scroll_y += dy
                return "Minimap scrolled."
            return "Menu open. Press M to return to the game."
        if command in {"w", "a", "s", "d"}:
            if self.move_player(command):
                collected = self.collect_items_if_present()
                if collected:
                    names = ", ".join(item.name for item in collected)
                    return f"Picked up: {names}."
                return "You moved."
            if self.pending_door is not None:
                if self.door_prompt_mode == "locked":
                    return "The door is locked and you lack a key."
                return "Open the door? Press Y to open it or N to cancel."
            direction = {"w": "N", "d": "E", "s": "S", "a": "W"}[command]
            secret_wall = self._secret_wall_for(self.player.tile_x, self.player.tile_y, direction)
            if secret_wall is not None and not secret_wall.found:
                return "A secret wall blocks your path. Press F to search."
            if command in {"w", "a", "s", "d"}:
                direction = {"w": "N", "d": "E", "s": "S", "a": "W"}[command]
                door = self._door_for(self.player.tile_x, self.player.tile_y, direction)
                if door is not None and door.locked:
                    return "The door is locked and you lack a key."
            return "A wall blocks your path."
        return "Use W, A, S, D to move, E potion, F grenade, R search, K kneel, P altar, C cast, or Q quit."

    def elapsed_seconds(self, now: float | None = None) -> float:
        """Return gameplay time, excluding time spent in the menu."""
        current_time = time.monotonic() if now is None else now
        if self.menu_started_at is not None:
            current_time = self.menu_started_at
        return max(0.0, current_time - self.started_at - self.paused_seconds)

    def formatted_time(self) -> str:
        """Return gameplay time as minutes and seconds."""
        total_seconds = int(self.elapsed_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def health_bar(self, width: int = 20) -> str:
        """Return the player's current health as an ASCII bar."""
        ratio = max(0.0, min(1.0, self.player.hp / self.player.max_hp))
        filled = round(width * ratio)
        return "[" + "#" * filled + "-" * (width - filled) + "]"

    def handle_key(self, key: int | str) -> str:
        """Apply one key event from the real-time terminal loop."""
        if isinstance(key, int):
            if self.show_minimap:
                arrow_commands = {259: "up", 258: "down", 260: "left", 261: "right"}
                if key in arrow_commands:
                    return self.handle_command(arrow_commands[key])
            key = chr(key)
        return self.handle_command(key)

    def render(self) -> str:
        """Return the full five-by-five tile viewport."""
        return self.world.render_viewport(
            (self.player.tile_x, self.player.tile_y),
            (self.player.x, self.player.y),
            self.trophy_position if not self.trophy_collected else None,
            self.trophy_tile if not self.trophy_collected else None,
            self.items,
            self.doors,
            self.secret_walls,
            self.obstacles,
            self.monsters,
            self.grenades,
            self.explosions,
            (self.state.shrine_tiles, self.state.boss_tiles),
            self.state.altar_tile,
            self.state.altar_position,
            self.state.boss_center if self.state.boss_active else None,
        )

    def render_current_room(self) -> str:
        """Return the current room with the player and exit layered on top."""
        rows = [row[:] for row in self.room]
        for item in self.items:
            if (item.tile_x, item.tile_y) == (self.player.tile_x, self.player.tile_y):
                rows[item.y][item.x] = item.symbol
        for door in self.doors.values():
            if not door.locked:
                continue
            if (door.tile_x, door.tile_y) == (self.player.tile_x, self.player.tile_y):
                glyph = "-" if door.direction in ("N", "S") else "|"
                for local_x, local_y in OPENING_CELLS[door.direction]:
                    rows[local_y][local_x] = glyph
        for wall in self.secret_walls.values():
            if wall.found:
                continue
            if (wall.tile_x, wall.tile_y) == (self.player.tile_x, self.player.tile_y):
                for local_x, local_y in OPENING_CELLS[wall.direction]:
                    rows[local_y][local_x] = WALL_SYMBOL
        for obstacle in self.obstacles:
            if (obstacle.tile_x, obstacle.tile_y) == (self.player.tile_x, self.player.tile_y):
                rows[obstacle.y][obstacle.x] = "X"
        for explosion in self.explosions:
            if (explosion.tile_x, explosion.tile_y) == (self.player.tile_x, self.player.tile_y):
                if explosion.holy:
                    for row in rows:
                        for x in range(explosion.x - 2, explosion.x + 3):
                            if 0 <= x < len(row):
                                row[x] = "%"
                    if 0 <= explosion.y < len(rows):
                        for y in range(explosion.y - 1, explosion.y + 2):
                            if 0 <= y < len(rows):
                                rows[y] = ["%"] * len(rows[y])
                    continue
                for x in range(explosion.x - 2, explosion.x + 3):
                    for y in range(explosion.y - 1, explosion.y + 2):
                        if 0 <= y < len(rows) and 0 <= x < len(rows[y]) and rows[y][x] != WALL_SYMBOL:
                            rows[y][x] = "%"
        for grenade in self.grenades:
            if (grenade.tile_x, grenade.tile_y) == (self.player.tile_x, self.player.tile_y):
                rows[grenade.y][grenade.x] = "+" if grenade.flash % 2 == 0 else "O"
        for monster in self.monsters:
            for tile_x, tile_y, local_x, local_y in monster.tail + [monster.position]:
                if (tile_x, tile_y) == (self.player.tile_x, self.player.tile_y):
                    symbol = (
                        monster.head_symbol
                        if (tile_x, tile_y, local_x, local_y) == monster.position
                        else monster.symbol
                    )
                    size = 2 if monster.is_boss else 1
                    for body_y in range(local_y, local_y + size):
                        for body_x in range(local_x, local_x + size):
                            if 0 <= body_y < len(rows) and 0 <= body_x < len(rows[body_y]):
                                rows[body_y][body_x] = symbol
        if (self.player.tile_x, self.player.tile_y) == self.state.altar_tile:
            altar_x, altar_y = self.state.altar_position
            for offset, symbol in enumerate("T===T"):
                if 0 <= altar_x - 2 + offset < len(rows[altar_y]):
                    rows[altar_y][altar_x - 2 + offset] = symbol
        rows[self.player.y][self.player.x] = PLAYER_SYMBOL
        return "\n".join("".join(row) for row in rows)

    def render_world_map(self) -> str:
        """Return the five-by-five gameplay viewport."""
        return self.render()

    def render_minimap(self) -> str:
        """Return the complete discovered map for the optional overlay."""
        return self.world.render_minimap(
            (self.player.tile_x, self.player.tile_y),
            self.state.shrine_tiles,
        )

    def render_minimap_window(self, size: int) -> str:
        """Return the square minimap window used by the menu."""
        return self.world.render_minimap_window(
            (self.player.tile_x, self.player.tile_y),
            size,
            self.minimap_scroll_x,
            self.minimap_scroll_y,
            self.state.shrine_tiles,
        )
