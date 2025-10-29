# Python Functions

> ### Quick info
> **Level:** 01 • **Time:** 35–60 min
> **Prereqs:** Guide: ../Guides/00-python-basics.md
> **Hardware:** Computer only
> **You’ll practice:**
> - Define and call functions with and without parameters
> - Return values from functions and capture results
> - Use default parameters and keyword arguments
> - Understand variable scope (local vs. global)
> - Write simple, reusable utilities with docstrings

# BLUF
Functions let you name a chunk of code and reuse it. They make programs shorter, clearer, and easier to test—skills you’ll need in the matching lab, **Treasure Hunt (Functions)**, where you’ll organize logic into well‑named functions.

## What you’ll learn
- Defining a function with `def`
- Parameters vs. arguments
- Returning values with `return`
- Default parameters & keyword arguments
- Local vs. global scope
- Basic docstrings for readability

## Setup
- Any Python 3 environment (installed locally or browser-based).
- Keep your **Python Basics** guide handy for print/input/if/while.

## Walkthrough

### 1) Define and call a function
```python
def say_hello():
    print("Hello!")

say_hello()  # call
```

### 2) Add parameters (inputs)
```python
def greet(name):
    print("Hello,", name)

greet("Alex")
greet(name="Ava")  # keyword argument
```

### 3) Return a value
```python
def add(x, y):
    return x + y

result = add(2, 3)
print(result)  # 5
```

### 4) Default parameters
```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))      # 25 (uses default exponent=2)
print(power(2, 10))  # 1024
```

### 5) Scope: local vs. global
```python
bonus = 10  # global variable

def score_with_bonus(score):
    # 'score' is local to this function
    return score + bonus

print(score_with_bonus(90))  # 100
```
> Rule of thumb: prefer passing values in as parameters over relying on globals.

### 6) Document with a docstring
```python
def distance(a, b):
    """Return the distance between numbers a and b."""
    return abs(a - b)

print(distance(10, 6))  # 4
```

## Check your understanding
1. What’s the difference between a **parameter** and an **argument**?
2. What happens if a function has no `return` statement—what value is returned?
3. Why are default parameters useful? Give an example.
4. Where is a local variable accessible?

## Try it: Mini‑exercise
Build a tiny quiz game using functions:
- `ask(question, answer)` → returns `True` if the user’s input matches.
- `play_round()` → asks 2–3 questions and returns the score.
- In `main()`, call `play_round()` in a loop until the user types `quit`.
> Stretch: add a `normalize(s, casefold=True)` helper that trims spaces and optionally ignores case.

## Troubleshooting
- **TypeError: missing required positional argument** → You defined a parameter but didn’t pass an argument when calling.
- **Function returns `None`** → You printed inside the function but forgot to `return` the value.
- **Unexpected value changes** → Avoid mutating shared/global state; pass values as parameters and return results.

## Next up
Do the matching lab: **[01 – Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**

## Attributions & License
- Adapted from the original “1 Python Functions Guide.”
- See repository LICENSE for terms.
