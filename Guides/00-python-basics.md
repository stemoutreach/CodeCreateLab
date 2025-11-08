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
- Convert input text to numbers for math
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
**Checkpoint**: You can explain the difference between printing a **value** vs. a **string** that looks like code.

---
## 2) Read input (and convert when needed)
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
**Gotchas**
- Doing math with a string → `"5" + 1` ❌; use `int("5") + 1` ✅
- Forgetting to store the result of `input()`
**Checkpoint**: You can explain why `input()` gives a string and how to convert it.

---
## 3) Variables & types (names for values)
**Idea**: Variables keep data so you can reuse or change it. Types tell Python how to treat the data.  
**When to use**: Any time you need to remember something for later.  
**Pattern**:
```python
name = "Kai"     # str
score = 10       # int
pi = 3.14        # float
truth = True     # bool
```
**Try it**
```python
score = 10
score = score + 5
score += 5                 # shortcut
a = "5"; b = 5
print(type(a), type(b))
```
**Naming tips**
- Use snake_case: `player_name`, `total_points`
- Don’t start with a number; be descriptive
**Checkpoint**: You can state the type (`str`, `int`, `float`, `bool`) of a given literal.

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
**Checkpoint**: You can explain what path runs for a given input and why.

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
**Checkpoint**: You can choose **for** or **while** and justify your choice.

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
- Using quotes inside braces `{}` → keep expressions simple
**Checkpoint**: Convert a `print("X", val)` line to an f-string.

---
## 7) Booleans & logic combos (True/False thinking)
**Idea**: A **boolean** is either `True` or `False`. You combine conditions with **and**, **or**, **not** to make smarter decisions.  
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
age_text = input("Age: ")
age = int(age_text)
with_adult = input("With adult? (y/n) ").lower() == "y"

if (13 <= age <= 18) or with_adult:
    print("Allowed")
else:
    print("Not allowed")
```
**Common mistakes**
- Writing `13 <= age <= 18 or with_adult == True` then misunderstanding precedence.  
  Tip: add parentheses to make intent obvious.  
- Using strings `"True"/"False"` instead of real booleans `True/False`.
**Checkpoint**: Explain why an 11‑year‑old with an adult passes, but an 11‑year‑old alone does not.

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
- **f-string**: formatted string literal like `f\"{name} scored {score}\"`

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

## Troubleshooting
- **IndentationError** → lines in a block don’t line up (use 4 spaces).  
- **`TypeError: can only concatenate str (not "int") to str`** → use `int(...)` or an **f-string**.  
- **`NameError`** → variable used before assignment or spelled differently.  
- **Stuck in a loop** → change something each time or use `break`.  
- **No output** → is `print` inside the loop/block? Is your code saved and run?

---
## Next up
Jump into the lab: **[01 — Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**.
