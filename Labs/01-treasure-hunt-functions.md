# 01 — Treasure Hunt (Functions)

> ### Quick Summary
> **Level:** 01 • **Time:** 35–60 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md), [Guide: 01 — Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Computer only  
> **You’ll practice:** defining/calling functions, parameters, return values, local vs global scope, docstrings

# Why This Matters
Functions let you **name** and **reuse** logic. Refactoring the basic Treasure Hunt into functions makes it easier to test, extend, and reason about—exactly what you’ll do in later labs.

---

# What You’ll Build
A function‑organized text‑adventure. You’ll separate I/O (printing/reading) from **decision logic** and use **return values** to drive the loop.

---

# Outcomes
By the end you can:
- Define **3–4 small functions** with clear, single purposes.
- Use **parameters** and **return values** to pass information.
- Keep `main()` short and readable.
- Avoid hidden global state—prefer passing values in and returning results out.

---

# Setup
- Use any Python 3 environment (local install or browser).  
- Start from a **new folder**: `Labs/01-treasure-hunt-functions/`.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open [STUDENT_START.md](Example_Code/01-treasure-hunt-functions/STUDENT_START.md) and reveal the Full Starter to compare with your approach.

## 1) Plan (2–3 min)
List your functions and their jobs. For example:  
- `welcome()` — prints the intro  
- `normalize(text, casefold=True)` — trims and optionally lowercases input  
- `get_direction(prompt="Which way? ")` — reads and normalizes input  
- `check_direction(direction)` — **returns** `"win"`, `"continue"`, or `"invalid"`  
- `main()` — loop that calls helpers until win/quit

> From the Guide: prefer **return values** over print for decisions.

## 2) Write Function Stubs (5 min)
Create empty functions with docstrings and `pass`. Fill them in later.
```python
def welcome():
    """Print game intro."""
    pass

def normalize(text, casefold=True):
    """Return text trimmed; case‑folded if requested."""
    pass

def get_direction(prompt="Which way? "):
    """Read input and return a normalized direction."""
    pass

def check_direction(direction):
    """Return one of: 'win', 'continue', 'invalid'."""
    pass

def main():
    """Run the game loop until win or quit."""
    pass
```

## 3) Normalize Input (5 min)
Implement `normalize(text, casefold=True)` using the Guide’s **string methods**.
- Trim spaces with `.strip()`  
- If `casefold` is `True`, return `text.casefold()` (more robust than `lower()`).

## 4) Decide What Happens (10–12 min)
Use `if/elif/else` **inside** `check_direction()` and **return** a value that the loop can use. **Do not copy code—write your own** using the checklist.

**Checklist**
- Compare the cleaned direction to your `WIN` value.
- On win: **return** `"win"` (don’t print everything here; keep prints short).
- On other valid directions: print a short message and **return** `"continue"`.
- Otherwise: **return** `"invalid"`.

**Pseudocode (guide, not code)**
```
if direction matches WIN:
    maybe print; return "win"
elif direction is valid but not WIN:
    print hint; return "continue"
else:
    return "invalid"
```

## 5) Main Loop & Quit Flow (6–8 min)
In `main()`:
- Print a short intro with `welcome()`.
- Loop: read input with `get_direction()`.
- If the user types `"quit"`, print goodbye and break.
- Otherwise call `check_direction()` and handle the **returned** result.

## 6) Celebrate & Report (1–2 min)
Track attempts in `main()` and report with an f‑string when they win.

---

# Skeleton Starter (start here)
Use this starter and the **Functions** guide to fill each TODO.  
If you get stuck for 5–7 minutes, open the **Student Start** helper: `Example_Code/01-treasure-hunt-functions/STUDENT_START.md`.

```python
WIN = "???"   # TODO: pick one: "north", "south", "east", or "west"

def welcome():
    """Print game intro."""
    print("Welcome to the Treasure Hunt (Functions)!")
    print("Type a direction (north/south/east/west) or 'quit' to exit.")

def normalize(text, casefold=True):
    """Return text trimmed; case‑folded if requested."""
    # TODO: implement using .strip() and optionally .casefold()
    return text  # placeholder

def get_direction(prompt="Which way? "):
    """Read input and return a normalized direction."""
    # TODO: read input(), then normalize and return it
    return ""  # placeholder

def check_direction(direction):
    """Return one of: 'win', 'continue', 'invalid'."""
    # TODO: compare to WIN, decide, and return a status string
    # Keep prints short; let main() decide what to do.
    return "invalid"  # placeholder

def main():
    """Run the game loop until win or quit."""
    # TODO:
    # - call welcome()
    # - track tries
    # - read direction with get_direction()
    # - support 'quit'
    # - call check_direction() and handle its return value
    pass

if __name__ == "__main__":
    main()

# Quick self-checks:
# 1) Typing "  EAST  " should still win after normalization (if WIN is "east").
# 2) main() stays short: helpers do the work; logic flows via return values.
# 3) 'tries' increments only when a valid attempt is made.
```

---

# Submission / Demo Checklist
- [ ] Uses **three+ functions** with clear names and single purposes.  
- [ ] `check_direction()` **returns** a value that drives the loop (no hidden globals).  
- [ ] Program handles **invalid** input and supports **quit**.  
- [ ] Code is organized (docstrings/comments where helpful).

---

# Extensions (choose one)
- **Stateful map:** Track a 2×2 grid and the player’s position; win at specific coordinates.  
- **Lives/score:** Subtract lives for bad choices; track and print best score.  
- **Hints:** Add `get_hint()` that returns a clue based on the last direction.

---

# Troubleshooting
- **Function returns `None`** → Ensure you `return` a value instead of only `print`ing.  
- **Global state bugs** → Pass values into functions and **return** results rather than mutating globals.  
- **Unclear flow** → Keep `main()` short—delegate logic to helpers.  
- **TypeError: missing required positional argument** → You defined a parameter but didn’t pass an argument when calling.

---

# Reflection (1–2 sentences)
- Which function helped the most with readability?  
- What would you add next if you had one more hour?

---

# Next Up
Advance to hardware with **[02 — Sense HAT Basics](../Labs/02-sense-hat-basics.md)** when you’re ready.
