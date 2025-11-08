# Python Functions

> ### Quick Summary
> **Level:** 01 • **Time:** 35–60 min    
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md)    
> **Hardware:** Computer only     
> **You’ll practice:** 
> - Define and call functions with and without parameters
> - Return values from functions and capture results
> - Use default parameters and keyword arguments
> - Understand variable scope (local vs. global)
> - Write simple, reusable utilities with docstrings

# Why This Matters 
Functions let you name a chunk of code and reuse it. They make programs shorter, clearer, and easier to test—skills you’ll need in the matching lab, **Treasure Hunt (Functions)**, where you’ll organize logic into well‑named functions.

---

## What you’ll learn
- Defining a function with `def`
- Parameters vs. arguments
- Returning values with `return`
- Default parameters & keyword arguments
- Local vs. global scope
- Basic docstrings for readability

## Setup
- **Raspberry Pi 500** running Raspberry Pi OS
- Open **Thonny** (Menu → Programming → Thonny)
- Create `functions_playground.py` in `~/Documents/CodeCreate/`
- Press **Run ▶** and view results in the **Shell**

---
## Essentials for this step (keep it light)

### Return vs. print
Functions should **return data**; your main code usually **prints**.
```python
def add(a, b):
    return a + b

total = add(3, 4)     # use the result
print(total)
```

### Parameters & arguments (positional and keyword)
```python
def area(width, height):
    return width * height

area(3, 4)                 # positional
area(width=3, height=4)    # keyword
```

### Default parameters
```python
def greet(name, punctuation="!"):
    return f"Hi, {name}{punctuation}"

print(greet("Ava"))
print(greet("Ava", punctuation="!!!"))
```

### Names, purpose, and tiny docstring
- Use **verb** names: `compute_`, `get_`, `is_`.
- Each function does **one job**.
```python
def is_even(n):
    """Return True if n is even, else False."""
    return n % 2 == 0
```

> Optional (older/faster students):  
> - **Pure vs side-effect:** pure returns a value; side-effect prints/does I/O.  
> - **Scope (light):** variables inside a function aren’t visible outside.

---
## Try (tiny practice, pick one)

1) **Return vs print:** change a function that prints a sum to one that **returns** a sum; print it in `main`.
2) **Defaults:** call `greet("Ava")` and `greet("Ava", punctuation="!!")`.
3) **Predicate:** write `is_even(n)` and print even numbers 1–10 using it.

---
## Bridge to the Lab (01 — Treasure Hunt / Functions)

Split the game into small functions:

- `show_menu(options)` → prints choices *(side-effect)*  
- `get_direction()` → reads input and **returns** cleaned text  
- `is_win(direction, target)` → **returns bool**  
- `respond(direction, target)` → prints hint/win message *(side-effect)*

### Checklist for this step
- [ ] At least one function with **parameters** and a **return**  
- [ ] One function with a **default parameter**  
- [ ] A **predicate** `is_*` that returns `True/False`  
- [ ] A 1‑line **docstring** in at least one function  
- [ ] Main script prints; functions mostly **return**

### Common pitfalls
- Printing inside every function → then nothing to combine. Prefer **return**.  
- Forgetting to **use** return values (`result = f(...)`).  
- Over-long functions → split into smaller pieces.

---

## Walkthrough — Step by Step (with explanations)

### 1) Define and call a function
**Idea:** A function is a named block of code you can run (call) whenever you need it.

**Anatomy of a function definition**
- `def` — tells Python you’re defining a function
- `say_hello` — the function’s *name* (use letters, numbers, and `_`, do not start with a number)
- `()` — parentheses (will hold inputs later; empty means “no inputs”)
- `:` — starts the function body
- **indented block** — the code that runs when the function is called

```python
def say_hello():
    print("Hello!")

say_hello()  # call
```

**Why indentation matters:** Everything indented under `def ...:` belongs *inside* the function. Use 4 spaces.

**Common mistakes**
- Forgetting the parentheses when calling: write `say_hello()` not `say_hello`.
- Missing the colon `:` after the parentheses in the definition.

**Try this variant**
```python
def cheer():
    print("Go team!")
    print("You’ve got this!")

cheer()
```

---

### 2) Add parameters (inputs)
**Idea:** Parameters are placeholders inside the function definition. Arguments are the actual values you pass when you call the function.

```python
def greet(name):
    print("Hello,", name)

greet("Alex")          # positional argument
greet(name="Ava")      # keyword argument
```

**How it works**
- **Parameter**: `name` in the definition `def greet(name):`
- **Argument**: `"Alex"` when calling `greet("Alex")`

**Positional vs. keyword**
- *Positional* uses order: `greet("Alex")`
- *Keyword* names the slot: `greet(name="Ava")` (order can change when you name them)

**Multiple parameters**
```python
def introduce(name, grade):
    print(f"This is {name}, in grade {grade}.")

introduce("Zoe", 7)
introduce(grade=11, name="Carter")  # keyword order can flip
```

**Pitfall:** If your function has required parameters, you must pass all of them when calling, or you’ll get a `TypeError`.

---

### 3) Return a value
**Idea:** `return` hands a result back to the caller. Printing shows a message on‑screen, but does **not** give a value back.

```python
def add(x, y):
    return x + y

result = add(2, 3)
print(result)  # 5
```

**Print vs. return**
- `print()` → displays text for a human
- `return` → gives data back to the program so it can be saved, used, or tested

**Only one path continues after `return`**
```python
def max_of_two(a, b):
    if a >= b:
        return a
    return b  # this line only runs if the first return didn't happen
```

**Multiple values?** You can return a tuple.
```python
def min_and_max(a, b, c):
    return min(a, b, c), max(a, b, c)

low, high = min_and_max(10, 3, 7)  # low=3, high=10
```

**No `return`?** Then the function returns `None` (Python’s “nothing” value).

---

### 4) Default parameters
**Idea:** Give a parameter a default so callers can skip it.

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))      # 25 (uses default exponent=2)
print(power(2, 10))  # 1024
```

**Rules of thumb**
- Put parameters with defaults **after** required ones: `def f(a, b=10): ...`
- You can always override a default: `power(3, exponent=3)`

**Important pitfall: avoid mutable defaults**
```python
# ❌ Don't do this
def append_once(item, bucket=[]):
    bucket.append(item)
    return bucket

# ✅ Do this instead
def append_once(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

---

### 5) Scope: local vs. global
**Idea:** Variables created *inside* a function are **local** (only exist there). Variables created *outside* are **global** (the whole file can read them).

```python
bonus = 10  # global variable

def score_with_bonus(score):
    # 'score' is local to this function
    return score + bonus  # reading a global is OK

print(score_with_bonus(90))  # 100
```

**Modifying a global?** It’s possible but discouraged in beginner code.

```python
counter = 0

def bad_increment():
    # ❌ This will error without 'global' because Python thinks 'counter' is local
    # counter = counter + 1  # UnboundLocalError

def better_increment():
    global counter   # tells Python to use the global 'counter'
    counter = counter + 1

better_increment()
```

**Best practice:** Prefer passing values **in** and returning results **out**. Globals make code harder to test.

**Tip:** Treat constants as globals you don’t change, and name them in ALL_CAPS:
```python
MAX_LIVES = 3
```

---

### 6) Document with a docstring
**Idea:** A docstring is a short description at the top of a function that explains what it does, its parameters, and what it returns.

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

print(distance(10, 6))      # 4
print(distance.__doc__)     # view the docstring text
# Or in a REPL: help(distance)
```

**Make it clear and short**
- First line: one‑sentence summary (“Return …” / “Compute …”)
- Optional lines: parameters and return value

---

## Vocabulary
- **Function**: a named, reusable block of code
- **Parameter**: a variable name in the function definition (placeholder)
- **Argument**: the actual value you pass when calling the function
- **Return value**: the data a function gives back using `return`
- **Scope**: where a variable can be used (local vs. global)
- **Docstring**: text inside triple quotes that documents a function

---

## Check your understanding
1. What’s the difference between a **parameter** and an **argument**?
2. What happens if a function has no `return` statement—what value is returned?
3. Why are default parameters useful? Give an example.
4. Where is a local variable accessible?
5. Fix this: `def area(width=10, height): return width * height` (what’s wrong with the parameter order?)

---

## Try it: Mini‑exercise
Build a tiny quiz game using functions:
- `ask(question, answer)` → returns `True` if the user’s input matches.
- `play_round()` → asks 2–3 questions and returns the score.
- In `main()`, call `play_round()` in a loop until the user types `quit`.

> **Stretch ideas**
> - Add `normalize(s, casefold=True)` that trims spaces and optionally ignores case.  
> - Track high score.  
> - Use a constant `MAX_TRIES = 2` and let players retry missed questions.

---

## Troubleshooting
- **TypeError: missing required positional argument** → You defined a parameter but didn’t pass an argument when calling.
- **Function returns `None`** → You printed inside the function but forgot to `return` the value.
- **Unexpected value changes** → Avoid mutating shared/global state; pass values as parameters and return results.
- **UnboundLocalError** → You tried to assign to a variable inside a function that also exists globally, without using `global`.

---

## Next up
Do the matching lab: **[01 – Treasure Hunt (Functions)](../Labs/01-treasure-hunt-functions.md)**
