# 01 — Python Functions

> ### Quick Summary  
> **Level:** 01 • **Time:** 35–60 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> **Hardware:** Raspberry Pi 500 (Raspberry Pi OS)  
> **You’ll practice:** define/call functions, parameters & arguments, return values, defaults & keywords, scope (local vs global), docstrings, small utilities

# Why This Matters
Functions let you name a chunk of code and reuse it. They make programs shorter, clearer, and easier to test—skills you’ll use right away in the **Treasure Hunt (Functions)** lab when you organize logic into well‑named helpers.

## Table of contents
- [1) What is a function? (define & call)](#1-what-is-a-function-define-call)  
- [2) Parameters & arguments](#2-parameters-arguments)  
- [3) Return values vs `print`](#3-return-values-vs-print)  
- [4) Default parameters & keyword args](#4-default-parameters-keyword-args)  
- [5) Scope: local vs global](#5-scope-local-vs-global)  
- [6) Docstrings (explain your function)](#6-docstrings-explain-your-function)  
- [7) Predicate helpers and tiny utilities](#7-predicate-helpers-and-tiny-utilities)
- [9) Run your program safely: the main-guard](#9-run-your-program-safely-the-main-guard)
- [Vocabulary](#vocabulary)  

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


### Vocabulary
- **function** — named, reusable block of code

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

## 7) Predicate helpers and tiny utilities
**Learn**: A **predicate** returns `True`/`False`. Use them to keep `if` checks clean.

```python
def is_even(n):
    """Return True if n is even."""
    return n % 2 == 0
```

#### More number predicates
```python
def is_odd(n):
    """True if n is odd."""
    return n % 2 == 1

def is_positive(x):
    """True if x > 0."""
    return x > 0

def is_between(x, low, high, inclusive=True):
    """True if low <= x <= high (or low < x < high if inclusive=False)."""
    return (low <= x <= high) if inclusive else (low < x < high)

def is_prime(n):
    """Simple prime test for n >= 2."""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

#### String predicates
```python
def is_vowel(ch):
    """True if ch is a vowel (A/E/I/O/U)."""
    return ch.lower() in "aeiou"

def is_consonant(ch):
    """True if ch is a letter and not a vowel."""
    return ch.isalpha() and not is_vowel(ch)

def starts_with_vowel(s):
    """True if s starts with a vowel."""
    return len(s) > 0 and is_vowel(s[0])

def is_blank(s):
    """True if s is empty or only spaces."""
    return s.strip() == ""

def is_palindrome(text):
    """True if text reads the same forward/backward (ignore spaces/punctuation/case)."""
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
```

#### Collection predicates (lists/tuples/strings)
```python
def all_unique(seq):
    """True if no duplicates."""
    return len(set(seq)) == len(seq)

def has_duplicates(seq):
    """True if any value appears more than once."""
    return len(set(seq)) != len(seq)

def is_sorted(seq, *, reverse=False):
    """True if seq is in nondecreasing order (or nonincreasing if reverse=True)."""
    return list(seq) == sorted(seq, reverse=reverse)
```

#### Tiny utilities (helpers you’ll reuse)
```python
def normalize(text, *, casefold=True, strip=True):
    """Return cleaned text for comparisons."""
    if strip:
        text = text.strip()
    return text.casefold() if casefold else text

def clamp(x, low, high):
    """Keep x within [low, high]."""
    return max(low, min(x, high))

def approximately_equal(a, b, tol=1e-6):
    """True if a and b are within tol."""
    return abs(a - b) <= tol
```


### Mini practice
- Print the even numbers from 1–10 using `is_even`.

### Check your understanding
- Why do tiny helpers like `is_even` make other code clearer?
- What will `is_even(13)` return? Why?
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



## 9) Run your program safely: the main-guard
> **Quick note — what’s this line?** When you run a file directly, `__name__` is `"__main__"`, so we call `main()`. When this file is imported from another file, the line **doesn’t** run—so your game won’t auto‑start. You’ll use this more in a later guide.


**Learn**: When Python runs a file directly (press **Run ▶** in Thonny), it sets a special variable `__name__` to `"__main__"`.  
When a file is **imported** (used as a module), `__name__` becomes the module’s name (like `"functions_playground"`).

Use the **main‑guard** to run demo code only when the file is executed directly—**not** when it’s imported from somewhere else:

```python
def main():
    print("This only runs when the file is executed directly.")

if __name__ == "__main__":
    main()
```

Why it matters for our Treasure Hunt:
- You can import your helper functions into other files without accidentally starting the game.
- Keeps files reusable and testable.

### Try
1) Create a file `demo_guard.py` with the main‑guard and a `print("hi")` inside `main()`. Run it.  
2) In a second file, `import demo_guard`. Notice that it **does not** print “hi”.  
3) Add a small helper (e.g., `normalize(text)`) to `demo_guard.py` and import/use it from the second file.

### Common mistakes
- Forgetting the `()` → writing `if __name__ == "__main__": main` (does nothing).  
- Putting **all code** under the guard—keep **functions above**, guard at **bottom**.

> In this guide’s examples and the lab skeleton, we include:
>
> ```python
> if __name__ == "__main__":
>     main()
> ```
>
> so your helpers can be imported and tested without auto‑running the game.

## Vocabulary
- **function** — named, reusable block of code  
- **parameter** — variable name in a function definition (placeholder)  
- **argument** — actual value you pass when calling  
- **return value** — data a function gives back with `return`  
- **scope** — where a variable can be used (local vs global)  
- **docstring** — triple‑quoted text that documents a function
- **predicate** — `is_*` style helper that returns `True`/`False`

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
