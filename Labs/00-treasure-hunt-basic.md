# 00 — Treasure Hunt (Basic)

> ### Quick Summary
> **Level:** 00 • **Time:** 30–45 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> **Hardware:** Raspberry Pi 500 + Thonny (or any Python 3)  
> **You’ll practice:** `print()`, `input()`, variables & types, **lists + membership**, `if/elif/else`, **for/while loops**, **f-strings**, boolean shortcuts, input cleaning

# Why This Matters
The core moves from the **Python Basics** guide—print, input, variables, lists, decisions, and loops—show up in almost every program. This mini‑game glues them together so you can *use* them, not just read about them.

> **Learn → Try → Do**  
> - **Learn** + **Try** in the Guide.  
> - **Do** here in the Lab.

---

# What You’ll Build
A tiny **text‑adventure** where the player types directions (north/south/east/west) until they find treasure. The game loops, handles messy input (like `EAST` or extra spaces), validates against a **list of allowed options**, and celebrates the win.

---

# Outcomes
By the end you can:
- Read and sanitize user input with `.strip().lower()`  
- Track state with variables (`found`, `tries`) of the correct **type**  
- Keep allowed options in a **list** and check with `in` (membership)  
- Make decisions with `if/elif/else` (with a simple **`or`** shortcut check)  
- Loop with `while` until a condition changes; use a tiny **for** loop to print a menu  
- Print clean messages using **f‑strings**  
- Explain why the loop stops and how indentation groups code

---

# Setup
- On a **Raspberry Pi 500**, open **Thonny** (Menu → Programming → Thonny).  
- Create a new file named `treasure.py` in `~/Documents/CodeCreate/`.  
- Click **Run ▶** to execute; watch the **Shell** for input/output.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/00-treasure-hunt-basic/STUDENT_START.md)** and reveal the Full Starter to compare with your approach.

## 1) Plan (2–3 min)
Pick which direction hides the treasure. Decide what message each wrong direction shows.  
> From the Guide: use **strings**, **variables**, and **if/elif/else**.

**Try:** Make a **list** of valid directions for later:
```python
valid = ["north", "south", "east", "west"]
```

## 2) Start the Loop (4–5 min)
Create variables and a `while` loop that repeats until the player wins.
```python
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

found = False          # bool (True/False)
tries = 0              # int (count of guesses)
valid = ["north", "south", "east", "west"]
WIN = "???"            # pick: "north", "south", "east", or "west"

while not found:
    # we'll fill this in next
    pass
```
> Same indentation = same block. Run now to confirm no errors.

## 3) Show a Menu with a **for** Loop (2–3 min)
Print the valid options once each loop *before* asking for input.
```python
# inside the while loop, just before asking input:
for d in valid:
    print(f"- {d}")
```

## 4) Read, Normalize, and Count (2–3 min)
Replace `pass` with an input line, clean it, and increase the counter.
```python
direction = input("Which way? ").strip().lower()  # string → normalized
tries += 1                                        # int → add 1
```

## 5) Validate with **membership** and Decide (8–10 min)
Use `if/elif/else` to respond. First, check if the input is one of the allowed words or their shortcut letters.

**Checklist**
- If the choice matches `WIN` **or** its shortcut (`n/s/e/w`), celebrate and set `found = True`  
- Else if the choice is a **valid** direction but not the winner, print your own message  
- Else print a helpful nudge (invalid word)

**Pattern you can adapt**
```python
# full‑word or shortcut match helper:
is_east = (direction == "east") or (direction == "e")
is_north = (direction == "north") or (direction == "n")
is_south = (direction == "south") or (direction == "s")
is_west  = (direction == "west")  or (direction == "w")

# decide what happens
if (WIN == "east"  and is_east) or    (WIN == "north" and is_north) or    (WIN == "south" and is_south) or    (WIN == "west"  and is_west):
    print(f"You found the treasure in {tries} moves!")
    found = True
elif direction in valid or direction in ["n", "s", "e", "w"]:
    print("Not here—keep exploring...")
else:
    print("Try north, south, east, or west (n/s/e/w).")
```

> From the Guide: `in` checks membership in a list; boolean `or` lets shortcuts work.

## 6) Wrap Up (1–2 min)
After the loop ends, report how many tries it took.
```python
print(f"You won in {tries} tries!")
```

---

# Skeleton Starter (copy/paste and fill the TODOs)
Use this starter and the **Python Basics** guide to fill each TODO.  
If you get stuck for 5–7 minutes, open **STUDENT_START.md** in the Example_Code folder.

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

    # TODO 2: read and normalize input into 'direction' using .strip().lower()
    # direction = ...

    # TODO 3: build helper booleans for shortcuts (e.g., is_east = direction == "east" or direction == "e")

    # TODO 4: if direction matches the WIN (full word or shortcut):
    #         - print a win message with an f-string AND set found = True
    #     elif direction is valid (full or shortcut but not WIN):
    #         - print a custom hint
    #     else:
    #         - print a nudge to use the allowed options
    #
    # Hints:
    # - membership: if direction in valid:
    # - combine conditions with or/and

    # TODO 5: increase tries by 1
    # tries += 1

# TODO 6: after the loop ends, print "You won in <tries> tries!" with an f-string
```

---

# Demo / Submission Checklist
- [ ] The game **loops** until treasure is found (uses a `while` with a boolean condition).  
- [ ] Input is **case‑insensitive** and ignores spaces (`.strip().lower()`).  
- [ ] A tiny **for** loop prints the options menu each loop.  
- [ ] **List membership** is used to validate allowed inputs (`direction in valid`).  
- [ ] Shortcuts (`n/s/e/w`) are accepted via simple boolean checks with **`or`**.  
- [ ] Clear win message uses an **f‑string** that includes the number of tries.  
- [ ] Indentation is consistent (4 spaces).

---

# Make It Yours — Extensions (choose one)
- **Limited tries (numbers):** Ask the player how many tries they want (e.g., `max_tries = int(input("Max tries? "))`). End with “Game over” if they run out.  
- **Directional hint:** After 3 wrong tries, print a hint like “Think sunrise or sunset…”.  
- **Mini‑map:** Track simple rooms (e.g., `start → east → treasure`). Print a hint after 2 wrong moves.  
- **ASCII treasure:** Print a tiny ASCII chest on win.

> Tip: If you prompt for numbers, remember `input()` returns **text**—convert with `int(...)` or `float(...)` as shown in the Guide. Consider validating the text before converting.

---

# Troubleshooting
- **Loop never ends** → Forgot to set `found = True` on win.  
- **Case problems** → Comparing `"East"` to `"east"` → Normalize with `.strip().lower()`.  
- **`IndentationError`** → Mixed tabs/spaces → Use **4 spaces** consistently.  
- **Menu prints once** → Your `for` loop is outside the `while` loop; move it inside.  
- **Shortcuts don’t work** → Re‑check your boolean `or` comparisons.  
- **`ValueError` on int(...)** → You tried to convert non‑numeric text; keep this in an extension, or validate first.

---

# Reflection (1–2 sentences)
- What part was trickiest—lists & membership, conditionals, or loop control?  
- If you had more time, what feature would you add next and why?

---

# Next Up
Level up to **[01 — Python Functions](../Guides/01-python-functions.md)** to refactor this game into reusable pieces.
