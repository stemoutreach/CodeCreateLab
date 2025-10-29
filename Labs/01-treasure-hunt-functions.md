
---
title: "Treasure Hunt (Functions)"
level: "01"
estimated_time: "35-60 min"
difficulty: "Beginner → Intermediate"
prereqs:
  - "Lab: 00 – Treasure Hunt (Basic) (../Labs/00-treasure-hunt-basic.md)"
  - "Guide: 01 – Python Functions (../Guides/01-python-functions.md)"
rubric:
  - "✅ Must: Uses at least three functions (welcome, input, evaluate/check)"
  - "✅ Must: Returns values from a function (e.g., check_direction returns win/lose/continue)"
  - "✅ Must: Main loop calls functions and ends cleanly on win or quit"
  - "⭐ Stretch: Adds a helper function (e.g., normalize) and a tiny state/map"
---

# Goal
Refactor your basic Treasure Hunt into a **function-based design** that’s easier to read and extend.

## Materials
- Computer only (Python 3 or browser-based Python environment)

## Steps
1) **Plan** — List the functions you’ll write (see starter). Decide your map/win condition.
2) **Build** — Write and test each function **individually** before wiring them together.
3) **Code** — Use return values rather than printing inside every function.
4) **Test** — Try different paths and invalid input; verify quit flow works.
5) **Iterate** — Add one stretch feature (stateful map or helper utilities).

## Starter design & code
```python
def welcome():
    print("Welcome to the Treasure Hunt (Functions)!")
    print("Type a direction (north/south/east/west) or 'quit' to exit.")

def normalize(text, casefold=True):
    text = text.strip()
    return text.casefold() if casefold else text

def get_direction(prompt="Which way? "):
    return normalize(input(prompt))

def check_direction(direction):
    """Return one of: 'win', 'continue', 'invalid'"""
    if direction == "east":
        print("🎉 You found the treasure!")
        return "win"
    elif direction in {"north", "south", "west"}:
        outcomes = {
            "north": "You hit a wall.",
            "south": "You stepped in a puddle.",
            "west": "It's a dead end.",
        }
        print(outcomes[direction], "Try again.")
        return "continue"
    else:
        return "invalid"

def main():
    welcome()
    tries = 0
    while True:
        d = get_direction()
        if d == "quit":
            print("Goodbye!")
            break
        result = check_direction(d)
        tries += 1

        if result == "win":
            print(f"You won in {tries} tries!")
            break
        elif result == "invalid":
            print("Please type north/south/east/west or 'quit'.")

if __name__ == "__main__":
    main()
```

## Submission / Demo checklist
- [ ] Uses **three+ functions** with clear names and single purposes.
- [ ] `check_direction()` **returns** a value that drives the main loop (no hidden globals).
- [ ] Program handles **invalid** input and supports **quit**.
- [ ] Code is organized and readable (blank lines, docstrings/comments where helpful).

## Extensions (choose one)
- **Stateful map:** Track a 2×2 grid and the player’s position; win only at specific coordinates.
- **Lives/score:** Subtract lives for bad choices; track and print best score.
- **Hints:** Add `get_hint()` that returns a clue based on the last direction.

## Troubleshooting
- **Function returns `None`** → Ensure you `return` a value instead of only `print`ing.
- **Global state bugs** → Pass values into functions and **return** results rather than mutating globals.
- **Unclear flow** → Keep `main()` short—delegate logic to helpers.

## Reflection (1–2 sentences)
- Which function helped the most with readability?
- What would you add next if you had one more hour?

## Next up
Advance to hardware with **[02 – Sense HAT Basics](../Labs/02-sense-hat-basics.md)** when you’re ready.
