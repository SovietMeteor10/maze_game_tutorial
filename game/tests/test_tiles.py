import unittest
from collections import Counter, deque

from game.constants import TILE_HEIGHT, TILE_WIDTH
from game.constants import WALL_SYMBOL
from game.tiles import TILE_CATALOGUE, opening_cells
from game.world import DELTA, OPPOSITE, _kind_for, generate_tiles, validate_connections
from game.world import WorldMap


class TileCatalogueTests(unittest.TestCase):
    def test_rooms_are_more_likely_near_corridors_or_corners(self):
        class FixedRandom:
            def random(self):
                return 0.3

        openings = {"N", "S"}

        self.assertEqual(_kind_for(openings, FixedRandom()), "straight")
        self.assertEqual(
            _kind_for(openings, FixedRandom(), [{"N", "S"}]),
            "room",
        )

    def test_catalogue_contains_every_big_tile_kind(self):
        expected_kinds = {
            "room",
            "dead_end",
            "straight",
            "corner",
            "t_junction",
            "cross",
        }

        self.assertEqual(set(TILE_CATALOGUE), expected_kinds)
        self.assertTrue(all(TILE_CATALOGUE[kind] for kind in expected_kinds))

    def test_every_catalogue_tile_has_the_locked_dimensions(self):
        for tiles in TILE_CATALOGUE.values():
            for tile in tiles:
                rendered = tile.render()
                self.assertEqual(len(rendered), TILE_HEIGHT)
                self.assertTrue(all(len(row) == TILE_WIDTH for row in rendered))

    def test_every_opening_is_a_clear_boundary(self):
        for tiles in TILE_CATALOGUE.values():
            for tile in tiles:
                rendered = tile.render()
                for direction in tile.openings:
                    for x, y in opening_cells(direction):
                        self.assertNotEqual(rendered[y][x], WALL_SYMBOL)

    def test_closed_boundaries_remain_walls_in_corridor_tiles(self):
        for tiles in TILE_CATALOGUE.values():
            for tile in tiles:
                rendered = tile.render()
                for direction in set(("N", "E", "S", "W")) - tile.openings:
                    for x, y in opening_cells(direction):
                        self.assertEqual(rendered[y][x], WALL_SYMBOL)

    def test_generated_world_connections_match(self):
        tiles = generate_tiles(11, 11, seed=7)
        validate_connections(tiles, 11, 11)

    def test_generated_world_is_reachable_and_prefers_fewer_openings(self):
        tiles = generate_tiles(11, 11, seed=7)
        start = (0, 0)
        reached = {start}
        queue = deque([start])

        while queue:
            position = queue.popleft()
            for direction, (dx, dy) in DELTA.items():
                neighbour = (position[0] + dx, position[1] + dy)
                if (
                    neighbour in tiles
                    and tiles[position].is_open(direction)
                    and tiles[neighbour].is_open(OPPOSITE[direction])
                    and neighbour not in reached
                ):
                    reached.add(neighbour)
                    queue.append(neighbour)

        self.assertEqual(len(reached), len(tiles))
        opening_counts = Counter(len(tile.openings) for tile in tiles.values())
        self.assertGreater(
            opening_counts[1] + opening_counts[2], opening_counts[3] + opening_counts[4]
        )

    def test_frontier_crossing_generates_a_reciprocal_tile(self):
        world = WorldMap(seed=7)
        boundary_position, direction = next(
            (
                (position, direction)
                for position, tile in world.tiles.items()
                for direction in ("N", "E", "S", "W")
                if tile.is_open(direction)
                and (
                    position[0] + DELTA[direction][0],
                    position[1] + DELTA[direction][1],
                )
                not in world.tiles
            )
        )
        next_position = (
            boundary_position[0] + DELTA[direction][0],
            boundary_position[1] + DELTA[direction][1],
        )

        self.assertTrue(world.can_cross(*boundary_position, direction))
        self.assertIn(next_position, world.tiles)
        self.assertTrue(world.tiles[next_position].is_open(OPPOSITE[direction]))

    def test_revealing_new_area_creates_big_tiles_with_valid_connections(self):
        world = WorldMap(seed=7)
        world.reveal_around(20, 20)

        self.assertEqual(len(world.discovered), 9)
        for (x, y), tile in world.tiles.items():
            for direction, (dx, dy) in DELTA.items():
                neighbour = (x + dx, y + dy)
                if neighbour in world.tiles:
                    self.assertEqual(
                        tile.is_open(direction),
                        world.tiles[neighbour].is_open(OPPOSITE[direction]),
                    )

    def test_revealed_tiles_are_connected_to_one_component(self):
        world = WorldMap(seed=7)
        world.reveal_around(5, 5)
        graph = world.connection_graph()
        reached = {(5, 5)}
        queue = [(5, 5)]
        while queue:
            position = queue.pop()
            for neighbour in graph[position]:
                if neighbour in world.discovered and neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)

        self.assertEqual(reached, world.discovered)

    def test_frontier_generates_a_reciprocal_entry(self):
        world = WorldMap(seed=7)
        position, direction = next(
            (
                (position, direction)
                for position, tile in world.tiles.items()
                for direction, (dx, dy) in DELTA.items()
                if tile.is_open(direction)
                and (position[0] + dx, position[1] + dy) not in world.tiles
            )
        )

        self.assertTrue(world.can_cross(*position, direction))
        dx, dy = DELTA[direction]
        next_position = (position[0] + dx, position[1] + dy)
        self.assertIn(OPPOSITE[direction], world.connections[next_position])

    def test_runtime_world_can_generate_arbitrarily_far_coordinates(self):
        world = WorldMap(seed=7)
        position = (1000, -1000)

        world.ensure_tile(position)
        self.assertIn(position, world.tiles)

    def test_world_exposes_a_graph_from_matching_openings(self):
        world = WorldMap(seed=7)
        graph = world.connection_graph()

        self.assertEqual(set(graph), set(world.tiles))
        self.assertTrue(
            all(neighbour in graph for links in graph.values() for neighbour in links)
        )


if __name__ == "__main__":
    unittest.main()
