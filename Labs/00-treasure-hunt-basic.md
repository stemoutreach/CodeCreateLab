---
title: Treasure Hunt (Basic)
level: 00
estimated_time: 30–45 min
difficulty: Beginner
prereqs:
  - Guide: [00 – Python Basics](../Guides/00-python-basics.md)
rubric:
  - ✅ Must: Uses print(), input(), if/elif/else, and a while loop to keep playing
  - ✅ Must: Normalizes input (e.g., lowercasing) and handles invalid entries
  - ✅ Must: Game ends when treasure is found (clear success message)
  - ⭐ Stretch: Adds a simple map or limited lives/tries
---

# Goal
Build a **text adventure mini‑game** where the player chooses directions until they find a treasure.

## Materials
- Computer only (Python 3 or browser‑based Python environment)

## Steps
1) **Plan** — Decide which directions exist (north/south/east/west) and which one hides the treasure.
2) **Build** — Start with a game loop that keeps asking for a direction.
3) **Code** — Use conditionals to give different outcomes for each direction.
4) **Test** — Try correct and incorrect inputs; try uppercase/lowercase; try unexpected words.
5) **Iterate** — Add one extension (lives/tries or a tiny map).

## Starter snippet
```python
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing a direction: north, south, east, or west.")

found = False
tries = 0

while not found:
    direction = input("Which way? ").strip().lower()
    tries += 1

    if direction == "east":
        print("🎉 You found the treasure!")
        found = True
    elif direction == "north":
        print("You hit a wall. Try again.")
    elif direction == "south":
        print("You fell into a puddle. Soggy socks… try again.")
    elif direction == "west":
        print("It's a dead end. Try another way.")
    else:
        print("I don't understand that direction. Try north/south/east/west.")

print(f"You won in {tries} tries!")
```

## Submission / Demo checklist
- [ ] The game **loops** until the treasure is found.
- [ ] Input is **case‑insensitive** (e.g., `East`, `EAST`, `east` all work).
- [ ] There is a **clear win message**.
- [ ] The program handles **invalid inputs** without crashing.

## Extensions (choose one)
- **Lives/tries:** Limit the player to 5 tries; show remaining tries each turn.
- **Mini‑map:** Track “rooms” (e.g., start → east = treasure) and print a simple text map or hints.
- **Flavor:** Add sound effects via text, ASCII art, or a short intro story.

## Troubleshooting
- **Loop never ends** → Make sure you set `found = True` at the win condition.
- **Case problems** → Use `.strip().lower()` on user input before comparing.
- **Nothing happens** → Confirm your `if/elif/else` blocks are correctly **indented**.

## Reflection (1–2 sentences)
- What part of the logic was trickiest—loops, conditionals, or input handling?
- If you had more time, what feature would you add next?

## Next up
Do **[01 – Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)** to refactor your game using functions.
