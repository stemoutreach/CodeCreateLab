# STUDENT_START — 00 Treasure Hunt (Basic)

**Use this only if you're stuck for 5–7 minutes.**  
This is a clean **starter skeleton** that matches the lab. It avoids spoilers but keeps you moving.

> Keep this open next to your `treasure.py`. Copy only what you need.

---

## What this starter covers
- Print intro, set up **state** (bool/int/list/str)
- Loop with **while** until you win
- Show options with a tiny **for** loop
- Read/clean input using `.strip().lower()`
- Leave win/lose logic as **TODOs** for you

---

## Minimal Skeleton (copy into `treasure.py` if needed)

```python
# 00 — Treasure Hunt (Basic)

# Intro
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

# State (types: bool, int, list, str)
found = False
tries = 0
valid = ["north", "south", "east", "west"]
WIN = "???"  # TODO: pick one: "north", "south", "east", or "west"

while not found:
    # TODO 1: print a short menu using a for loop over 'valid' (f-string recommended)
    # for d in valid:
    #     print(f"- {d}")

    # TODO 2: read and normalize input into 'direction' using .strip().lower()
    # direction = input("Which way? ").strip().lower()

    # TODO 3: increase the guess counter
    # tries += 1

    # TODO 4: build simple helper booleans for shortcuts (pick the ones you need)
    # is_east  = (direction == "east")  or (direction == "e")
    # is_west  = (direction == "west")  or (direction == "w")
    # is_north = (direction == "north") or (direction == "n")
    # is_south = (direction == "south") or (direction == "s")

    # TODO 5: decide what happens
    # if (WIN == "east"  and is_east) or     #    (WIN == "west"  and is_west) or     #    (WIN == "north" and is_north) or     #    (WIN == "south" and is_south):
    #     print(f"You found the treasure in {tries} moves!")
    #     found = True
    # elif direction in valid or direction in ["n", "s", "e", "w"]:
    #     print("Not here—keep exploring...")
    # else:
    #     print("Try north, south, east, or west (n/s/e/w).")

# TODO 6: after the loop ends, print "You won in <tries> tries!" with an f-string
```

---

## Hints (use sparingly)
- Normalize **before** any comparisons: `direction = input(...).strip().lower()`  
- Membership check: `if direction in valid:`  
- Combine conditions with **or**; keep them readable (helper booleans help)  
- Indentation matters: use **4 spaces**, not tabs

---

## Quick Self‑Check
- [ ] The game only ends when `found` becomes **True**  
- [ ] Menu prints **each** loop (the `for` is **inside** the `while`)  
- [ ] Input like `"  EAST  "` works because you normalized it  
- [ ] You used an **f-string** for the final win message with the try count
```
