# 00 — Treasure Hunt (Basic)

> ### Quick Summary
> **Level:** 00 • **Time:** 30–45 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> **Hardware:** Computer only (Python 3 or browser-based)  
> **You’ll practice:** `print()`, `input()`, variables, `if/elif/else`, `while` loops, string normalization

# Why This Matters
The five Python moves from the **Python Basics** guide—`print`, `input`, variables, decisions, and loops—show up in almost every program you’ll ever write. This mini game glues them together so you can *use* them, not just read about them.

---

# What You’ll Build
A tiny **text‑adventure** where the player types directions (north/south/east/west) until they find treasure. The game keeps looping, handles messy input (like `EAST` or extra spaces), and celebrates the win.

---

# Outcomes
By the end you can:
- Read and sanitize user input with `.strip().lower()`
- Track state with variables (`found`, `tries`)
- Make decisions with `if/elif/else`
- Loop with `while` until a condition changes
- Print a clear success message

---

# Setup
- Use any Python 3 environment (local install or browser).  
- Optional: create a new folder `Labs/00-treasure-hunt-basic/` for your code.

---

# Steps

## 1) Plan (2–3 min)
Pick which direction hides the treasure. Decide what message each wrong direction shows.

> From the Guide: you’ll use **strings**, **variables**, and **if/elif/else** here.

## 2) Start the Loop (5 min)
Create variables and a `while` loop that repeats until the player wins.

```python
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing a direction: north, south, east, or west.")

found = False
tries = 0

while not found:
    # we’ll fill this in next
    pass
```

> From the Guide: a loop keeps running **while** its condition is true.

## 3) Read & Normalize Input (5 min)
Replace the `pass` with an input line and standardize it.

```python
direction = input("Which way? ").strip().lower()
tries += 1
```

> From the Guide: `input()` returns a **string**. `.strip().lower()` cleans it up for comparisons.

## 4) Decide What Happens (10 min)
Use `if/elif/else` to respond to each direction. Set `found = True` on the winning move.

```python
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
```

> From the Guide: don’t confuse `==` (comparison) with `=` (assignment).

## 5) Celebrate & Report (1–2 min)
After the loop ends, print how many tries it took.

```python
print(f"You won in {tries} tries!")
```

---

# Full Starter (copy if you want a head start)
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

---

# Demo / Submission Checklist
- [ ] The game **loops** until treasure is found.  
- [ ] Input is **case‑insensitive** and ignores extra spaces (`.strip().lower()`).  
- [ ] Clear **win** message appears.  
- [ ] Invalid inputs don’t crash the program.  
- [ ] Variables and logic are neatly **indented** (4 spaces).

---

# Make It Yours — Extensions (pick one)
- **Limited tries:** Give the player **5 attempts**. Show remaining tries; if it hits zero, print “Game over.”
- **Mini‑map:** Track simple rooms (e.g., `start -> east -> treasure`). Print a hint after 2 wrong tries.
- **Shortcuts:** Accept single letters `n/s/e/w` *and* full words.
- **Flavor:** Add a short intro story or simple ASCII art treasure chest.

---

# Troubleshooting
- **Loop never ends** → Forgot to set `found = True` when they win → Set it inside the correct branch.  
- **Case problems** → Comparing `"East"` to `"east"` → Normalize with `.strip().lower()`.  
- **`IndentationError`** → Mixed tabs/spaces → Use **4 spaces** consistently.  
- **Nothing prints** → Your `print()` calls are outside the right block → Align with indentation rules.  
- **Weird math with input** → You didn’t convert strings → Use `int(...)`/`float(...)` *if* you add numbers.

---

# Reflection (1–2 sentences)
- What part was trickiest—loops, conditionals, or input handling?  
- If you had more time, what feature would you add next and why?

---

# Next Up
Level up to **[01 — Python Functions](../Guides/01-python-functions.md)** to learn how to break your game into reusable pieces.
