# 00 — Python Basics

> ### Quick Summary
> **Level:** 00 • **Time:** 35–60 min  
> **Prereqs:** None  
> **Hardware:** Raspberry Pi 500 (Raspberry Pi OS)  
> **You’ll practice:** `print()`/`input()`, variables & types, `if/elif/else`, **for** & **while** loops, **f‑strings**, boolean logic, indentation, common errors

# Why This Matters
These are your day‑one Python moves. You’ll reuse them in every guide and lab—from Sense HAT pixels to driving a robot. Learn the patterns now to move faster later.

---
## What you’ll learn
- Print messages and read keyboard input
- Store/update values in variables; tell strings vs. numbers
- Convert input text to numbers for math
- Make decisions with `if / elif / else` and comparisons
- Repeat with **for** (counted repeats) and **while** (repeat while true)
- Format output cleanly with **f‑strings**
- Avoid common mistakes with indentation and types

## Setup
- On a **Raspberry Pi 500**, open **Thonny** (Menu → Programming → Thonny).
- Create a new file named `basics.py` in a folder you can find (e.g., `Documents/CodeCreate/`).
- Click **Run ▶**. Results appear in the **Shell** (bottom pane).

---
## 1) Print a message (your program “talks”)
**Idea:** `print()` shows information to the user.

```python
print("Welcome to Python!")
print(3 + 4)                 # prints the RESULT 7
print("3 + 4")               # prints the TEXT 3 + 4
print("Hi", "there", 2025)   # prints items with spaces
```

**Common mistakes**
- Missing quotes around text → `NameError`
- Unmatched quotes/parentheses → `SyntaxError`

---
## 2) Read input (and convert when needed)
**Idea:** `input()` pauses and returns what the user typed **as a string**.

```python
name = input("What is your name? ")
print("Hi", name)
```

**Numbers from input**
```python
age_text = input("How old are you? ")
age = int(age_text)      # or float(...) for decimals
print("Next year you’ll be", age + 1)
```

**Gotchas**
- Doing math with a string → `"5" + 1` ❌; use `int("5") + 1` ✅
- Forgetting to store the result of `input()`

---
## 3) Variables & types (names for values)
**Idea:** Variables keep data so you can reuse or change it.

```python
score = 10          # create
score = score + 5   # update
print(score)        # 15
```

**Shortcuts & types**
```python
score += 5          # same as score = score + 5
a = "5"             # string
b = 5               # int
print(type(a), type(b))
```

**Naming tips**
- Use snake_case: `player_name`, `total_points`
- Don’t start with a number; be descriptive

---
## 4) Decisions: `if / elif / else`
**Idea:** Run code only if a condition is true. Use `elif` for extra checks, `else` for “everything else.”

```python
direction = input("Which way? ").lower()

if direction == "north":
    print("You hit a wall.")
elif direction == "east":
    print("You found a hallway.")
else:
    print("Try another direction.")
```

**Comparisons & logic**
```python
temperature = 72
if temperature > 80:
    print("Hot")
elif 60 <= temperature <= 80:
    print("Nice")
else:
    print("Chilly")

has_key = True
door_locked = True
if has_key and door_locked:
    print("You unlock the door.")
```

**Mistakes to avoid**
- Missing colon `:` after `if/elif/else`
- Using `=` (assignment) instead of `==` (comparison)

---
## 5) Loops two ways: **for** vs. **while**
**Rule of thumb:**  
- Use **for** when you know how many times to repeat.  
- Use **while** when you repeat *until* something changes.

**for — counted repeats**
```python
for i in range(1, 6):   # 1,2,3,4,5
    print(i)
```

**while — repeat while condition is true**
```python
count = 1
while count <= 5:
    print(count)
    count += 1
```

**Input loop pattern (quit to stop)**
```python
while True:
    cmd = input("Command (quit to stop): ").lower()
    if cmd == "quit":
        print("Bye!")
        break
    print("You typed:", cmd)
```

**Common mistakes**
- Forgetting to change something inside a `while` → infinite loop
- Printing outside the loop (indent wrong) → prints once instead of many times

---
## 6) Clean printing with **f‑strings**
```python
name = "Kai"
score = 87
print(f"{name} scored {score}")
# No + needed—just write what you want to see.
```

---
## 7) Booleans & logic combos
```python
age = 12
with_adult = True
if age >= 13 or with_adult:
    print("Allowed")
```

Use **and**, **or**, **not** to combine conditions.

---
## 8) Comments & indentation (syntax that saves you)
```python
# This is a comment
if True:
    print("Indented lines belong together")
print("This line is outside the if.")
```
- Use **4 spaces** per level (don’t mix tabs and spaces).
- Same indentation = same block.

---
## Vocabulary
- **String**: text in quotes, e.g., `"hello"`  
- **Integer / Float**: whole number / decimal, e.g., `3`, `3.14`  
- **Variable**: named storage for a value, e.g., `score = 0`  
- **Boolean**: `True` or `False`  
- **Condition**: expression that’s `True`/`False`  
- **Loop**: repeats code while a condition holds (or for a count)

---
## Check your understanding
1. What does `input()` return by default?  
2. Why does `"5" + 1` cause an error, and how do you fix it?  
3. What’s the difference between `=` and `==`?  
4. How do you compare `"NORTH"` and `"north"` equally?  
5. When would you pick a **for** loop vs. a **while** loop?

---
## Mini practice (choose 1–2)
- **Loop count:** print numbers 1–5 with **for** and with **while**.  
- **Name letters:** ask for a name, then print each letter on a new line.  
- **Score card:** ask for a name + score, print `"<name> scored <score>"` using an **f‑string**.

### Stretch
- Print the **squares** from 1–10 on one line (hint: `end=" "` in `print`).  
- Accept ages **13–18** only (no adult override).

---
## Troubleshooting
- **IndentationError** → lines in a block don’t line up (use 4 spaces).  
- **`TypeError: can only concatenate str (not "int") to str`** → use `int(...)` or an **f‑string**.  
- **`NameError`** → variable used before assignment or spelled differently.  
- **Stuck in a loop** → change something each time or use `break`.  
- **No output** → is `print` inside the loop/block? Is your code saved and run?

---
## Next up
Move on to **[01 — Python Functions](01-python-functions.md)**, then try the lab **Treasure Hunt (Functions)**.
