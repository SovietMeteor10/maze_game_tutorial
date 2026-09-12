# 11: Classes, Objects, And Entities

**Coding exercise:** `11_classes_entities.py` | **Model answer:** `../solutions/11_classes_entities.py`

The earlier checkpoints used dictionaries and dataclasses to group data. Now we will learn the full Python class idea. A class is a recipe. An object, also called an instance, is one thing made from that recipe. Classes are useful when a game thing has several attributes that belong together, and when many objects share the same shape or behavior.

## What You Will Build

You will study `tutorial/checkpoints/11_entities.py`. It defines `Tile`, `Item`, `Door`, `Player`, and `Monster` classes. `main` creates instances of those classes, puts an `Item` instance inside a player's inventory, and puts several different instances into one `things` list. It then prints each instance's class name and follows the composition relationship from player to item.

This checkpoint does not add movement or combat. Its job is to make object-oriented vocabulary concrete before the game has more rules.

## Learning Goals

- Distinguish a class, an object, and an instance.
- Read a constructor named `__init__`.
- Explain `self`, attributes, and methods.
- Understand why each player needs separate state.
- Understand composition as putting objects inside other objects.
- Understand inheritance and why this checkpoint does not need it.
- Relate these simple classes to the reference game's dataclasses.

## New Words With Plain Definitions

- **Class**: A recipe describing what objects of a kind contain and can do.
- **Object**: A value made from a class. In Python, every instance is an object.
- **Instance**: One individual object created from a class.
- **Attribute**: Data attached to an instance, such as `player.hp`.
- **Method**: A function defined inside a class, usually operating on that instance.
- **Constructor**: Setup work that runs while an instance is being created.
- `__init__`: Python's common constructor method. It assigns starting attributes.
- **self**: The particular instance currently using a method or holding constructor data.
- **Composition**: Building a larger thing by storing smaller objects inside it.
- **Inheritance**: Defining a new class from an existing class to reuse or specialize behavior.
- **Entity**: A game thing with an identity or role, such as a player or monster.
- **Instance state**: Attribute values belonging to one particular instance.

## Why This Matters

Without classes, a player might be split across `player_name`, `player_hp`, and `player_inventory`, while a monster uses another collection of unrelated variables. That becomes difficult to pass around and easy to mix up. A `Player` object keeps its name, health, and inventory together.

Classes also make repeated things manageable. A game can create one player and many monsters from the same recipe. Each instance starts with the correct fields, but its state is independent. Changing one monster's health should not change every other monster.

Classes are not automatically better than dictionaries. A one-time configuration may be clearer as a dictionary. A small, repeated game object with identity and behavior is a good class candidate. Use the simplest structure that keeps the program understandable.

## Tiny Examples Explained Line By Line

```python
class Lantern:
    def __init__(self, color):
        self.color = color

lamp = Lantern("blue")
print(lamp.color)
```

The first line begins a class recipe. The constructor receives a `color` argument when a new instance is made. `self` refers to the new lantern, so `self.color = color` stores the argument as an attribute on that particular object. `Lantern("blue")` constructs one instance. `lamp.color` reads its stored attribute.

```python
class Counter:
    def __init__(self):
        self.number = 0

    def add(self):
        self.number += 1
```

The constructor gives each counter its own starting number. `add` is a method because it is indented inside the class. When `counter.add()` runs, Python supplies `counter` as `self`, so the method changes that counter's `number` attribute.

Inheritance would look like this:

```python
class Animal:
    pass

class Snake(Animal):
    pass
```

`Snake` inherits from `Animal`, so shared behavior could live in `Animal`. The checkpoint does not use inheritance because its tile, door, player, and monster do not yet share a useful behavior contract. Composition, such as a player containing item objects, is enough.

## Guided Build Tied To The Checkpoint

Open `tutorial/checkpoints/11_entities.py`. `Tile.__init__` stores `kind` on `self`. `Item.__init__` stores `name`. `Door.__init__` stores the required key and starts `open` as `False`. The two assignments on one line are still ordinary assignments; they simply use tuple unpacking.

`Player.__init__` stores three separate attributes: the supplied name, a starting `hp` of 10, and a new empty inventory list. `Monster.__init__` stores a name and starts at 4 hp. The constructor is the place where the object becomes valid enough for the rest of the program to use.

In `main`, `player = Player("Explorer")` creates an instance. `Player` is the class recipe; `player` is one object made from it. The next line creates an `Item` instance and appends it to `player.inventory`. This is composition: a Player object contains an Item object. The item is not copied into separate name text; the actual object is stored.

The `things` list demonstrates that one list can hold instances of different classes. `type(thing).__name__` asks Python for the class name that made each object. The final print follows `player.inventory[0].name`: first reach the player, then its inventory, then the first item, then the item's name.

## Complete Checkpoint Walkthrough

Run the checkpoint. Python defines five classes, enters `main`, constructs a player, constructs an item, and composes them. It then creates a tile, door, and monster. The expected output is:

```text
Entities: Tile, Door, Player, Monster
Explorer has Gold Key
```

There is no `Fighter` here, no method call beyond list `append`, and no inheritance. That is intentional. Learn how state is packaged before adding behavior that changes it.

## Common Mistakes

- Writing `name = name` does not store the value on the object; use `self.name = name`.
- Omitting `self` from `__init__` or a method changes how Python calls it.
- `Player` is the class; `Player("Explorer")` is an instance.
- Giving every object a shared global inventory would mix players together.
- Appending a string instead of an `Item` object means `.name` may not exist.
- Adding inheritance only because two classes both have a `name` attribute can make the design harder to understand.
- A method must be indented inside its class.

## Fun Side Quests

1. Create two players and append a key to only one. Prove their inventories are separate.
2. Add a `symbol` attribute to `Monster` and print it.
3. Add a `describe` method to `Door` that returns its key and open status.
4. Add a method to `Player` that reports whether `hp` is above zero, then call it.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/11_entities.py
```

Expected result:

```text
Entities: Tile, Door, Player, Monster
Explorer has Gold Key
```

## Learner Questions

- Why does `self.hp` belong to each fighter or monster rather than one global variable?
- Is an item inside an inventory an example of composition? Why?
- When would inheritance reduce repeated code?
- Why can a plain dictionary still be the better choice for one simple value?

## What To Remember

A class is a recipe, and an instance is one object made from it. Constructors create starting state. Attributes store data, methods store behavior, and `self` identifies the current instance. Composition means objects can contain other objects. Inheritance is optional, not a requirement for object-oriented code.

## Exact Reference Game Comparison

The reference game uses dataclasses in `game/player.py`, `game/items.py`, `game/doors.py`, and `game/monsters.py`. `Player` owns an inventory and health, `Item` owns item facts, `Door` owns lock state and opening behavior, and `Snake` owns monster position and health. Those are richer versions of the checkpoint classes. The reference also uses composition in `game/game_state.py`, where a `GameState` contains a player, world, items, doors, and monsters. It generally prefers focused classes and composition rather than forcing every game thing into one inheritance tree.
