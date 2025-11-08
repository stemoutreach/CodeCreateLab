# 00 — Python Basics

> ### Quick Summary
> **Level:** 00 • **Time:** 35–60 min  
> **Prereqs:** None  
> **Hardware:** Raspberry Pi 500 (Raspberry Pi OS)  
> **You’ll practice:** `print()`/`input()`, variables & types, `if/elif/else`, **for** & **while** loops, **f-strings**, boolean logic, indentation, common errors

# Why This Matters
These are your day-one Python moves. You’ll reuse them in every guide and lab—from Sense HAT pixels to driving a robot. Learn the patterns now to move faster later.

---
## What you’ll learn
- Print messages and read keyboard input
- Store/update values in variables; tell strings vs. numbers
- Convert input text to numbers for math (safely)
- Make decisions with `if / elif / else` and comparisons
- Repeat with **for** (counted repeats) and **while** (repeat while true)
- Combine conditions with booleans (`and`, `or`, `not`)
- Format output cleanly with **f-strings**
- Avoid common mistakes with indentation and types

## Setup
- On a **Raspberry Pi 500**, open **Thonny** (Menu → Programming → Thonny).
- Create a new file named `basics.py` in a folder you can find (e.g., `Documents/CodeCreate/`).
- Click **Run ▶**. Results appear in the **Shell** (bottom pane).

---
## 1) Print a message (your program “talks”)
**Idea**: `print()` shows information to the user.  
**When to use**: Any time you need feedback (debugging, prompts, results).  
**Pattern**:
```python
print(<thing>, <another_thing>, ...)
```
**Try it**
```python
print("Welcome to Python!")
print(3 + 4)                 # prints the RESULT 7
print("3 + 4")               # prints the TEXT 3 + 4
print("Hi", "there", 2025)   # prints items with spaces
```
**Common mistakes**
- Missing quotes around text → `NameError`
- Unmatched quotes/parentheses → `SyntaxError`
**Checkpoint**: Explain the difference between printing a **value** vs. a **string** that looks like code.

---
## 2) Variables & types (names for values)
**Idea**: A **variable** stores a value so you can reuse or change it. The **type** (`str`, `int`, `float`, `bool`) tells Python how to treat that value (text vs. number, etc.).  
**When to use**: Any time you need to keep a value for later or update it during the program.

**Pattern**
```python
name = "Kai"     # str (text)
score = 10       # int (whole number)
pi = 3.14        # float (decimal)
truth = True     # bool (True/False)
```

**Inspecting types (know what you’re holding)**
```python
a = "5"
b = 5
print(type(a))   # <class 'str'>
print(type(b))   # <class 'int'>
```

**Try it (see values change and print results)**
```python
score = 10
print("Start score:", score)

score = score + 5
print("After +5:", score)

score += 5                   # shortcut for score = score + 5
print("After another +5:", score)

# Doing math with input text? Convert first:
age_text = "12"              # imagine this came from input()
age = int(age_text)          # now it's an int
print("Next year age:", age + 1)

# Turn numbers back into text if you need to join with strings:
msg = "Player " + str(score) # or use an f-string:
print(f"Score message: {msg} / f-string: Player score is {score}")
```

**Naming tips**
- Use snake_case: `player_name`, `total_points`
- Don’t start with a number; avoid spaces; be descriptive

**What is `snake_case`?**
`snake_case` means all lowercase words separated by underscores. It’s the Python style for variable and function names (PEP 8).

**Why use it?** Consistent, readable, and it matches community standards.

**Do**
```python
player_name = "Kai"
total_points = 15
max_speed = 3.2
is_ready = True
```

**Don’t**
```python
playerName = "Kai"     # camelCase (common in JavaScript, not Python)
TotalPoints = 15       # PascalCase (used for Classes in Python)
max-speed = 3.2        # hyphen is illegal in identifiers
2players = 2           # cannot start with a digit
```

**Rules of thumb**
- Use letters, digits, and underscores only; start with a **letter** or underscore.
- Keep it descriptive but short: `laps_completed`, not `l`.
- Reserve `PascalCase` for **Class** names, e.g., `class GameController:`.

**Common mistakes**
- Mixing types by accident (e.g., `score = '5'` and later `score + 1`)  
- Illegal names (start with a number, have spaces) or using keywords (`for`, `if`)  
- Case sensitivity: `Score` and `score` are different  
- Typo: `a =+ 1` (this sets `a` to `+1`) instead of `a += 1`

**Checkpoint**
- Explain the difference between `str`, `int`, `float`, and `bool`.  
- Given `x = "7"` and `y = 3`, write one line that prints `10` (hint: convert `x`).

---
## 3) Read input (and convert when needed)
**Idea**: `input()` pauses and returns what the user typed **as a string**.  
**When to use**: You need the user to choose, answer, or confirm.  
**Pattern**:
```python
answer_text = input("<question> ")
# convert if you need a number:
answer_number = int(answer_text)   # or float(...)
```
**Try it**
```python
name = input("What is your name? ")
print("Hi", name)

age_text = input("How old are you? ")
age = int(age_text)      # or float(...) for decimals
print("Next year you’ll be", age + 1)
```

**About `int()` (quick reference)**
- `int(x)` converts a number-like **string** or **float** to an integer. Examples: `int("42") → 42`, `int(3.9) → 3` (truncates).
- `int(x, base)` lets you parse other number bases: `int("101", 2) → 5`, `int("1A", 16) → 26`.
- Whitespace is okay: `int("  7\n") → 7`.
- **Decimals**: if the text has a decimal point (e.g., `"3.14"`), use `float("3.14")` first, or read as `float` directly.
- **Errors**: if text isn’t number-like (`"five"`), Python raises `ValueError`.

**Safe conversion pattern**
```python
raw = input("Enter a whole number: ").strip()
try:
    n = int(raw)          # or: n = int(raw, 10) for explicit base
    print("You typed:", n)
except ValueError:
    print("Oops — please type digits only (0–9).")
```

**About `float()` (quick reference)**
- `float("3.14") → 3.14`, `float(5) → 5.0`.
- Handles scientific notation: `float("1e3") → 1000.0`.
- Ignores surrounding spaces/newlines: `float("  2.5\n") → 2.5`.
- Errors for non-number text raise `ValueError`.

**Rounding & truncation (quick reference)**
- `round(x)` rounds to nearest integer (banker’s rounding for .5 cases).  
  `round(2.5) → 2`, `round(3.5) → 4`
- `round(x, n)` rounds to `n` decimal places: `round(3.14159, 2) → 3.14`.
- `int(x)` **truncates** toward zero: `int(3.9) → 3`, `int(-3.9) → -3`.

**Gotchas**
- Doing math with a string → `"5" + 1` ❌; use `int("5") + 1` ✅
- Forgetting to store the result of `input()`  
**Checkpoint**: Explain why `input()` gives a string and how to convert it.

---
## 4) Decisions: `if / elif / else`
**Idea**: Run code only if a condition is true. `elif` = extra check; `else` = everything else.  
**When to use**: You need branching behavior.  
**Pattern**:
```python
if condition_a:
    ...
elif condition_b:
    ...
else:
    ...
```
**Try it**
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
```
**Common mistakes**
- Missing colon `:` after `if/elif/else`
- Using `=` (assignment) instead of `==` (comparison)  
**Checkpoint**: Describe which path runs for a given input and why.

---
## 5) Loops two ways: **for** vs. **while**
**Idea**: Repeat actions. **for** repeats a known count; **while** repeats *until* a condition changes.  
**When to use**: Lists/counts → **for**. Waiting for a condition/user action → **while**.  
**Patterns**
```python
# for: counted repeats
for i in range(start, stop_inclusive_plus_one):
    ...

# while: repeat while condition is True
while condition:
    ...
```
**Try it**
```python
for i in range(1, 6):   # 1,2,3,4,5
    print(i)

count = 1
while count <= 5:
    print(count)
    count += 1

# Input loop (quit to stop)
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
**Checkpoint**: Choose **for** or **while** for a task and justify your choice.

---
## 6) Clean printing with **f-strings**
**Idea**: Build readable strings without clumsy `+` or commas.  
**When to use**: Any time you combine text with values.  
**Pattern**:
```python
print(f"{name} scored {score}")
```
**Try it**
```python
name = "Kai"
score = 87
print(f"{name} scored {score}")
```
**Common mistakes**
- Forgetting the `f` before the opening quote
- Putting quotes inside braces `{}` — keep expressions simple  
**Checkpoint**: Convert a `print("X", val)` line to an f-string.

---
## 7) Booleans & logic combos (True/False thinking)
**Idea**: A **boolean** is either `True` or `False`. Combine conditions with **and**, **or**, **not** to make smarter decisions.  
**When to use**: Permissions, safety checks, multi-rule decisions.  
**Truth table (mental model)**
- `A and B` is `True` only if **both** are True.  
- `A or B` is `True` if **either** is True.  
- `not A` flips True ↔ False.
**Pattern**:
```python
if (age >= 13 and age <= 18) or with_adult:
    print("Allowed")
```
**Try it**
```python
age = int(input("Age: "))
with_adult = input("With adult? (y/n) ").lower() == "y"

if (13 <= age <= 18) or with_adult:
    print("Allowed")
else:
    print("Not allowed")
```
**Common mistakes**
- Misreading precedence in `A or B and C` — add parentheses to show intent.
- Using strings `"True"/"False"` instead of real booleans `True/False`.  
**Checkpoint**: Explain why an 11-year-old with an adult passes, but an 11-year-old alone does not.

---
## 8) Comments & indentation (syntax that saves you)
**Idea**: Comments explain your thinking; indentation defines **blocks** of code.  
**When to use**: Always—comments for clarity; indentation because Python requires it.  
**Pattern**:
```python
# This is a comment
if True:
    print("Indented lines belong together")
print("This line is outside the if.")
```
**Rules of thumb**
- Use **4 spaces** per level (don’t mix tabs and spaces).  
- All lines at the same indentation belong to the same block.  
**Checkpoint**: Move `print("Hello")` inside and outside an `if` to see the effect.

---

**Common mistakes**
- Mixing **tabs** and **spaces** → causes `IndentationError`.
- Misaligned blocks: one line off breaks the block.
- Commenting out code but leaving a dangling `:` above a block.
## Vocabulary
- **String**: text in quotes, e.g., `"hello"`  
- **Integer / Float**: whole number / decimal, e.g., `3`, `3.14`  
- **Variable**: named storage for a value, e.g., `score = 0`  
- **Boolean**: `True` or `False`  
- **Expression**: a combination of values/variables/operators that evaluates to a single result, e.g., `3 + x`  
- **Operator**: a symbol that performs an action, e.g., `+ - * /`  
- **Comparison operator**: checks relationships, e.g., `== != < <= > >=`  
- **Logical operator**: combines conditions: `and`, `or`, `not`  
- **Condition**: an expression that’s `True` or `False`  
- **Block**: a group of indented lines that run together (after `if`, `elif`, `else`, `for`, `while`)  
- **Cast / Type conversion**: turning a string into a number (or vice versa), e.g., `int("5")`  
- **Input / Output**: `input()` reads from the keyboard; `print()` shows results  
- **f-string**: formatted string literal like `f"{name} scored {score}"`

---
## Check your understanding
1. What does `input()` return by default? Give an example where you must convert the result.  
2. Why does `"5" + 1` cause an error, and how do you fix it (two different ways)?  
3. What’s the difference between `=` and `==`? Show a one-line example of each.  
4. How do you compare `"NORTH"` and `"north"` equally? Write a single `if` line.  
5. When would you pick a **for** loop vs. a **while** loop? Give one example for each.  
6. In your own words, explain `and`, `or`, and `not` with a tiny example.  
7. Predict the output:  
   ```python
   a = 3
   b = 5
   print(a + b * 2)
   print((a + b) * 2)
   print(not (a < b and b < 10))
   ```  
8. Identify the bug and fix it:
   ```python
   age = input("Age? ")
   if age >= 13:
       print("Teen")
   ```

---
## Mini practice (choose 2–3)
- **Loop count:** print numbers 1–5 with **for** and with **while**.  
- **Name letters:** ask for a name, then print each letter on a new line.  
- **Score card:** ask for a name + score, print `"<name> scored <score>"` using an **f-string**.  
- **Echo loop:** repeatedly ask for a word and echo it back until the user types `quit`.  
- **Temperature converter:** ask for °C and print °F using `F = C * 9/5 + 32` (use `float`).  
- **Even or odd:** read a number and print `even` or `odd`. Repeat until blank input.  
- **Menu loop:** show a tiny menu (`1) greet  2) add  3) quit`) and perform the choice.  
- **Times table:** ask for `n` and print the `n` times table from 1–10 using a loop.

### Stretch
- **Sum until blank:** keep asking for integers and print the running total; stop on blank input.  
- **Guessing game:** pick a secret number 1–10 and let the user guess until correct; give hints `higher/lower`.  
- **Simple calculator:** read `a`, operator, `b` and print the result for `+ - * /` (skip error handling for now).  
- **Refactor to f-strings:** take any `print` that uses commas or `+` and rewrite with one f-string.

---
## Troubleshooting
- **IndentationError** → lines in a block don’t line up (use 4 spaces).  
- **`TypeError: can only concatenate str (not "int") to str`** → use `int(...)` or an **f-string**.  
- **`NameError`** → variable used before assignment or spelled differently.  
- **Stuck in a loop** → change something each time or use `break`.  
- **No output** → is `print` inside the loop/block? Is your code saved and run?

---
## Next up
Jump into the lab: **[01 — Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**.
