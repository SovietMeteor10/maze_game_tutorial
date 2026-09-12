# 12: Turns, Enemies, Combat, And State Transitions

**Coding exercise:** `12_turns_enemies_combat.py` | **Model answer:** `../solutions/12_turns_enemies_combat.py`

Combat is a good place to combine objects, methods, state, mutation, and conditions. A fighter begins with health. An attack subtracts damage from a target. The target may survive and receive a turn, or it may reach zero health and be skipped. The checkpoint models one fair exchange without hiding the rules inside a large game loop.

## What You Will Build

You will study `tutorial/checkpoints/12_turn_combat.py`. It defines a `Fighter` class with `name`, `hp`, and `damage` attributes. It defines a separate `attack(attacker, target)` function that mutates the target's health and returns a message. `main` creates a player and a snake, lets the player attack first, lets the snake attack only if it survived, and reports whether the snake is defeated.

The point is not to build a complete battle system. The point is to make one turn sequence traceable from input objects to changed state to displayed result.

## Learning Goals

- Explain turn order as a game rule.
- Use a class to represent repeated combatants.
- Distinguish attributes from methods and a standalone function.
- Mutate the correct target object.
- Clamp health at zero with `max`.
- Use a condition to prevent a defeated enemy from acting.
- Keep combat calculation separate from display text.
- Compare this simple exchange with the reference game's real-time snake rules.

## New Words With Plain Definitions

- **Turn**: One participant's chance to act.
- **Enemy**: A character or creature opposing the player.
- **Combat**: A conflict controlled by game rules.
- **Fighter**: A checkpoint object that can deal and receive damage.
- **Health or hp**: A number showing how much damage a fighter can survive.
- **Damage**: An amount subtracted from a target's health.
- **State transition**: A change from one game situation to another, such as 5 hp becoming 2 hp.
- **Mutation**: Changing an existing object's attribute in place.
- **Target**: The object receiving an action.
- **Turn order**: The rule deciding who acts first and who acts next.
- **Rendering**: Showing game results as text or graphics.
- **Pure-ish rule**: A calculation that focuses on its inputs and result rather than keyboard or screen work.
- **Clamp**: Keep a number within a boundary. Here, health cannot go below zero.

## Why This Matters

The order of actions changes fairness. If the snake attacks after it has been defeated, the player can lose health to a dead enemy. The checkpoint uses `if snake.hp:` as a compact rule: positive health is truthy, and zero health is falsey. That condition is not decoration; it is the gate between one turn and the next.

Combat also demonstrates separation of concerns. `attack` changes health and creates a result sentence. It does not read a key, draw the map, or decide how many turns the whole game should run. A larger controller can decide when to call it. A user interface can display the returned sentence. A test can inspect health directly.

Mutation is appropriate because the fighter object is the current game state. When the snake takes damage, every part of the program that has a reference to that snake should see the new hp. The danger is mutating the wrong object. The attacker's damage is read; the target's hp is changed.

## Tiny Examples Explained Line By Line

```python
def subtract_health(hp, damage):
    return max(0, hp - damage)

print(subtract_health(2, 5))
```

The function receives a current health number and a damage number. It subtracts damage, but `max(0, ...)` selects zero if the result would be negative. The call prints `0`. This rule does not know about a player, a screen, or a turn.

```python
hp = 1
if hp:
    print("alive")
```

Python treats zero as false in a condition and a positive integer as true. Therefore this prints `alive`. If `hp` became zero, the body would be skipped. Writing `if hp > 0` is more explicit and would express the same idea here.

```python
class Fighter:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
```

The class is a reusable recipe. The constructor stores different starting values on each instance. Two fighters can use the same class while having separate health.

## Guided Build Tied To The Checkpoint

Open `tutorial/checkpoints/12_turn_combat.py`. `Fighter.__init__` assigns three attributes in one line: `name`, `hp`, and `damage`. The player and snake are instances of the same class, but their values differ. That is why one class can represent both sides without claiming that they are the same character.

The `attack` function receives two objects. `attacker.damage` reads the attacker's power. `target.hp - attacker.damage` calculates the new health. `max(0, ...)` clamps it. The assignment to `target.hp` mutates the target instance. The formatted return string reads both names and the resulting health. It does not print, so the caller controls presentation.

In `main`, the player has 10 hp and 3 damage. The snake has 5 hp and 1 damage. The first call changes snake hp from 5 to 2 and returns `Player hits Snake (2 hp left)`. The condition `if snake.hp:` is true because 2 is positive, so the snake gets its turn. It changes player hp from 10 to 9. The final expression `snake.hp == 0` is false, so the program reports that the snake is not defeated.

## Complete Checkpoint Walkthrough

Run the checkpoint. The expected output is:

```text
Player hits Snake (2 hp left)
Snake hits Player (9 hp left)
Defeated: False
```

Read it as a timeline. At time zero, player is 10 hp and snake is 5 hp. Player damage is 3, so snake becomes 2. Because 2 is truthy, snake acts and its damage of 1 changes player to 9. The snake is not at zero, so the final comparison is false.

If the player's damage changes to 5, the first attack sets snake hp to zero. The condition becomes false, so no snake attack is printed. This is the intended turn rule. The checkpoint does not loop until someone dies; it demonstrates one exchange. A later game can call the same pieces repeatedly.

## Common Mistakes

- Subtracting from `attacker.hp` hurts the wrong object.
- Letting a zero-hp snake attack violates the checkpoint's turn order.
- Omitting `max` can create negative health such as `-3`.
- Printing inside `attack` makes the rule less reusable.
- Changing damage without recalculating the expected output causes misleading debugging.
- Using one global hp value makes multiple fighters overwrite each other.
- Confusing a method on `Fighter` with the checkpoint's standalone `attack` function changes the design; either can work, but follow the actual file first.

## Fun Side Quests

1. Change player damage to 5 and predict which output line disappears.
2. Add a second attack call only when both fighters still have hp, then calculate the new totals.
3. Add `assert snake.hp == 2` immediately after the first attack in a copy of the checkpoint.
4. Give the snake 6 damage and see how quickly the player's health changes.
5. Add a healing function that uses `min` to prevent health exceeding a maximum.

## Run Command And Expected Result

```text
python3 tutorial/checkpoints/12_turn_combat.py
```

Expected result:

```text
Player hits Snake (2 hp left)
Snake hits Player (9 hp left)
Defeated: False
```

## Learner Questions

- Why does a dead enemy lose its turn?
- Why is `target.hp` mutated instead of `attacker.hp`?
- What would a healing action change?
- Should a game use a method such as `player.attack(snake)` or a rule function such as `attack(player, snake)`? What might each design make easier?

## What To Remember

Combat is state changing under a turn-order rule. Classes hold each fighter's independent attributes. The attack rule reads the attacker, mutates the target, clamps health, and returns a result. A condition decides whether the next participant is still allowed to act.

## Exact Reference Game Comparison

The reference game stores the player in `game/player.py` and snakes in `game/monsters.py`. A reference `Snake` has position, tail, hp, speed, and boss flags rather than the checkpoint's name, hp, and damage. In `game/game.py`, `attack` finds a nearby snake, subtracts 5 damage for a normal attack or 10 for a boss, removes defeated snakes, and can drop a relic. The same file's `update_snakes` and `update_realtime` coordinate enemy movement, while collision applies damage to the player. The checkpoint is a deliberately simplified, turn-by-turn model of the same core ideas: fighter state, damage mutation, survival checks, and a controller that decides when rules run.
