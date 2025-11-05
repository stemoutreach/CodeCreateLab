# 00 — Python Basics

> ### Quick Summary
> **Level:** 00 • **Time:** 45–60 min  
> **Prereqs:** None  
> **Hardware:** None  
> **You’ll practice:** print/input, variables & types, expressions, conditionals, while loops, debugging basics

# Why This Matters
Python is the language we’ll use across the Code & Create Lab—from text adventures to blinking LEDs and driving robots. Mastering the basics now makes every future guide (and lab) faster and more fun.

---
## What you’ll learn
- Print a message and read user input safely
- Store values in variables and convert types (`str`, `int`, `float`)
- Use arithmetic and comparison operators
- Make decisions with `if / elif / else`
- Repeat actions with `while` loops (and avoid infinite loops)
- Read and fix simple error messages

## Setup
Any Python 3 environment works (IDLE, VS Code, terminal). In locked-down school labs, you can also use a browser IDE (e.g., Python in Replit). Save files with a `.py` extension and run them with Python.

## Materials  (ONLY include if hardware is involved)
- *(None for this guide)*

---
## Walkthrough — Step by Step (with explanations)

### 1) Say hello
**Idea:** Learn `print()` and run a script.
```python
print("Hello, Code & Create!")
```
**Anatomy:**
- `print(...)` sends text to the console.
- Quotes create a string.
**Common mistakes:**
- Missing quotes or parentheses.

### 2) Read input and convert
**Idea:** Get a string from the keyboard; convert to a number.
```python
name = input("Your name: ")
age_text = input("How old are you? ")
age = int(age_text)  # convert text to number
print("Hi", name, "- next year you’ll be", age + 1)
```
**Notes & pitfalls:**
- `input()` returns **text**. Use `int()` or `float()` for math.
- If the user types non-numeric text, `int()` will error—catch later with validation.

### 3) Decisions with if
**Idea:** Choose different paths.
```python
score = int(input("Score (0–100): "))
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("Keep going!")
```
**Notes & pitfalls:**
- Use `>=` for ranges; check higher thresholds first.

### 4) Looping with while
**Idea:** Repeat until done.
```python
count = 3
while count > 0:
    print("Countdown:", count)
    count = count - 1
print("Liftoff!")
```
**Notes & pitfalls:**
- Update the loop variable inside the loop.
- To stop a runaway program: **Ctrl+C** in terminal.

### 5) Validate input (bonus)
**Idea:** Guard against bad input.
```python
text = input("Enter a whole number: ")
if text.isdigit():
    n = int(text)
    print("Squared:", n*n)
else:
    print("That was not a whole number.")
```

---
## Vocabulary
- **String**: Text value like `"hello"`.
- **Integer / Float**: Whole number / decimal number.
- **Variable**: A named box that stores a value.
- **Expression**: Code that produces a value.
- **Condition**: A true/false check in an `if` statement.
- **Loop**: Repeats code while a condition is true.

---
## Check your understanding
1) What does `input()` return and why is `int()` sometimes needed?  
2) Which operator checks “greater than or equal to”?  
3) How do you stop a script stuck in an infinite loop?  
4) Where should you update the loop variable in a `while`?  
5) What happens if you call `int("six")`?

---
## Try it: Mini-exercises
Build a small “Greeter+” program: ask for a name and favorite number, print a custom message, and show the number doubled.  
**Stretch goals:**
- Ask for a second number and print the larger one.
- Add input validation: keep asking until the user types a valid number.

---
## Troubleshooting
- **`SyntaxError: EOL while scanning string literal`** → You forgot a closing quote.  
- **`NameError: name 'age' is not defined`** → Spelling mismatch or using a variable before assigning.  
- **Program never stops** → Your `while` condition never becomes false; update the variable or add a break.

---
## Next up
**[01 – Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**
