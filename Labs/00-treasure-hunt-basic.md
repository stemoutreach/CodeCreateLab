# 00 — Treasure Hunt (Basic)

> ### Quick Summary
> **Level:** 00 • **Time:** 30–45 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> **Hardware:** Raspberry Pi 500 + Thonny (or any Python 3)  
> **You’ll practice:** `print()`, `input()`, variables, `if/elif/else`, **for/while loops**, **f-strings**, input cleaning

# Why This Matters
The core moves from the **Python Basics** guide—print, input, variables, decisions, and loops—show up in almost every program. This mini game glues them together so you can *use* them, not just read about them.

> **Learn → Try → Do**  
> - **Learn** + **Try** in the Guide.  
> - **Do** here in the Lab.

---

# What You’ll Build
A tiny **text-adventure** where the player types directions (north/south/east/west) until they find treasure. The game keeps looping, handles messy input (like `EAST` or extra spaces), and celebrates the win.

---

# Outcomes
By the end you can:
- Read and sanitize user input with `.strip().lower()`  
- Track state with variables (`found`, `tries`)  
- Make decisions with `if/elif/else` (with a simple **`or`** case)  
- Loop with `while` until a condition changes  
- Use a **for** loop over a small list (directions menu)  
- Print with **f-strings**

---

# Setup
- Open **Thonny** on your **Raspberry Pi 500** (Menu → Programming → Thonny).  
- Create a new file named `treasure.py` in `~/Documents/CodeCreate/`.  
- Click **Run ▶** to execute; watch the **Shell** for output.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/00-treasure-hunt-basic/STUDENT_START.md)** and reveal the Full Starter to compare with your approach.

## 1) Plan (2–3 min)
Pick which direction hides the treasure. Decide what message each wrong direction shows.  
> From the Guide: you’ll use **strings**, **variables**, and **if/elif/else** here.

**Try:** Make a **list** of valid directions for later:
```python
valid = ["north", "south", "east", "west"]
```

## 2) Start the Loop (5 min)
Create variables and a `while` loop that repeats until the player wins.
```python
# Game intro (note the comment and consistent indentation)
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

found = False
tries = 0
WIN = "???"  # pick: "north", "south", "east", or "west"

while not found:
    # we’ll fill this in next
    pass
```
> From the Guide: a loop keeps running **while** its condition is true. Same indentation = same block.

> **Quick test:** Run now—should print the intro and then loop (currently with `pass`). No errors yet.


## 3) Read & Normalize Input (4 min)
Replace the `pass` with an input line and standardize it.
```python
direction = input("Which way? ").strip().lower()
tries += 1
```
> From the Guide: `input()` returns a **string**. `.strip().lower()` cleans it up for comparisons.

## 4) Decide What Happens (8–10 min)
Use `if/elif/else` to respond to each direction. **Write your own** code using the checklist.

**Checklist**
- Compare the cleaned input to your `WIN` value.  
- On win: print a celebration with an **f-string** and set `found = True`.  
- On other valid directions: print your own messages.  
- On anything else: print a nudge to use north/south/east/west.   and **continue the loop**.
- **Bonus Boolean:** Accept **shortcuts** like `n/s/e/w` using `or`. Example pattern:
  ```python
  if direction == "east" or direction == "e":
      # treat as east
  ```

**Pseudocode (guide, not code)**
```
if direction matches WIN (full word or shortcut):
    celebrate; set found to True
elif direction is another valid word or shortcut:
    print your custom message
else:
    print a helpful nudge
```

## 5) Show a Menu with a **for** Loop (2–3 min)
Use a short **for** loop to print the valid options once at the top of the loop.
```python
# inside the while loop, just before asking input:
for d in valid:
    print(f"- {d}")
```
> From the Guide: Use `for` to repeat a known number of times or walk a list.

## 6) Celebrate & Report (1–2 min)
After the loop ends, print how many tries it took.
```python
print(f"You won in {tries} tries!")
```

---

# Skeleton Starter (start here)
Use this starter and the **Python Basics** guide to fill each TODO.  
If you get stuck for 5–7 minutes, open the **Student Start** helper: `../Example_Code/00-treasure-hunt-basic/STUDENT_START.md`.

```python
# 00 — Treasure Hunt (Basic)

# Intro
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

# State
found = False
tries = 0
valid = ["north", "south", "east", "west"]
WIN = "???"  # TODO: pick one: "north", "south", "east", or "west"

while not found:
    # TODO 1: print a short menu using a for loop over 'valid'
    # Example shape (not exact): for d in valid: print(f"- {d}")

    # TODO 2: read input into 'direction', then normalize with .strip().lower()
    direction = input("Which way? ")

    # TODO 3: compare 'direction' with WIN using if/elif/else
    # - If matches WIN or its shortcut (e.g., 'e' for 'east'): celebrate with an f-string and set found = True
    # - If direction is another valid word or shortcut: print your own message and keep looping
    # - Else: print a nudge to use north/south/east/west

    # TODO 4: increase tries by 1

# TODO 5: after the loop ends, report how many tries using an f-string
# Example: print(f"You won in {tries} tries!")

# Quick self-checks:
# 1) Typing " EAST  " works after normalization.
# 2) Shortcuts like 'n'/'s'/'e'/'w' work if you coded the boolean 'or' check.
# 3) The loop stops only when found = True.
# 4) 'tries' is > 0 when you win.
```

---

# Demo / Submission Checklist
- [ ] The game **loops** until treasure is found.  
- [ ] Input is **case-insensitive** and ignores extra spaces (`.strip().lower()`).  
- [ ] A tiny **for** loop prints the options menu once each loop.  
- [ ] Clear **win** message uses an **f-string**.  
- [ ] Shortcuts (`n/s/e/w`) are accepted via a simple **`or`** check.  
- [ ] Variables and logic are neatly **indented** (4 spaces).

---

# Make It Yours — Extensions (pick one)
- **Limited tries:** Give the player **5 attempts**. Show remaining tries; if it hits zero, print “Game over.”  
- **Mini-map:** Track simple rooms (e.g., `start -> east -> treasure`). Print a hint after 2 wrong tries.  
- **ASCII treasure:** Show a tiny ASCII art chest on win.  
- **Directional hint:** After 3 wrong tries, print “Think about the sunrise or sunset…”

---

# Troubleshooting
- **Loop never ends** → Forgot to set `found = True` in the win branch.  
- **Case problems** → Comparing `"East"` to `"east"` → Normalize with `.strip().lower()`.  
- **`IndentationError`** → Mixed tabs/spaces → Use **4 spaces** consistently.  
- **Menu spams** → Your `for` loop is outside the `while` loop; move it inside.  
- **Shortcuts don’t work** → Check your `or` comparisons for typos.

---

# Reflection (1–2 sentences)
- What part was trickiest—loops, conditionals, or input handling?  
- If you had more time, what feature would you add next and why?

---

# Next Up
Level up to **[01 — Python Functions](../Guides/01-python-functions.md)** to learn how to break your game into reusable pieces.
tries += 1  # increase tries immediately after reading input
