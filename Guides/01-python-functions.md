# 01 — Python Functions

> ### Quick Summary
> **Level:** 01 • **Time:** 45–60 min  
> **Prereqs:** [00 — Python Basics](./00-python-basics.md)  
> **Hardware:** None  
> **You’ll practice:** defining functions, parameters/arguments, return values, scope, docstrings, basic testing

# Why This Matters
Functions turn messy scripts into reusable, testable building blocks. You’ll use them in every lab—from treasure-hunt puzzles to robot driving helpers.

---
## What you’ll learn
- Define functions with `def` and call them
- Pass information with parameters; receive results with `return`
- Explain `print` vs `return` (side-effect vs value)
- Use docstrings to document behavior and examples
- Avoid common pitfalls (argument order, missing returns, mutable defaults)
- Write tiny tests to check correctness

## Setup
Any Python 3 environment. Save examples in `functions_play.py` so you can re-run quickly.

## Materials  (ONLY include if hardware is involved)
- *(None for this guide)*

---
## Walkthrough — Step by Step (with explanations)

### 1) Define and call
**Idea:** Create a named operation.
```python
def greet(name):
    return f"Hello, {name}!"
print(greet("Ava"))
```
**Anatomy:**
- `def name(params):` defines a function.
- `return` sends a value back to the caller.

### 2) Parameters vs arguments
**Idea:** Functions accept data; calls provide it.
```python
def repeat(text, times):
    return text * times

print(repeat("ha", 3))  # "hahaha"
```
**Notes & pitfalls:**
- Match the argument order to parameter order.
- Prefer explicit keyword arguments when helpful: `repeat(text="ha", times=3)`.

### 3) print vs return
**Idea:** `print()` shows info; `return` **produces** a value for later.
```python
def add(a, b):
    print("Adding...")   # side effect
    return a + b         # result
total = add(2, 3)
```

**Notes & pitfalls:**
- If you forget `return`, the function returns `None`.

### 4) Docstrings and examples
**Idea:** Document what your function expects and returns.
```python
def area_rect(w, h):
    """Return rectangle area.
    Examples:
    >>> area_rect(3, 4)
    12
    """
    return w * h
```
**Notes & pitfalls:**
- Keep docstrings short; include a simple example.

### 5) Common mistakes
**Idea:** Avoid subtle bugs.
```python
# Bad: mutable default shared across calls
def add_item(item, bag=[]):
    bag.append(item)
    return bag
```
**Notes & pitfalls:**
- Use `None` as a default and create a new list inside when needed.

---
## Vocabulary
- **Function**: A reusable block of code with a name.
- **Parameter / Argument**: Variable in the function definition / value passed in.
- **Return value**: The result produced by a function.
- **Docstring**: Triple-quoted string documenting a function.
- **Side effect**: Output or state change that isn’t the return value.
- **Scope**: Where a variable is visible/usable.

---
## Check your understanding
1) Why is `return` usually better than `print` inside a function?  
2) What happens if a function hits the end without `return`?  
3) How can keyword arguments help readability?  
4) Why are mutable default parameters dangerous?  
5) Where do parameters live: inside or outside the function’s scope?

---
## Try it: Mini-exercises
Write `hint(direction)` that returns a string like `"Try going north"` and `move(position, direction)` that returns a new position tuple.  
**Stretch goals:**
- Add `clamp(value, lo, hi)` that keeps a number within bounds.
- Write a tiny “doctest-style” comment example for one function.

---
## Troubleshooting
- **`TypeError: missing required positional argument`** → You didn’t pass enough arguments.  
- **`UnboundLocalError`** → You assigned to a variable inside a function that also needs a global—pass it in or return a new value.  
- **Function returns `None`** → You forgot `return`.

---
## Next up
**[01 – Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**
