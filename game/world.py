"""Graph-first infinite dungeon generation and exploration state."""

import random
from dataclasses import dataclass, field
from itertools import combinations

from .constants import TILE_HEIGHT, TILE_WIDTH
from .constants import WALL_SYMBOL
from .doors import DELTA as DOOR_DELTA, OPPOSITE as DOOR_OPPOSITE
from .tiles import OPENING_CELLS, DIRECTIONS, Tile, classify_openings, room_for_openings

WORLD_SIZE = 11
VIEWPORT_SIZE = 5
VISIBILITY_RADIUS = 1
START_TILE = (5, 5)
TILE_KINDS = ("room", "dead_end", "straight", "corner", "t_junction", "cross")
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}
DELTA = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def _direction_between(start: tuple[int, int], end: tuple[int, int]) -> str:
    delta = (end[0] - start[0], end[1] - start[1])
    return next(direction for direction, value in DELTA.items() if value == delta)


def generate_tiles(width: int, height: int, seed: int = 7) -> dict[tuple[int, int], Tile]:
    """Generate a finite graph for tests and examples using shared tile rules."""
    rng = random.Random(seed)
    positions = [(x, y) for y in range(height) for x in range(width)]
    connections = {position: set() for position in positions}

    # A serpentine path guarantees connectivity while keeping junctions rare.
    path: list[tuple[int, int]] = []
    if rng.random() < 0.5:
        rows = list(range(height))
        if rng.random() < 0.5:
            rows.reverse()
        for index, y in enumerate(rows):
            columns = list(range(width))
            if index % 2:
                columns.reverse()
            path.extend((x, y) for x in columns)
    else:
        columns = list(range(width))
        if rng.random() < 0.5:
            columns.reverse()
        for index, x in enumerate(columns):
            rows = list(range(height))
            if index % 2:
                rows.reverse()
            path.extend((x, y) for y in rows)

    for current, following in zip(path, path[1:]):
        direction = _direction_between(current, following)
        connections[current].add(direction)
        connections[following].add(OPPOSITE[direction])

    # Add occasional graph edges without allowing junctions to dominate.
    for x, y in positions:
        for direction in ("E", "S"):
            dx, dy = DELTA[direction]
            neighbour = (x + dx, y + dy)
            if neighbour not in connections:
                continue
            if len(connections[(x, y)]) <= 2 and len(connections[neighbour]) <= 2 and rng.random() < 0.12:
                connections[(x, y)].add(direction)
                connections[neighbour].add(OPPOSITE[direction])

    tiles = {}
    for position, openings in connections.items():
        neighbouring_openings = [
            connections[(position[0] + dx, position[1] + dy)]
            for dx, dy in DELTA.values()
            if (position[0] + dx, position[1] + dy) in connections
        ]
        tiles[position] = room_for_openings(
            openings,
            _kind_for(openings, rng, neighbouring_openings),
        )
    validate_connections(tiles, width, height)
    return tiles


def _kind_for(
    openings: set[str],
    rng: random.Random,
    neighbouring_openings: list[set[str]] | None = None,
) -> str:
    kind = classify_openings(openings)
    near_corridor_or_corner = any(
        len(neighbour_openings) == 2
        for neighbour_openings in neighbouring_openings or []
    )
    room_chance = 0.4 if near_corridor_or_corner else 0.2
    if len(openings) >= 2 and rng.random() < room_chance:
        return "room"
    return kind


def _choose_uniform_tile(
    fixed_openings: set[str],
    available_openings: set[str],
    rng: random.Random,
    room_bias: bool = False,
) -> tuple[str, set[str]]:
    """Choose a compatible tile kind uniformly, then choose its mask."""
    candidates: dict[str, list[set[str]]] = {kind: [] for kind in TILE_KINDS}
    available = sorted(available_openings)
    for size in range(len(available) + 1):
        for optional in combinations(available, size):
            openings = set(fixed_openings) | set(optional)
            if not openings and available:
                continue
            classified = classify_openings(openings)
            if classified in candidates:
                candidates[classified].append(openings)
            candidates["room"].append(openings)

    feasible_kinds = [kind for kind in TILE_KINDS if candidates[kind]]
    if not feasible_kinds:
        return "room", set(fixed_openings)
    if room_bias and "room" in feasible_kinds:
        feasible_kinds.append("room")
    kind = rng.choice(feasible_kinds)
    return kind, rng.choice(candidates[kind])


def validate_connections(tiles: dict[tuple[int, int], Tile], width: int, height: int) -> None:
    """Assert that every generated neighbouring tile agrees on its edge."""
    for (x, y), tile in tiles.items():
        for direction, (dx, dy) in DELTA.items():
            neighbour = (x + dx, y + dy)
            if neighbour in tiles:
                assert tile.is_open(direction) == tiles[neighbour].is_open(OPPOSITE[direction])


@dataclass
class WorldMap:
    """An infinite graph whose tiles are generated only when discovered."""

    width: int = WORLD_SIZE
    height: int = WORLD_SIZE
    seed: int | None = None
    discovered: set[tuple[int, int]] = field(default_factory=set)
    landmarks: dict[tuple[int, int], str] = field(default_factory=dict)
    connections: dict[tuple[int, int], set[str]] = field(init=False)
    tiles: dict[tuple[int, int], Tile] = field(init=False)

    def __post_init__(self) -> None:
        if self.seed is None:
            self.seed = random.SystemRandom().randrange(0, 2**32)
        self.connections = {START_TILE: set(DIRECTIONS)}
        self.tiles = {START_TILE: room_for_openings(set(DIRECTIONS), "room")}

    def _random_for(self, position: tuple[int, int]) -> random.Random:
        return random.Random(f"{self.seed}:{position[0]}:{position[1]}")

    def in_bounds(self, tile_x: int, tile_y: int) -> bool:
        return (tile_x, tile_y) in self.connections

    def ensure_tile(self, position: tuple[int, int], required_opening: str | None = None) -> Tile:
        """Create a tile and its opening mask from graph constraints."""
        if position in self.tiles:
            return self.tiles[position]

        rng = self._random_for(position)
        openings: set[str] = set()
        blocked: set[str] = set()
        x, y = position

        for direction, (dx, dy) in DELTA.items():
            neighbour = (x + dx, y + dy)
            if neighbour not in self.connections:
                continue
            if OPPOSITE[direction] in self.connections[neighbour]:
                openings.add(direction)
            else:
                blocked.add(direction)

        if required_opening is not None:
            if required_opening in blocked:
                raise ValueError("A required graph opening conflicts with a known closed edge")
            openings.add(required_opening)

        available = set(DIRECTIONS) - openings - blocked
        room_bias = any(
            len(self.connections[neighbour]) == 2
            for direction, (dx, dy) in DELTA.items()
            for neighbour in [(x + dx, y + dy)]
            if neighbour in self.connections
        )
        chosen_kind, chosen_openings = _choose_uniform_tile(
            openings,
            available,
            rng,
            room_bias,
        )
        self.connections[position] = chosen_openings
        self.tiles[position] = room_for_openings(chosen_openings, chosen_kind)
        return self.tiles[position]

    def reveal_around(self, tile_x: int, tile_y: int) -> None:
        """Generate and reveal exactly the three-by-three area around a tile."""
        revealed_positions = []
        for y in range(tile_y - VISIBILITY_RADIUS, tile_y + VISIBILITY_RADIUS + 1):
            for x in range(tile_x - VISIBILITY_RADIUS, tile_x + VISIBILITY_RADIUS + 1):
                self.ensure_tile((x, y))
                self.discovered.add((x, y))
                revealed_positions.append((x, y))
        self._connect_discovered_tiles(revealed_positions)

    def _connect_discovered_tiles(self, positions: list[tuple[int, int]]) -> None:
        """Add graph edges until every newly revealed tile is in one component."""
        positions = list(dict.fromkeys(positions))
        scope = set(positions)
        graph = self.connection_graph()
        existing_reachable = {START_TILE}
        queue = [START_TILE]
        while queue:
            current = queue.pop()
            for neighbour in graph.get(current, set()):
                if neighbour in self.discovered and neighbour not in existing_reachable:
                    existing_reachable.add(neighbour)
                    queue.append(neighbour)
        roots = sorted(scope & existing_reachable)
        root = roots[0] if roots else min(scope)
        while True:
            graph = self.connection_graph()
            reachable = {root}
            queue = [root]
            while queue:
                current = queue.pop()
                for neighbour in graph.get(current, set()):
                    if neighbour in scope and neighbour not in reachable:
                        reachable.add(neighbour)
                        queue.append(neighbour)
            missing = [position for position in scope if position not in reachable]
            if not missing:
                return
            position = None
            neighbours = []
            for candidate in sorted(missing):
                candidate_neighbours = [
                    ((candidate[0] + dx, candidate[1] + dy), direction)
                    for direction, (dx, dy) in DELTA.items()
                    if (candidate[0] + dx, candidate[1] + dy) in reachable
                ]
                if candidate_neighbours:
                    position = candidate
                    neighbours = candidate_neighbours
                    break
            if not neighbours:
                raise RuntimeError("Unable to connect revealed dungeon tiles")
            neighbour, direction = neighbours[0]
            self._add_connection(neighbour, position, OPPOSITE[direction])

    def _add_connection(
        self,
        source: tuple[int, int],
        target: tuple[int, int],
        direction: str,
    ) -> None:
        """Add a reciprocal edge and refresh both tile opening masks."""
        self.connections[source].add(direction)
        self.connections[target].add(OPPOSITE[direction])
        for position in (source, target):
            tile = self.tiles[position]
            self.tiles[position] = Tile(tile.kind, frozenset(self.connections[position]))

    def can_cross(self, tile_x: int, tile_y: int, direction: str) -> bool:
        """Create and validate a graph edge in one direction."""
        position = (tile_x, tile_y)
        if position not in self.connections or direction not in self.connections[position]:
            return False
        dx, dy = DELTA[direction]
        neighbour = (tile_x + dx, tile_y + dy)
        self.ensure_tile(neighbour, OPPOSITE[direction])
        return OPPOSITE[direction] in self.connections[neighbour]

    def add_landmark(self, tile_x: int, tile_y: int, symbol: str) -> None:
        if len(symbol) != 1:
            raise ValueError("A landmark symbol must be one character")
        self.ensure_tile((tile_x, tile_y))
        self.landmarks[(tile_x, tile_y)] = symbol

    def create_special_region(
        self,
        center: tuple[int, int],
        width: int,
        height: int,
    ) -> set[tuple[int, int]]:
        """Create a fully connected rectangular region of room tiles."""
        left = center[0] - width // 2
        top = center[1] - height // 2
        positions = {
            (left + x, top + y)
            for y in range(height)
            for x in range(width)
        }
        for position in positions:
            openings = {
                direction
                for direction, (dx, dy) in DELTA.items()
                if (position[0] + dx, position[1] + dy) in positions
            }
            self.connections[position] = openings
            self.tiles[position] = room_for_openings(openings, "room")
            self.discovered.add(position)
        return positions

    def connection_graph(self) -> dict[tuple[int, int], set[tuple[int, int]]]:
        """Return graph edges whose openings exist on both tile sides."""
        graph = {position: set() for position in self.connections}
        for position, openings in self.connections.items():
            for direction in openings:
                dx, dy = DELTA[direction]
                neighbour = (position[0] + dx, position[1] + dy)
                if neighbour in self.connections and OPPOSITE[direction] in self.connections[neighbour]:
                    graph[position].add(neighbour)
        return graph

    def _cell(
        self,
        x: int,
        y: int,
        player_tile: tuple[int, int],
        shrine_tiles=None,
    ) -> str:
        if (x, y) == player_tile:
            return "[@]"
        if (x, y) not in self.discovered:
            return "~~~"
        if (x, y) in self.landmarks:
            return f"[{self.landmarks[(x, y)]}]"
        if shrine_tiles is not None and (x, y) in shrine_tiles:
            return "[S]"
        return "[ ]"

    def render_viewport(
        self,
        player_tile: tuple[int, int],
        player_local: tuple[int, int],
        exit_local=None,
        exit_tile=None,
        items=None,
        doors=None,
        secret_walls=None,
        obstacles=None,
        monsters=None,
        grenades=None,
        explosions=None,
        special_regions=None,
        altar_tile=None,
        altar_position=None,
        viewport_tile=None,
    ) -> str:
        """Render discovered big tiles and fog for the rest of the 5x5 view."""
        player_x, player_y = player_tile
        camera_x, camera_y = viewport_tile or player_tile
        half_size = VIEWPORT_SIZE // 2
        tile_rows = [["~"] * (VIEWPORT_SIZE * TILE_WIDTH) for _ in range(VIEWPORT_SIZE * TILE_HEIGHT)]

        for viewport_y, world_y in enumerate(range(camera_y - half_size, camera_y + half_size + 1)):
            for viewport_x, world_x in enumerate(range(camera_x - half_size, camera_x + half_size + 1)):
                position = (world_x, world_y)
                if position not in self.discovered:
                    continue
                rendered = self.render_region_tile(position, special_regions or ())
                for local_y, row in enumerate(rendered):
                    start = viewport_x * TILE_WIDTH
                    tile_rows[viewport_y * TILE_HEIGHT + local_y][start:start + TILE_WIDTH] = row

        centre_start_x = half_size * TILE_WIDTH
        centre_start_y = half_size * TILE_HEIGHT
        if exit_local is not None and exit_tile is not None:
            exit_x, exit_y = exit_local
            exit_view_x = (exit_tile[0] - camera_x + half_size) * TILE_WIDTH + exit_x
            exit_view_y = (exit_tile[1] - camera_y + half_size) * TILE_HEIGHT + exit_y
            if 0 <= exit_view_y < len(tile_rows) and 0 <= exit_view_x < len(tile_rows[0]):
                tile_rows[exit_view_y][exit_view_x] = "E"
        for door in (doors or {}).values():
            if not door.locked:
                continue
            for tile_position, direction in (
                ((door.tile_x, door.tile_y), door.direction),
                (
                    (
                        door.tile_x + DOOR_DELTA[door.direction][0],
                        door.tile_y + DOOR_DELTA[door.direction][1],
                    ),
                    DOOR_OPPOSITE[door.direction],
                ),
            ):
                viewport_x = tile_position[0] - camera_x + half_size
                viewport_y = tile_position[1] - camera_y + half_size
                if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                    continue
                glyph = "-" if direction in ("N", "S") else "|"
                for local_x, local_y in OPENING_CELLS[direction]:
                    tile_rows[
                        viewport_y * TILE_HEIGHT + local_y
                    ][viewport_x * TILE_WIDTH + local_x] = glyph
        for wall in (secret_walls or {}).values():
            if wall.found:
                continue
            for tile_position, direction in (
                ((wall.tile_x, wall.tile_y), wall.direction),
                (
                    wall.hidden_tile,
                    wall.opposite_direction,
                ),
            ):
                viewport_x = tile_position[0] - camera_x + half_size
                viewport_y = tile_position[1] - camera_y + half_size
                if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                    continue
                for local_x, local_y in OPENING_CELLS[direction]:
                    tile_rows[
                        viewport_y * TILE_HEIGHT + local_y
                    ][viewport_x * TILE_WIDTH + local_x] = "#"
        for explosion in explosions or ():
            viewport_x = explosion.tile_x - camera_x + half_size
            viewport_y = explosion.tile_y - camera_y + half_size
            if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                continue
            if explosion.holy:
                horizontal_start = viewport_y * TILE_HEIGHT + explosion.y - 1
                for y in range(horizontal_start, horizontal_start + 3):
                    if 0 <= y < len(tile_rows):
                        tile_rows[y] = ["%"] * len(tile_rows[y])
                vertical_start = viewport_x * TILE_WIDTH + explosion.x - 2
                for y in range(len(tile_rows)):
                    for x in range(vertical_start, vertical_start + 5):
                        if 0 <= x < len(tile_rows[y]):
                            tile_rows[y][x] = "%"
                continue
            tile = self.ensure_tile((explosion.tile_x, explosion.tile_y)).render()
            for local_x in range(explosion.x - 2, explosion.x + 3):
                for local_y in range(explosion.y - 1, explosion.y + 2):
                    if (
                        0 <= local_y < TILE_HEIGHT
                        and 0 <= local_x < TILE_WIDTH
                        and tile[local_y][local_x] != "#"
                    ):
                        tile_rows[
                            viewport_y * TILE_HEIGHT + local_y
                        ][viewport_x * TILE_WIDTH + local_x] = "%"
        for grenade in grenades or ():
            viewport_x = grenade.tile_x - camera_x + half_size
            viewport_y = grenade.tile_y - camera_y + half_size
            if 0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE:
                tile_rows[
                    viewport_y * TILE_HEIGHT + grenade.y
                ][viewport_x * TILE_WIDTH + grenade.x] = "+" if grenade.flash % 2 == 0 else "O"
        for obstacle in obstacles or ():
            viewport_x = obstacle.tile_x - camera_x + half_size
            viewport_y = obstacle.tile_y - camera_y + half_size
            if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                continue
            tile_rows[
                viewport_y * TILE_HEIGHT + obstacle.y
            ][viewport_x * TILE_WIDTH + obstacle.x] = "X"
        for monster in monsters or ():
            body = monster.tail + [monster.position]
            for tile_x, tile_y, local_x, local_y in body:
                viewport_x = tile_x - camera_x + half_size
                viewport_y = tile_y - camera_y + half_size
                if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                    continue
                symbol = (
                    monster.head_symbol
                    if (tile_x, tile_y, local_x, local_y) == monster.position
                    else monster.symbol
                )
                size = 2 if monster.is_boss else 1
                for block_y in range(local_y, local_y + size):
                    for block_x in range(local_x, local_x + size):
                        if 0 <= block_y < TILE_HEIGHT and 0 <= block_x < TILE_WIDTH:
                            tile_rows[
                                viewport_y * TILE_HEIGHT + block_y
                            ][viewport_x * TILE_WIDTH + block_x] = symbol
        if altar_tile in self.discovered if altar_tile is not None else False:
            viewport_x = altar_tile[0] - camera_x + half_size
            viewport_y = altar_tile[1] - camera_y + half_size
            if 0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE:
                altar_x, altar_y = altar_position
                table = "T===T"
                start_x = viewport_x * TILE_WIDTH + altar_x - 2
                row = tile_rows[viewport_y * TILE_HEIGHT + altar_y]
                for offset, symbol in enumerate(table):
                    if 0 <= start_x + offset < len(row):
                        row[start_x + offset] = symbol
        for item in items or ():
            if (item.tile_x, item.tile_y) not in self.discovered:
                continue
            viewport_x = item.tile_x - camera_x + half_size
            viewport_y = item.tile_y - camera_y + half_size
            if not (0 <= viewport_x < VIEWPORT_SIZE and 0 <= viewport_y < VIEWPORT_SIZE):
                continue
            tile_rows[
                viewport_y * TILE_HEIGHT + item.y
            ][viewport_x * TILE_WIDTH + item.x] = item.symbol
        local_x, local_y = player_local
        player_view_x = (player_x - camera_x + half_size) * TILE_WIDTH + local_x
        player_view_y = (player_y - camera_y + half_size) * TILE_HEIGHT + local_y
        if 0 <= player_view_y < len(tile_rows) and 0 <= player_view_x < len(tile_rows[0]):
            tile_rows[player_view_y][player_view_x] = "@"
        return "\n".join("".join(row) for row in tile_rows)

    def render_region_tile(
        self,
        position: tuple[int, int],
        special_regions,
    ) -> list[list[str]]:
        """Render a tile as part of a seamless multi-tile room."""
        tile = self.ensure_tile(position)
        region = next((region for region in special_regions if position in region), None)
        if region is None:
            return tile.render()
        rows = [[" "] * TILE_WIDTH for _ in range(TILE_HEIGHT)]
        left, right, top, bottom = (
            (TILE_WIDTH - 10) // 2,
            (TILE_WIDTH - 10) // 2 + 10,
            (TILE_HEIGHT - 5) // 2,
            (TILE_HEIGHT - 5) // 2 + 5,
        )
        for direction, (dx, dy) in DELTA.items():
            neighbour = (position[0] + dx, position[1] + dy)
            if neighbour in region:
                continue
            if direction == "N":
                for x in range(TILE_WIDTH):
                    if not tile.is_open(direction) or not left <= x < right:
                        rows[0][x] = WALL_SYMBOL
            elif direction == "S":
                for x in range(TILE_WIDTH):
                    if not tile.is_open(direction) or not left <= x < right:
                        rows[-1][x] = WALL_SYMBOL
            elif direction == "W":
                for y in range(TILE_HEIGHT):
                    if not tile.is_open(direction) or not top <= y < bottom:
                        rows[y][0] = WALL_SYMBOL
                    if not tile.is_open(direction) or not top <= y < bottom:
                        rows[y][1] = WALL_SYMBOL
            else:
                for y in range(TILE_HEIGHT):
                    if not tile.is_open(direction) or not top <= y < bottom:
                        rows[y][-1] = WALL_SYMBOL
                        rows[y][-2] = WALL_SYMBOL
        return rows

    def render_minimap(self, player_tile: tuple[int, int], shrine_tiles=None) -> str:
        """Render only the discovered portion of the infinite world."""
        known = self.discovered | {player_tile}
        min_x = min(x for x, _ in known)
        max_x = max(x for x, _ in known)
        min_y = min(y for _, y in known)
        max_y = max(y for _, y in known)
        return "\n".join(
            "".join(
                self._cell(x, y, player_tile, shrine_tiles)
                for x in range(min_x, max_x + 1)
            )
            for y in range(min_y, max_y + 1)
        )

    def render_minimap_window(
        self,
        player_tile: tuple[int, int],
        size: int,
        scroll_x: int = 0,
        scroll_y: int = 0,
        shrine_tiles=None,
    ) -> str:
        """Render a square minimap window centered on the player by default."""
        half_size = size // 2
        player_x, player_y = player_tile
        min_x = player_x - half_size + scroll_x
        min_y = player_y - half_size + scroll_y
        return "\n".join(
            "".join(
                self._cell(x, y, player_tile, shrine_tiles)
                for x in range(min_x, min_x + size)
            )
            for y in range(min_y, min_y + size)
        )
