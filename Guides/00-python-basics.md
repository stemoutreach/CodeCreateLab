# Python Basics

> ### Quick Summary
> **Level:** 00 • **Time:** 30–60 min  
> **Prereqs:** None  
> **Hardware:** Computer only  
> **You’ll practice:** print(), input(), variables, if/elif/else, while loops

# Why This Matters
These are the five moves you’ll use in almost every Python program. Learn them well here—you’ll reuse them immediately in the **Treasure Hunt (Basic)** lab and throughout later guides.

---

## What you’ll learn
- Printing text to the screen with `print()`
- Reading keyboard input with `input()`
- Storing and updating values in **variables**
- Making decisions with **if / elif / else**
- Repeating actions with **while** loops
- Indentation rules and common errors to avoid

## Setup
- Any Python 3 environment (installed locally or browser-based).
- If provided, download starters from `Example_Code/00-python-basics/`.

---

## Walkthrough — Step by Step (with explanations)

### 1) Print a message
**Idea:** `print()` shows information to the user. It’s how your program “talks.”

**Anatomy**
- `print` is a built‑in **function**.
- `("Welcome")` are the **parentheses** with the thing to print (an **argument**).
- Text inside quotes is a **string**.

```python
print("Welcome to Python!")
```

**Try variants**
```python
print(3 + 4)               # prints the RESULT of math → 7
print("3 + 4")             # prints the TEXT "3 + 4"
print("Hi", "there", 2025) # prints items with spaces
```

**Common mistakes**
- Missing quotes around text → `NameError`
- Unmatched quotes → `SyntaxError`

---

### 2) Ask the user for input
**Idea:** `input()` pauses the program and waits for the user to type. It **always returns a string**.

```python
name = input("What is your name? ")
print("Hi", name)
```

**Breaking it down**
- The text inside `input("...")` is a **prompt**.
- The result is stored in `name` (a variable).
- `print()` displays the combined message.

**Numbers from input**
`input()` returns a string. Convert to a number if you need math:

```python
age_text = input("How old are you? ")
age = int(age_text)     # or float(...) for decimals
print("Next year you’ll be", age + 1)
```

**Common mistakes**
- Doing math with strings: `"5" + 1` ❌ → convert first: `int("5") + 1` ✅
- Forgetting to store the result: `input("...")` returns a value—save it!

---

### 3) Store values in variables
**Idea:** Variables keep data so you can reuse or change it later.

```python
score = 10         # create
score = score + 5  # update
print(score)       # 15
```

**Rules & tips**
- Variable names: letters, numbers, `_`, but **don’t start with a number**.
- Use **snake_case**: `total_points`, `player_name`.
- Make names meaningful: `hp` is worse than `player_health` (until you learn conventions).

**Shortcuts**
```python
score += 5   # same as score = score + 5
count -= 1   # same as count = count - 1
```

**Strings vs. numbers**
```python
a = "5"      # string
b = 5        # int
print(a + a) # "55"
print(b + b) # 10
```

**Common mistakes**
- Reusing a variable before assigning it → `NameError`
- Confusing `=` (assignment) with `==` (comparison)

---

### 4) Make a decision with if
**Idea:** Run certain code only if a condition is true. Use `elif` for extra checks, `else` for “everything else.”

```python
direction = input("Which way? ").lower()

if direction == "north":
    print("You hit a wall.")
elif direction == "east":
    print("You found a hallway.")
else:
    print("Hmm… try another direction.")
```

**Breaking it down**
- `==` tests equality. (`=` assigns.)
- `.lower()` normalizes input (so “NORTH” equals “north”).

**Comparisons & logic**
```python
temperature = 72
if temperature > 80:
    print("Hot")
elif 60 <= temperature <= 80:
    print("Nice")
else:
    print("Chilly")

# combine with and/or/not
has_key = True
door_locked = True
if has_key and door_locked:
    print("You unlock the door.")
```

**Common mistakes**
- Missing colon `:` after `if`, `elif`, or `else`
- Inconsistent indentation (mixing tabs/spaces). Use 4 spaces.
- Using `=` instead of `==` in conditions

---

### 5) Repeat with while
**Idea:** A `while` loop repeats **as long as** its condition is true.

```python
keep_going = True
count = 0

while keep_going:
    print("Looping...", count)
    count += 1
    if count == 3:
        keep_going = False
```

**Breaking it down**
- The condition is checked **before every loop**.
- Something inside should change the condition; otherwise you get an **infinite loop**.

**Typical patterns**
```python
# Count up
i = 1
while i <= 5:
    print(i)
    i += 1

# Input loop (quit to stop)
while True:
    cmd = input("Command (quit to stop): ").lower()
    if cmd == "quit":
        print("Bye!")
        break
    print("You typed:", cmd)
```

**Common mistakes**
- Forgetting to update the loop variable
- Using `== True` or `== False` unnecessarily (just use the variable directly)

---

## Indentation rules (super important)
- Code blocks (after `if`, `elif`, `else`, `while`, `def`) must be **indented**.
- Use **4 spaces** per level. Don’t mix tabs and spaces.
- Everything in the same block lines up vertically.

```python
if ready:
    print("Start")      # indented = inside the if
print("Always runs")    # not indented = outside the if
```

---

## Vocabulary
- **String**: text (inside quotes), e.g., `"hello"`  
- **Integer / Float**: whole number / decimal, e.g., `3`, `3.14`  
- **Variable**: named storage for a value, e.g., `score = 0`  
- **Boolean**: `True` or `False`  
- **Condition**: an expression that’s `True` or `False`  
- **Loop**: repeats code while a condition is `True`

---

## Check your understanding
1. What does `input()` return by default?  
2. Why might `"5" + 1` cause an error? How do you fix it?  
3. What’s the difference between `=` and `==`?  
4. How can you make sure user input like `"NORTH"` and `"north"` compare equally?  
5. What causes an infinite loop, and how do you prevent it?

---

## Try it: Mini‑exercise
Write a mini greeter:
1. Ask for **name** and **favorite color**.  
2. If the color is `"blue"` or `"green"`, print `"Great choice!"`, else print `"Nice!"`.  
3. Ask how many stickers they want (a number).  
4. Use a `while` loop to print `"Sticker #1"`, `"Sticker #2"`, … up to that number.

**Stretch goals**
- Accept `"Blue"`/`"BLUE"` using `.lower()`  
- Validate the number: if the user types a non-number, ask again

---

## Troubleshooting
- **`NameError: name 'x' is not defined`** → Use a variable only after assignment; check spelling.  
- **`SyntaxError`** → Look for missing quotes, parentheses, or colons.  
- **`IndentationError`** → Make sure blocks are indented with the same 4 spaces.  
- **Stuck loop** → Add a change inside the `while`, or use `break`.  
- **Unexpected string math** → Convert inputs with `int(...)` or `float(...)` first.

---

## Next up
Do the matching lab: **[00 – Treasure Hunt (Basic)](../Labs/00-treasure-hunt-basic.md)**

## Attributions & License
- Examples adapted from the original “0 Python Basics Guide.”  
- See repository LICENSE for terms.
