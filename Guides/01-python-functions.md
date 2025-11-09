# 01 — Python Functions

> ### Quick Summary  
> **Level:** 01 • **Time:** 35–60 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> **Hardware:** Raspberry Pi 500 (Raspberry Pi OS)  
> **You’ll practice:** define/call functions, parameters & arguments, return values, defaults & keywords, scope (local vs global), docstrings, small utilities

# Why This Matters
Functions let you name a chunk of code and reuse it. They make programs shorter, clearer, and easier to test—skills you’ll use right away in the **Treasure Hunt (Functions)** lab when you organize logic into well‑named helpers.

## Table of contents
- [What you’ll learn](#what-youll-learn)  
- [Setup](#setup)  
- [1) What is a function? (define & call)](#1-what-is-a-function-define-call)  
- [2) Parameters & arguments](#2-parameters-arguments)  
- [3) Return values vs `print`](#3-return-values-vs-print)  
- [4) Default parameters & keyword args](#4-default-parameters-keyword-args)  
- [5) Scope: local vs global](#5-scope-local-vs-global)  
- [6) Docstrings (explain your function)](#6-docstrings-explain-your-function)  
- [7) Predicate helpers (`is_*`) & tiny utilities](#7-predicate-helpers-is_-tiny-utilities)  
- [Vocabulary](#vocabulary)  
- [Check your understanding](#check-your-understanding)  
- [Troubleshooting](#troubleshooting-troubleshooting)  
- [Next up](#next-up)
---

## What you’ll learn
- Define a function with `def` and call it
- Use **parameters** (in the definition) and **arguments** (in the call)
- Return values with `return` and capture results in variables
- Use **default parameters** and **keyword arguments**
- Understand **scope** (local vs global) and good habits
- Write short, clear **docstrings** and name functions well

## Setup
- On a **Raspberry Pi 500**, open **Thonny** (Menu → Programming → Thonny).  
- Create `functions_playground.py` in `~/Documents/CodeCreate/`.  
- Click **Run ▶**. Results appear in the **Shell** (bottom pane).

---

## 1) What is a function? (define & call)
**Learn**: A function is a named block of code. You define it once and call it whenever you need it.

**Pattern**
```python
def say_hello():       # definition
    print("Hello!")

say_hello()            # call
```

**Common mistakes**
- Missing `()` when calling → `say_hello` (no call) vs `say_hello()` (calls it)
- Missing `:` after the `def` line
- Wrong indentation (use **4 spaces**, not tabs)



### End-of-guide helpers (updated)

### Vocabulary
- **function** — named, reusable block of code
- **parameter** — variable name in a function definition (placeholder)
- **argument** — actual value you pass when calling
- **return value** — data given back with `return`
- **scope** — where a variable can be used (local vs global)
- **docstring** — triple‑quoted text that documents a function
- **predicate** — `is_*` style helper that returns `True`/`False`

### Check your understanding- What is the difference between **defining** a function and **calling** it?
- Fix: `def hello() print("Hi")`

---

## 2) Parameters & arguments
**Learn**: **Parameters** are placeholders in the function definition. **Arguments** are the real values you pass in the call.

```python
def greet(name):              # parameter
    print("Hello,", name)

greet("Alex")                 # positional argument
greet(name="Ava")             # keyword argument
```

Multiple parameters:
```python
def introduce(name, grade):
    print(f"This is {name}, in grade {grade}.")
```



### Vocabulary
- **parameter**: placeholder name in the definition
- **argument**: actual value passed in a call
- **positional argument**: matched by position
- **keyword argument**: `name=value` in a call

### Mini practice
- Call `introduce("Zoe", 7)` and then `introduce(grade=11, name="Carter")`.

### Check your understanding
- Parameter vs argument—say it in your own words.
- In `def f(a, b=10): ...`, which parameter has a default?

---

## 3) Return values vs `print`
**Learn**: `print()` shows a message for humans. `return` hands data back to your program so you can store or reuse it.

```python
def add(a, b):
    return a + b

total = add(3, 4)     # capture the result
print(total)          # 7
```

One path after `return`:
```python
def max_of_two(a, b):
    if a >= b:
        return a
    return b
```



### Vocabulary
- **return value**: the data a function hands back
- **side effect**: something like `print()` that shows output
- **`None`**: value returned if there’s no `return`

### Mini practice
- Change a function that *prints* a sum into one that **returns** it; then print the result in `main`.

### Check your understanding
- What does a function return if there is no `return` statement?
- Why is returning a value more useful than only printing it?

---

## 4) Default parameters & keyword args
**Learn**: Give parameters defaults so callers can skip them.

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))            # 25 (uses default)
print(power(2, 10))        # 1024
print(power(base=3, exponent=3))
```

**Rules of thumb**
- Put defaults **after** required params: `def f(a, b=10): ...`
- You can always override defaults with keywords

**Important pitfall — avoid mutable defaults**
```python
# ❌ Don't
def append_once(item, bucket=[]):
    bucket.append(item)
    return bucket

# ✅ Do
def append_once(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```



### Vocabulary
- **default parameter**: value used when caller omits it
- **keyword argument**: `name=value` to be explicit
- **mutable default**: a changeable object like `[]`—avoid as a default

### Mini practice
- Make `greet(name, punctuation="!")` and test `greet("Ava")` and `greet("Ava", punctuation="!!")`.

### Check your understanding
- Why are default parameters helpful in beginner programs?
- Explain the bug that happens with a mutable default like `[]`.

---

## 5) Scope: local vs global
**Learn**: Variables created **inside** a function are **local**. Outside ones are **global**. Prefer passing values in and returning results out.

```python
BONUS = 10       # constant global

def score_with_bonus(score):
    return score + BONUS

print(score_with_bonus(90))   # 100
```

Modifying a global is possible but discouraged in beginner code:
```python
counter = 0

def better_increment():
    global counter
    counter = counter + 1
```



### Vocabulary
- **local variable**: defined inside a function; used there
- **global variable**: defined at module top; used anywhere
- **constant**: a global that you don’t change (UPPER_SNAKE_CASE)

### Mini practice
- Write `add_bonus(score, bonus=5)` that **returns** the new score (don’t use `global`).

### Check your understanding
- Why does avoiding `global` make testing easier?
- What’s the difference between a constant global and a changing global?

---

## 6) Docstrings (explain your function)
**Learn**: A **docstring** (triple quotes) says what the function does, its inputs, and what it returns.

```python
def distance(a, b):
    """Return the distance between numbers a and b.

    Parameters:
        a (int | float): first number
        b (int | float): second number
    Returns:
        int | float: the absolute difference |a - b|
    """
    return abs(a - b)
```



### Vocabulary
- **docstring**: triple‑quoted string that documents a function
- **signature**: the function’s name and parameter list

### Mini practice
- Add a 1‑line docstring to one of your functions and print it with `your_func.__doc__`.

### Check your understanding
- What goes into a helpful beginner docstring?
- How do you read a function’s docstring at runtime?

---

## 7) Predicate helpers (`is_*`) & tiny utilities
**Learn**: A **predicate** returns `True`/`False`. Great for clean `if` checks.

```python
def is_even(n):
    """Return True if n is even."""
    return n % 2 == 0
```



### Vocabulary
- **predicate**: function that returns `True`/`False`
- **boolean**: a `True` or `False` value

### Mini practice
- Print the even numbers from 1–10 using `is_even`.

### Check your understanding
- Why do small helpers like `is_even` make other code clearer?
- What will `is_even(13)` return? Why?

---

## Vocabulary
- **function** — named, reusable block of code  
- **parameter** — variable name in a function definition (placeholder)  
- **argument** — actual value you pass when calling  
- **return value** — data a function gives back with `return`  
- **scope** — where a variable can be used (local vs global)  
- **docstring** — triple‑quoted text that documents a function

---

## Check your understanding
1) Parameter vs argument—what’s the difference?  
2) What value is returned if a function has no `return`?  
3) Fix the parameter order: `def area(width=10, height): ...`  
4) Why are default parameters useful? Give an example.  
5) Why avoid mutable default values?  
6) How do docstrings help you (and your teammates)?

---

### Mini practice (choose 2–3)
- Write `square(n)` and `cube(n)` that **return** results; print a small table for 1–5.
- Create `safe_divide(a, b)` that returns `None` if `b == 0`, else `a / b`; test it.
- Build `format_name(first, last, *, upper=False)` that returns a full name; if `upper` is `True`, uppercase it.

## Troubleshooting
- **Missing argument / `TypeError`** → You defined a parameter but didn’t pass an argument.  
- **Function returns `None`** → You printed inside the function but forgot to `return`.  
- **`UnboundLocalError`** → You assigned to a name inside the function that also exists globally (without `global`).  
- **Unexpected value changes** → Don’t mutate shared globals; pass in values and return results.  
- **Nothing happens** → Did you call the function with `()`?

---

## Next up
Do the lab: **[01 — Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**.
