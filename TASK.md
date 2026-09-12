# Maze Game Project Document

## 1. Project overview

This project is a teaching-oriented Python maze / dungeon game designed to be built incrementally with a beginner.

The player explores a procedurally assembled dungeon made from a fixed set of compatible tiles. The dungeon contains corridors, junctions, rooms, doors, keys, items, enemies, hidden areas, boss rooms and an exit.

The important teaching principle is that the game should grow in stages. At every stage, the program should still run and be understandable. The project should introduce Python concepts naturally through the game rather than starting with abstractions for their own sake. This matches the existing architecture, which separates the dungeon data, game logic and rendering, and keeps the player and other entities separate from the underlying map. 

The eventual game should feel something like a small ASCII roguelike while remaining simple enough for a beginner to understand how every part works.

---

# 2. Teaching goals

The project should gradually introduce:

* variables
* strings
* printing
* `input()`
* `if / elif / else`
* lists
* nested lists
* loops
* functions
* dictionaries
* classes
* randomness
* coordinates
* simple graph ideas
* procedural generation
* state
* file I/O
* basic algorithms

The goal is not only to finish the game. It is to use the game to teach how a larger program can be decomposed into smaller, understandable systems.

A useful rule throughout the project is:

> If a beginner cannot explain what a piece of code is doing, we have probably introduced it too early.

---

# 3. High-level architecture

The project should be divided into four main layers:

```text
WORLD DATA
    ↓
GAME LOGIC
    ↓
GAME STATE
    ↓
RENDERING
```

The dungeon itself should not contain the player, monsters or items.

Instead:

```python
dungeon = [...]
player = Player(...)
monsters = [...]
items = [...]
doors = [...]
```

The renderer combines these pieces when displaying the game.

This prevents problems such as a monster overwriting the floor beneath it or the player accidentally destroying a wall tile. The original architecture already establishes this separation. 

---

# 4. Coordinate system

The dungeon is fundamentally a two-dimensional grid.

Use:

```python
dungeon[y][x]
```

rather than:

```python
dungeon[x][y]
```

This should be taught early because coordinate ordering is a common source of mistakes. 

Every large maze tile also occupies a coordinate in a higher-level tile grid:

```text
tile_map[y][x]
```

So there are effectively two coordinate systems:

```text
Tile coordinates
    ↓
ASCII / local coordinates inside each tile
```

Later, if needed, we can also distinguish:

```text
World coordinates
Tile coordinates
Screen coordinates
```

---

# 5. The tile system

## 5.1 Core idea

The dungeon is assembled from large, fixed-size tiles.

Every tile has exactly the same outer dimensions.

A tile may have an opening on any combination of:

```text
N = North
E = East
S = South
W = West
```

Each tile can therefore be represented as:

```python
{
    "N": True,
    "E": False,
    "S": True,
    "W": False
}
```

This example means:

```text
open north
closed east
open south
closed west
```

which creates a vertical path.

---

# 6. Standard tile geometry

We should lock this geometry and not alter it between tile types.

## Dimensions

```text
Width:  52 characters
Height: 21 rows
```

## Walls

```text
Top wall thickness:     3 rows
Bottom wall thickness:  3 rows

Left wall thickness:    6 characters
Right wall thickness:   6 characters
```

## Openings

North and south openings:

```text
10 characters wide
```

East and west openings:

```text
3 rows high
```

All openings are centred.

This means neighbouring tiles can always connect perfectly.

---

# 7. Standard room

This is the base room shape with all four sides open:

```text
#####################          #####################
#####################          #####################
#####################          #####################
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
                                                    
                                                    
                                                    
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
#####################          #####################
#####################          #####################
#####################          #####################
```

The internal chamber is deliberately wider in character count because terminal characters are taller than they are wide.

The result should therefore appear approximately square on screen.

---

# 8. Tile compatibility rule

Every opening must occupy exactly the same location.

If one tile has:

```text
E = True
```

then the tile immediately to its east must have:

```text
W = True
```

For example:

```text
Tile A               Tile B

E = True    ←→       W = True
```

This is valid.

But:

```text
Tile A               Tile B

E = True             W = False
```

is invalid because the first tile opens directly into a wall.

The dungeon generator should guarantee matching connections.

---

# 9. Corridor tiles

Corridors use the same 52 × 21 tile footprint but contain narrow passages rather than a large room.

There are two straight corridor types.

## 9.1 North-South corridor

```python
openings = {
    "N": True,
    "E": False,
    "S": True,
    "W": False
}
```

Conceptually:

```text
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
```

The ten-character gap continues vertically through the tile.

---

## 9.2 East-West corridor

```python
openings = {
    "N": False,
    "E": True,
    "S": False,
    "W": True
}
```

Conceptually:

```text
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
                                                    
                                                    
                                                    
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
```

The three-row opening continues horizontally through the tile.

---

# 10. Corner tiles

A corner joins two adjacent directions.

Rather than naming these "left" and "right", we name them after the directions they connect.

There are four.

## North-East

```python
corner_ne = {
    "N": True,
    "E": True,
    "S": False,
    "W": False
}
```

## East-South

```python
corner_es = {
    "N": False,
    "E": True,
    "S": True,
    "W": False
}
```

## South-West

```python
corner_sw = {
    "N": False,
    "E": False,
    "S": True,
    "W": True
}
```

## West-North

```python
corner_wn = {
    "N": True,
    "E": False,
    "S": False,
    "W": True
}
```

The internal corridor simply joins the relevant branches through the centre of the tile.

---

# 11. T-junction tiles

A T-junction has three open sides and one closed side.

There are four possible orientations.

## North-East-West

South closed:

```python
t_new = {
    "N": True,
    "E": True,
    "S": False,
    "W": True
}
```

## North-East-South

West closed:

```python
t_nes = {
    "N": True,
    "E": True,
    "S": True,
    "W": False
}
```

## East-South-West

North closed:

```python
t_esw = {
    "N": False,
    "E": True,
    "S": True,
    "W": True
}
```

## North-South-West

East closed:

```python
t_nsw = {
    "N": True,
    "E": False,
    "S": True,
    "W": True
}
```

---

# 12. Cross tile

The cross junction is open on all four sides.

```python
cross_nesw = {
    "N": True,
    "E": True,
    "S": True,
    "W": True
}
```

Conceptually:

```text
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
                                                    
                                                    
                                                    
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
#####################          #####################
```

---

# 13. Dead ends

We should also support one-ended corridor tiles.

These are useful for:

* treasure
* keys
* secrets
* traps
* dead ends
* small encounters

There are four.

```python
dead_end_n
dead_end_e
dead_end_s
dead_end_w
```

For example:

```python
dead_end_n = {
    "N": True,
    "E": False,
    "S": False,
    "W": False
}
```

These can later contain objects or encounters.

---

# 14. Room tiles

Rooms differ from corridors because the centre becomes a large open chamber.

The standard room uses this geometry:

```text
#####################          #####################
#####################          #####################
#####################          #####################
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
                                                    
                                                    
                                                    
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
#####################          #####################
#####################          #####################
#####################          #####################
```

A room may theoretically use any opening combination.

---

# 15. Room opening combinations

There are 16 possible combinations because each of four sides can independently be open or closed.

## No openings

```python
room_none
```

Useful mainly for special generation cases.

---

## One opening

```python
room_n
room_e
room_s
room_w
```

---

## Two opposite openings

```python
room_ns
room_ew
```

---

## Two adjacent openings

```python
room_ne
room_es
room_sw
room_wn
```

---

## Three openings

```python
room_new
room_nes
room_esw
room_nsw
```

---

## Four openings

```python
room_nesw
```

---

# 16. Difference between junctions and rooms

A cross corridor and four-door room technically have the same opening configuration:

```python
N = True
E = True
S = True
W = True
```

But visually they differ.

A cross corridor contains narrow paths:

```text
         |
         |
---------+---------
         |
         |
```

A room contains a large chamber:

```text
      doorway
         |
    +---------+
----|         |----
    |         |
    +---------+
         |
      doorway
```

Therefore the tile needs both:

```python
kind
```

and:

```python
openings
```

For example:

```python
Tile(
    kind="room",
    openings={"N": True, "E": True, "S": True, "W": True}
)
```

versus:

```python
Tile(
    kind="junction",
    openings={"N": True, "E": True, "S": True, "W": True}
)
```

---

# 17. Boss room

A boss room occupies a **3 × 3 block of ordinary tile positions**.

```text
+-------+-------+-------+
|       |       |       |
|   B   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   B   |   B   |   B   |
|       |       |       |
+-------+-------+-------+
```

Internally, however, the boundaries between those nine tiles disappear.

The result is one enormous arena.

Conceptually:

```text
+-----------------------+
|                       |
|                       |
|                       |
|                       |
|      BOSS ARENA       |
|                       |
|                       |
|                       |
|                       |
+-----------------------+
```

The boss room therefore occupies:

```python
width_tiles = 3
height_tiles = 3
```

Its external entrances may appear on any outer side.

Example:

```python
BossRoom(
    width_tiles=3,
    height_tiles=3,
    entrances=["S"]
)
```

Boss rooms should normally have fewer entrances than ordinary rooms so entering one feels deliberate.

---

# 18. Doors

Doors should be treated as something placed **inside an existing connection**, rather than a completely different tile.

A tile still has an opening:

```python
"N": True
```

but a door may occupy it.

For example:

```python
Tile(
    kind="room",
    openings={
        "N": True,
        "E": False,
        "S": True,
        "W": False
    },
    doors={
        "N": Door(locked=True)
    }
)
```

---

# 19. Door orientations

There are four door orientations:

```text
door_n
door_e
door_s
door_w
```

Their orientation depends on which wall they cross.

---

# 20. Door states

A door may be:

```text
open
closed
locked
```

A locked door may optionally require a specific key.

```python
class Door:
    def __init__(self, side, locked=False, key_id=None):
        self.side = side
        self.locked = locked
        self.key_id = key_id
```

Example:

```python
Door(
    side="N",
    locked=True,
    key_id="gold"
)
```

---

# 21. Door rendering

The previous game design uses a visual three-cell structure for doors rather than treating them as a single map character. 

For the new larger tile system, we can preserve the same principle.

A vertical doorway might conceptually contain:

```text
|
X
|
```

where:

```text
| = door frame
X = lock
```

Once unlocked:

```text
|
 
|
```

The opening itself remains part of the geometry.

Only the blocking lock disappears.

---

# 22. Keys

Keys are items.

```python
class Key:
    def __init__(self, key_id):
        self.key_id = key_id
```

Example:

```python
gold_key = Key("gold")
```

A door may then require:

```python
door.key_id == "gold"
```

If the player owns a matching key:

```python
door.locked = False
```

---

# 23. Tile data model

A simple early implementation might use dictionaries.

```python
tile = {
    "kind": "room",
    "openings": {
        "N": True,
        "E": False,
        "S": True,
        "W": False
    }
}
```

Later, this can become a class.

```python
class Tile:
    def __init__(self, kind, north=False, east=False,
                 south=False, west=False):

        self.kind = kind

        self.openings = {
            "N": north,
            "E": east,
            "S": south,
            "W": west
        }

        self.doors = {}
        self.items = []
        self.visited = False
```

This progression is useful pedagogically because the beginner first learns dictionaries and only later sees why classes are convenient.

---

# 24. Recommended tile catalogue

The complete first version should include:

### Straight corridors

```text
corridor_ns
corridor_ew
```

### Dead ends

```text
dead_end_n
dead_end_e
dead_end_s
dead_end_w
```

### Corners

```text
corner_ne
corner_es
corner_sw
corner_wn
```

### T-junctions

```text
t_new
t_nes
t_esw
t_nsw
```

### Cross

```text
cross_nesw
```

### Rooms

```text
room_none

room_n
room_e
room_s
room_w

room_ns
room_ew

room_ne
room_es
room_sw
room_wn

room_new
room_nes
room_esw
room_nsw

room_nesw
```

### Special rooms

```text
start_room
exit_room
boss_room
hidden_room
treasure_room
```

### Door overlays

```text
door_n
door_e
door_s
door_w
```

---

# 25. Dungeon representation

The high-level map should be a grid of tile objects.

Example:

```python
tile_map = [
    [None,        room_s,       None],
    [corridor_e,  cross_nesw,   room_w],
    [None,        boss_room,    None],
]
```

Eventually:

```python
MAP_WIDTH = 20
MAP_HEIGHT = 20

tile_map = [
    [None for _ in range(MAP_WIDTH)]
    for _ in range(MAP_HEIGHT)
]
```

Each position either contains:

```text
None
```

or a:

```text
Tile
```

---

# 26. Procedural dungeon generation

The dungeon should be generated so that connectivity is guaranteed by construction.

The previous architecture proposes building a connectivity graph and using a spanning tree rather than generating arbitrary rooms and repeatedly checking whether the resulting dungeon happens to be reachable. 

The same principle works well here.

---

# 27. Generation strategy

A possible generation pipeline is:

## Step 1: create empty tile grid

```python
tile_map = ...
```

## Step 2: select start position

Place:

```text
START
```

somewhere in the grid.

## Step 3: grow paths

Create connected paths outward.

Possible directions:

```python
["N", "E", "S", "W"]
```

## Step 4: decide junction types

Depending on how many neighbours a tile connects to, assign its shape.

For example:

```text
2 opposite neighbours → straight corridor
2 adjacent neighbours → corner
3 neighbours          → T-junction
4 neighbours          → cross
```

## Step 5: replace selected nodes with rooms

Some path nodes become full rooms.

## Step 6: place boss room

Reserve a free 3 × 3 region.

## Step 7: place exit

The exit should preferably be reasonably far from the start.

## Step 8: add loops

Add some extra connections so the dungeon does not feel like a single branching tree.

## Step 9: place doors and keys

Locked routes may require exploration elsewhere.

## Step 10: populate enemies and items

---

# 28. Automatic tile classification

The generator does not actually need to manually choose names like:

```text
corner_ne
```

It can determine the tile from connected neighbours.

For example:

```python
connections = {
    "N": True,
    "E": True,
    "S": False,
    "W": False
}
```

The renderer knows this corresponds to a north-east corner.

This makes generation considerably cleaner.

---

# 29. Connection validation

Whenever two adjacent tiles exist, assert that their openings match.

For example:

```python
assert tile.openings["E"] == neighbour.openings["W"]
```

Similarly:

```python
assert tile.openings["N"] == neighbour.openings["S"]
```

This is an excellent beginner-friendly introduction to assertions and invariants.

---

# 30. Player

The player exists independently from the dungeon tiles.

```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 20
        self.inventory = []
        self.keys = []
```

Later we may distinguish:

```text
tile_x
tile_y
local_x
local_y
```

because the player can move inside the larger ASCII tile.

---

# 31. Movement

Basic controls:

```text
W = up
A = left
S = down
D = right
```

Movement should proceed one logical floor position at a time.

Pseudo-code:

```python
new_x = player.x
new_y = player.y

if command == "w":
    new_y -= 1

elif command == "s":
    new_y += 1

elif command == "a":
    new_x -= 1

elif command == "d":
    new_x += 1
```

Then:

```python
if can_move_to(new_x, new_y):
    player.x = new_x
    player.y = new_y
```

---

# 32. Collision

The player may move onto:

```text
floor
open doorway
open door
item
exit
```

The player may not move onto:

```text
wall
locked door
closed door
solid obstacle
```

This logic should live inside something like:

```python
can_move_to()
```

rather than being scattered around the game.

---

# 33. Monsters

Monsters should use the same fundamental position system as the player.

```python
class Monster:
    def __init__(self, x, y, hp, damage, name):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.name = name
```

The existing architecture also keeps monsters in a separate list rather than writing them directly into the dungeon data. 

Example:

```python
monsters = [
    Monster(12, 8, 5, 2, "Goblin"),
    Monster(20, 4, 8, 3, "Skeleton")
]
```

---

# 34. Combat

Turn-based combat is probably the best choice for this teaching project.

It fits naturally with the input loop:

```text
player acts
enemy acts
player acts
enemy acts
```

Simple first version:

```python
monster.hp -= player.damage

if monster.hp > 0:
    player.hp -= monster.damage
```

Later we can add:

```text
weapons
armour
critical hits
status effects
boss mechanics
```

---

# 35. Items

Base item class:

```python
class Item:
    def __init__(self, x, y, name, kind):
        self.x = x
        self.y = y
        self.name = name
        self.kind = kind
```

Possible item types:

```text
key
potion
weapon
armour
treasure
map
food
```

This matches the existing project architecture's item model. 

---

# 36. Inventory

The player inventory can begin as a list:

```python
player.inventory = []
```

Pickup:

```python
player.inventory.append(item)
```

Display:

```python
for item in player.inventory:
    print(item.name)
```

This makes inventory a useful teaching exercise for lists and loops.

---

# 37. Hidden rooms

Hidden rooms should exist in the dungeon but have an entrance disguised as a wall.

The original architecture proposes tracking a secret wall separately and converting it to floor when discovered. 

The same idea can be used here.

For example:

```python
secret_walls = {
    (x, y): {
        "found": False
    }
}
```

When discovered:

```python
secret_walls[(x, y)]["found"] = True
```

and the wall becomes traversable.

---

# 38. Start room

Every dungeon contains one start room.

It should:

* be safe
* contain the player initially
* have at least one valid exit
* generally be far from the final exit or boss

Possible symbol:

```text
S
```

---

# 39. Exit room

The dungeon contains an exit tile or exit room.

Possible symbol:

```text
E
```

When the player reaches it:

```python
if player_position == exit_position:
    win_game()
```

The existing architecture treats `E` as the win-condition tile. 

---

# 40. Boss behaviour

Boss rooms should contain:

```text
one boss
or
one boss + supporting enemies
```

Entering may optionally close the door behind the player.

Example:

```text
You enter the chamber.

The door slams shut.

A giant troll wakes.
```

Defeating the boss might:

```text
unlock exit
drop special key
open boss-room doors
award treasure
```

---

# 41. Rendering

The rendering system should read the game state but should not modify it.

Conceptually:

```python
render(tile_map, player, monsters, items)
```

The original architecture recommends layered rendering, with things such as the player, monsters and items drawn over the underlying terrain. 

Suggested priority:

```text
player
monster
item
door
floor / wall
```

---

# 42. Rendering large tiles

Each tile should be generated as a list of 21 strings.

Example:

```python
tile_lines = [
    "#####################          #####################",
    ...
]
```

Every line must satisfy:

```python
len(line) == 52
```

And every tile must satisfy:

```python
len(tile_lines) == 21
```

These are useful assertions:

```python
assert len(tile_lines) == 21

for line in tile_lines:
    assert len(line) == 52
```

That will prevent the alignment problems we encountered while designing the tiles manually.

---

# 43. Procedural tile renderer

Rather than manually storing dozens of huge ASCII templates, we should eventually generate them.

Example interface:

```python
render_tile(
    kind="room",
    north=True,
    east=False,
    south=True,
    west=False
)
```

The renderer creates:

```text
top wall
top opening
side walls
side openings
bottom opening
bottom wall
```

according to fixed geometry constants.

---

# 44. Geometry constants

Use explicit constants:

```python
TILE_WIDTH = 52
TILE_HEIGHT = 21

SIDE_WALL_WIDTH = 6
TOP_WALL_HEIGHT = 3

VERTICAL_DOOR_WIDTH = 10
HORIZONTAL_DOOR_HEIGHT = 3
```

For the room:

```python
ROOM_INTERIOR_WIDTH = 40
ROOM_INTERIOR_HEIGHT = 15
```

This is much safer than manually counting spaces every time.

---

# 45. Useful derived constants

Centre:

```python
CENTER_X = TILE_WIDTH // 2
CENTER_Y = TILE_HEIGHT // 2
```

North/south opening:

```python
DOOR_LEFT = (TILE_WIDTH - VERTICAL_DOOR_WIDTH) // 2
DOOR_RIGHT = DOOR_LEFT + VERTICAL_DOOR_WIDTH
```

East/west opening:

```python
DOOR_TOP = (TILE_HEIGHT - HORIZONTAL_DOOR_HEIGHT) // 2
DOOR_BOTTOM = DOOR_TOP + HORIZONTAL_DOOR_HEIGHT
```

This guarantees symmetry.

---

# 46. Minimap

The main screen should eventually show only the area around the player.

A separate minimap can display explored rooms at a much smaller scale.

The previous architecture proposes maintaining a discovered set and drawing a downsampled representation of visited rooms. 

Example:

```text
    □
    |
□---□---□
    |
    □---B
```

Possible symbols:

```text
□ = discovered room
B = boss room
S = start
E = exit
? = unknown
```

---

# 47. Game state

A simple global game state might include:

```python
game = {
    "tiles": tile_map,
    "player": player,
    "monsters": monsters,
    "items": items,
    "doors": doors,
    "discovered": set(),
    "game_over": False
}
```

Later this can become:

```python
class Game:
    ...
```

---

# 48. Main game loop

The fundamental structure should remain simple.

```python
while player.hp > 0:

    render_game()

    command = input("> ")

    handle_command(command)

    update_monsters()

    check_items()

    check_exit()
```

The original architecture follows the same input-driven game-loop model. 

---

# 49. Commands

Initial controls:

```text
w = move north
a = move west
s = move south
d = move east
```

Later:

```text
i = inventory
m = map
f = search
q = quit
h = help
```

Possible combat actions:

```text
attack
use
run
```

---

# 50. Suggested project structure

Early in the project, keep everything in:

```text
game.py
```

Once it becomes difficult to navigate, split it.

For example:

```text
maze_game/
│
├── main.py
├── tiles.py
├── dungeon.py
├── entities.py
├── items.py
├── combat.py
├── render.py
└── save.py
```

Do not introduce this structure too early.

The refactor itself can become a lesson about modules.

---

# 51. Development stages

The original project already proposes building the game in incremental, runnable stages rather than constructing everything simultaneously. 

I would update that build order for the new tile system as follows.

## Stage 1: printing

Learn:

```text
print()
strings
variables
```

Build:

```text
one static room
```

---

## Stage 2: player marker

Learn:

```text
variables
coordinates
```

Build:

```text
@ symbol inside room
```

---

## Stage 3: input

Learn:

```text
input()
if
elif
```

Build:

```text
WASD movement
```

---

## Stage 4: collision

Learn:

```text
functions
conditions
```

Build:

```text
walls block player
```

---

## Stage 5: one tile object

Learn:

```text
dictionaries
```

Build:

```text
room openings stored as N/E/S/W
```

---

## Stage 6: procedural tile rendering

Learn:

```text
loops
string construction
```

Build:

```text
generate room ASCII from openings
```

---

## Stage 7: corridor tile types

Build:

```text
straight
corner
T
cross
dead end
```

---

## Stage 8: tile grid

Learn:

```text
lists of lists
```

Build:

```text
multiple connected tiles
```

---

## Stage 9: random generation

Learn:

```text
random
```

Build:

```text
random connected dungeon
```

---

## Stage 10: rooms

Build:

```text
rooms mixed into corridor network
```

---

## Stage 11: items

Learn:

```text
lists
objects
```

Build:

```text
keys
potions
weapons
```

---

## Stage 12: doors

Learn:

```text
state
dictionaries
```

Build:

```text
locked doors
keys
```

---

## Stage 13: classes

Introduce:

```python
Player
Tile
Room
Item
Door
Monster
```

Only after the simpler data structures are already understood.

---

## Stage 14: enemies

Build:

```text
monster movement
turn system
combat
```

---

## Stage 15: boss room

Build:

```text
3 × 3 boss arena
boss encounter
```

---

## Stage 16: minimap

Build:

```text
exploration tracking
map command
```

---

## Stage 17: save/load

Learn:

```text
JSON
files
```

Build:

```text
save game
load game
```

---

# 52. Important programming principles to teach

Throughout the project, reinforce:

## One job per function

Bad:

```python
def move_and_draw_and_attack_and_save():
```

Better:

```python
move_player()
render_game()
attack()
save_game()
```

---

## Data and visuals are different

The tile should not fundamentally be:

```text
#####################
```

The tile should be:

```python
Tile(
    kind="room",
    openings=...
)
```

and the renderer decides what ASCII that produces.

---

## Prefer calculated geometry

Avoid manually typing:

```text
"#####################          #####################"
```

throughout the code.

Instead calculate it from constants.

---

## Make invalid states difficult

If tile A connects east, tile B should automatically connect west.

Do not rely on remembering to fix both manually.

---

## Build working versions

Each lesson should end with something that runs.

That principle was part of the original architecture and is particularly important for teaching. 

---

# 53. First milestone

The first meaningful version of the game should have:

* one static dungeon
* several connected tiles
* corridors
* corners
* junctions
* rooms
* a player
* WASD movement
* collision
* an exit

No procedural generation yet.

Something like:

```text
START
  |
ROOM
  |
CORRIDOR
  |
T JUNCTION
 /        \
ROOM      ROOM
            |
           EXIT
```

This gives your brother something genuinely playable very early.

---

# 54. Second milestone

Add:

* procedural maze generation
* dead ends
* loops
* random rooms
* keys
* doors
* basic items

Now the dungeon becomes replayable.

---

# 55. Third milestone

Add:

* monsters
* HP
* combat
* weapons
* potions
* treasure
* minimap
* hidden rooms

---

# 56. Fourth milestone

Add:

* 3 × 3 boss rooms
* boss enemies
* dungeon completion
* save/load
* difficulty scaling

---

# 57. Possible later extensions

Once the basic game exists, there are many directions it could grow.

### Gameplay

```text
traps
shops
NPCs
quests
different dungeon levels
magic
armour
status effects
procedural loot
```

### Generation

```text
biomes
special room templates
rare structures
multiple bosses
loops
secret areas
```

### Programming lessons

```text
inheritance
composition
pathfinding
A*
serialisation
testing
packages
type hints
```

### Graphics

The exact same game model could later be rendered using:

```text
pygame
tilesets
sprites
animations
```

without replacing the dungeon logic.

That is one of the benefits of keeping rendering separate from game state.

---

# 58. Final architecture

At maturity, the system should roughly look like:

```text
                    ┌──────────────┐
                    │ Dungeon Gen  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Tile Map   │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        ┌────────┐    ┌────────┐    ┌────────┐
        │ Player │    │ Items  │    │Monsters│
        └────────┘    └────────┘    └────────┘
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Game Logic  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Renderer   │
                    └──────┬───────┘
                           │
                           ▼
                      ASCII Screen
```

The important thing is that:

```text
Dungeon generation creates the world.

Game logic changes the state.

Rendering displays the state.

Input tells the game logic what the player wants to do.
```

Those responsibilities should remain separate.

---

# 59. Core constants

For now, I would consider these **locked design decisions**:

```python
TILE_WIDTH = 52
TILE_HEIGHT = 21

TOP_WALL_HEIGHT = 3
BOTTOM_WALL_HEIGHT = 3

LEFT_WALL_WIDTH = 6
RIGHT_WALL_WIDTH = 6

NORTH_SOUTH_OPENING_WIDTH = 10
EAST_WEST_OPENING_HEIGHT = 3
```

Standard room:

```text
#####################          #####################
#####################          #####################
#####################          #####################
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
                                                    
                                                    
                                                    
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
######                                        ######
#####################          #####################
#####################          #####################
#####################          #####################
```

This becomes the geometric reference from which every other tile is generated.

---

# 60. Project objective

The final project should be a small but genuinely complete roguelike-style maze game that your brother has built himself.

The player should be able to:

```text
enter a randomly generated dungeon
explore connected corridors
discover rooms
collect items
find keys
unlock doors
fight monsters
discover secrets
enter a huge boss chamber
defeat the boss
find the exit
win
```

But the more important outcome is that by the end he understands how those systems were built.

The project progresses naturally from:

```python
print("######")
```

to:

```python
game.run()
```

without hiding the steps in between.

