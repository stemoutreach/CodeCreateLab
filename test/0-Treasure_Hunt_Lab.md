# Lab 0 – Treasure Hunt (Python Basics)

## Overview
Build a text adventure where the player hunts for buried treasure on a 5×5 grid island.  
You’ll practice **print**, **input**, **if/else**, **while**, and **functions**.

## Learning objectives
- Use `print()` to present a story
- Collect and validate user input
- Branch logic with `if/elif/else`
- Loop until a win/lose condition is met
- Break code into reusable functions

## Prerequisites
Complete the steps in **Guides/Python_Basics_Guide.md**.

## Materials
- Any computer with Python 3
- This starter file: `treasure_hunt.py`

## Step‑by‑step
1. **Fork & clone** the repo, open `treasure_hunt.py`.
2. Read through the scaffolding comments.
3. Implement the TODOs one by one; run after each change.
4. When you can *“dig”* and either find treasure or run out of guesses, you’re done!

## Starter code

```python
# treasure_hunt.py
import random

GRID_SIZE = 5
MAX_TURNS = 8

def place_treasure():
    """Randomly choose x, y within the grid."""
    return random.randint(1, GRID_SIZE), random.randint(1, GRID_SIZE)

def get_player_guess():
    """Prompt the player and return (x, y) as ints."""
    # TODO: ask for input like "3 4" and split
    return 0, 0  # placeholder

def give_hint(treasure, guess):
    """Print colder/warmer hint."""
    # TODO: compare Manhattan distance and print a message

def main():
    print("🧭  Welcome to Treasure Hunt!")
    treasure = place_treasure()
    turns_left = MAX_TURNS

    while turns_left:                    # TODO: loop condition
        # TODO: call get_player_guess()
        # TODO: check for win; break if found
        # TODO: else give_hint() and decrement turns_left

    print("Game over! The treasure was at", treasure)

if __name__ == "__main__":
    main()
```

## Stretch goals
- Track **score** across multiple rounds.
- Add **easy / hard** modes (change grid size & turns).
- Animate a simple map with 🟦 and 🟨 using `print()`.
