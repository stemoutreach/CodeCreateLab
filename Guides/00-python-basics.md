# Python Basics

> ### Quick info
> **Level:** 00 • **Time:** 30–45 min
> **Prereqs:** None
> **Hardware:** Computer only
> **You’ll practice:**
> - Use print() to display output
> - Read user input with input()
> - Store values in variables
> - Use if statements for simple decisions
> - Loop with while for repetition

# Why This Matters
This guide gives you the absolute essentials of Python—printing, input, variables, conditions, and loops—so you’re ready to complete the matching lab, **Treasure Hunt (Basic)**. Keep this open while you work; the lab will build directly on these skills.

## What you’ll learn
- Printing text to the screen
- Reading input from the keyboard
- Creating and updating variables
- Making decisions with `if`
- Repeating actions with `while`

## Setup
- Any computer with Python 3 or a browser-based Python environment will work.
- (If provided) Download starter code from `Example_Code/00-python-basics/`.

## Walkthrough

### 1) Print a message
Use `print()` to display text:
```python
print("Welcome to Python!")
```

### 2) Ask the user for input
`input()` returns a string you can store in a variable:
```python
name = input("What is your name? ")
print("Hi", name)
```

### 3) Store values in variables
Variables remember information for later:
```python
score = 10
# You can update it
score = score + 5
```

### 4) Make a decision with if
Run code only when a condition is true:
```python
direction = input("Which way? ").lower()

if direction == "north":
    print("You hit a wall.")
elif direction == "east":
    print("You found a hallway.")
else:
    print("Hmm… try another direction.")
```

### 5) Repeat with while
Do something multiple times (or until a condition changes):
```python
keep_going = True
count = 0

while keep_going:
    print("Looping...", count)
    count = count + 1
    if count == 3:
        keep_going = False
```

## Check your understanding
1. What does `input()` return by default (string, int, or bool)?
2. What happens if the condition in an `if` statement is false?
3. How do you stop a `while` loop that uses a boolean like `keep_going`?

## Try it: Mini-exercise
Create a short program that:
- Asks for your **name**
- Asks your **favorite color**
- Prints a friendly message combining both, e.g., `"Hi Ada, I like blue too!"`

## Troubleshooting
- **`NameError: name 'x' is not defined`** → You used a variable before creating it (check spelling and order).
- **Indentation errors** → Make sure the code inside `if` or `while` is indented the same amount (usually 4 spaces).
- **Infinite loop** → Ensure something inside your `while` changes the condition so it eventually becomes false.

## Next up
Do the matching lab: **[00 – Treasure Hunt (Basic)](../Labs/00-treasure-hunt-basic.md)**


