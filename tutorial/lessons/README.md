# Lesson Guide

This is a learn-by-building course for someone who is new to programming. You do
not need to know Python before Lesson 1. You do need curiosity, patience, and a
place where you can run Python commands.

## How To Use A Lesson

Read one lesson from top to bottom before changing code. The headings are
deliberate:

1. **What You Will Build** tells you the small result for this lesson.
2. **Learning Goals** tells you what to pay attention to.
3. **New Words** gives ordinary-language definitions before the words appear in
   complicated explanations.
4. **Tiny Examples** isolates one idea so the game code is not the first place
   you meet it.
5. **Guided Build** connects the idea to the checkpoint.
6. **Common Beginner Mistakes** gives you a debugging starting point.
7. **Fun Side Quests** lets you experiment without risking the main project.
8. **Learner Questions** gives you a way to test whether you understand the idea.
9. **Reference Game Comparison** shows how the small idea grows into the real
   product without asking you to copy a 2,000-line file.

Do not rush to the next lesson just because the checkpoint runs. Try changing
one thing, predict what will happen, run it, and compare the result with your
prediction. That loop of prediction, experiment, and explanation is programming
practice.

## What To Do When You Get Stuck

- Read the error's last line first. It usually says what Python could not do.
- Read the line number, then inspect the line before it too. Missing quotes and
  parentheses often cause an error to be reported one line later.
- Add a temporary `print()` to inspect a value.
- Change one thing at a time.
- Return to the smallest checkpoint that still shows the idea.
- Explain the problem out loud or on paper. If you cannot describe the value,
  its type, and the line that changes it, that is the next thing to investigate.

An error is not a personal judgement. It is a message about the program's
current assumptions. Debugging means reading that message and testing those
assumptions.

## Course Map

1. [Printing A Static Room](01-printing-static-room.md) - strings, lists, and
   terminal output.
2. [Variables, Coordinates, And The Player](02-variables-coordinates-player.md) -
   values, indexing, and a player marker.
3. [Input And Conditions](03-input-conditionals-wasd.md) - user input,
   comparisons, booleans, and WASD movement.
4. [Functions, Collision, And The Loop](04-functions-collision-loop.md) -
   reusable recipes, scope, returns, and a game loop.
5. [Dictionaries And Tile Openings](05-dictionaries-tile-openings.md) - data
   with named fields and directions.
6. [Loops And A Tile Renderer](06-loops-string-tile-renderer.md) - repeated
   work, nested loops, and generated geometry.
7. [Lists Of Lists And A Static Map](07-lists-static-tile-map.md) - rows,
   columns, and the `map[y][x]` convention.
8. [A Seeded Connected Dungeon](08-randomness-connected-dungeon.md) - random
   choices, seeds, sets, and reachable growth.
9. [Items And Inventory](09-items-inventory.md) - collections, pickup rules,
   and separation of concerns.
10. [State, Doors, And Keys](10-state-doors-keys.md) - changing state safely and
    validating commands.
11. [Classes, Objects, And Entities](11-classes-entities.md) - classes,
    instances, attributes, methods, composition, and inheritance.
12. [Turns, Enemies, And Combat](12-turns-enemies-combat.md) - state changes,
    turns, rules, and testable combat.
13. [Exploration, Secrets, And A Minimap](13-exploration-secrets-minimap.md) -
    discovery state and coordinate translation.
14. [Larger Structures And A Boss Arena](14-structures-boss-arena.md) - nested
    data, composition, and progression.
15. [JSON Save And Load](15-json-save-load.md) - persistence, serialization,
    validation, and file boundaries.
16. [Refactoring And Comparison](16-refactoring-reference.md) - modularity,
    cohesion, coupling, reusability, interpretability, and testability.

## The Big Ideas

The course introduces syntax, but syntax is not the final goal. Keep asking:

- **Readability:** Can another person understand this code without guessing?
- **Interpretability:** Can you explain what each value means and why it changes?
- **Modularity:** Can one part change without forcing unrelated parts to change?
- **Reusability:** Can a useful function or class be used in more than one place?
- **Testability:** Can you check a rule without starting the whole terminal game?
- **Separation of concerns:** Does each piece have one main job?
- **Cohesion:** Do the things inside one module belong together?
- **Coupling:** How many details must two modules know about each other?

Good design is not code that looks clever. It is code that makes the next
change understandable.

## Checkpoints

Each lesson has a matching runnable file in `tutorial/checkpoints/`. Run it from
the project root with a command such as:

```text
python3 tutorial/checkpoints/01_static_room.py
```

The checkpoints are demonstrations, not replacements for writing code yourself.
After running one, copy it to a temporary file or make a small change and see
what happens. Checkpoint 3 and checkpoint 4 also support `--play` for typing
movement commands.

The complete reference game lives in `game/`. It is intentionally more complex
than the tutorial. Use it to answer questions after a lesson, not as the first
example you have to understand.

## The Coding Exercises

Each lesson also has two Python files:

- `tutorial/lessons/##_topic.py` is the learner exercise.
- `tutorial/solutions/##_topic.py` is the model answer.

The names use underscores because they are Python filenames. For example:

```text
tutorial/lessons/04_functions_collision_loop.py
tutorial/solutions/04_functions_collision_loop.py
```

Use this order:

1. Read the matching Markdown lesson.
2. Run the learner exercise before changing it.
3. Read its `WORKED EXAMPLE` comments.
4. Complete one `TODO` at a time.
5. Run the file again after each small change.
6. Try one side quest from the Markdown lesson.
7. Compare your work with the model answer only after making a real attempt.
8. Run the checkpoint to see the lesson's compact milestone.

The exercise files are intentionally not blank. A total beginner should have
something that runs immediately and enough surrounding code to see where the new
idea belongs. A `TODO` is a question for you to answer in code, not an error that
the author forgot to fix.

The model answer is one good answer, not the only possible answer. Compare ideas,
names, and boundaries rather than trying to make your file look character-for-
character identical. If your version is readable, works, and is easy to explain,
you are learning the right skill.

To run an exercise or its answer:

```text
python3 tutorial/lessons/01_printing_static_room.py
python3 tutorial/solutions/01_printing_static_room.py
```

The exercises and solutions use only the Python standard library. They do not
change the reference game and they do not require third-party packages.
