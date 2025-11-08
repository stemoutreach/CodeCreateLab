# STUDENT_START — 00 Treasure Hunt (Basic)

**Use this only if you're stuck for 5–7 minutes.**  
This file gives you a clean **starter skeleton** (no spoilers) that matches the lab steps.

> Tip: Keep this side-by-side with your own `treasure.py` and copy only what you need.

---

## Starter Goals
- Show a minimal loop that runs until you win
- Normalize input (`.strip().lower()`)
- Leave **TODOs** for your logic and win condition
- Keep messages **yours** — don't copy text verbatim

---

## Minimal Skeleton (copy to your `treasure.py` if needed)
```python
# 00 — Treasure Hunt (Basic)

print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

found = False
tries = 0
valid = ["north", "south", "east", "west"]
WIN = "???"  # TODO: pick 'north' or 'south' or 'east' or 'west'

while not found:
    # Print menu once per loop
    for d in valid:
        print(f"- {d}")

    # Read + normalize
    direction = input("Which way? ").strip().lower()
    # TODO: tries += 1

    # TODO: Decide what happens
    # if direction matches WIN (full word or a shortcut like 'e'):
    #     print a win message with an f-string and set found = True
    # elif direction is one of the other valid directions (or their shortcuts):
    #     print your own message and keep looping
    # else:
    #     print a helpful nudge to use north/south/east/west

# TODO: Print how many tries it took using an f-string
```

---

## Shortcut Hints (optional)
You can accept n/s/e/w like this pattern:
```python
# Example pattern to adapt; do not copy blindly:
# if direction == "east" or direction == "e":
#     ...
```

---

## Quick Self-Check
- Loop ends only when you set found = True  
- Case/space variations work (e.g., "  EAST  ")  
- You printed a short menu using a for loop  
- Your final line reports tries using an f-string
