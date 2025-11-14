# 01 — Treasure Hunt (Functions)

> ### Quick Summary
> **Level:** 01 • **Time:** 35–60 min  
> **Prereqs:** [Guide: 00 — Python Basics](../Guides/00-python-basics.md), [Guide: 01 — Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi 500 + Thonny (Python 3)  
> **You’ll practice:** defining/calling functions, parameters & return values, **pure helpers vs I/O**, short `main()`, simple predicates

> **Learn → Try → Do**  
> - **Learn** + **Try** in the Functions guide.  
> - **Do** here in the Lab by refactoring the Basic Treasure Hunt into clean helpers.

---

# Why This Matters
Functions let you name a chunk of logic and reuse it. Refactoring your basic Treasure Hunt into **small helpers that return values** makes the game easier to read, test, and extend (like adding hints or a mini‑map).

---

# What You’ll Build
A function‑organized **text adventure** where:
- Input/printing (I/O) is kept in tiny wrappers  
- Game **decisions** happen inside helpers that **return** status strings  
- `main()` becomes short and readable

---

# Outcomes
By the end you can:
- Write **3–5 small functions** with single, clear jobs.  
- Pass information with **parameters** and **return values** (not globals).  
- Keep **I/O separate** from decision logic.  
- Explain why a short `main()` is easier to maintain.

---

# Setup
- Open **Thonny** on your **Raspberry Pi 500** (Menu → Programming → Thonny).  
- Create a new file `treasure_functions.py` in `~/Documents/CodeCreate/`.  
- Press **Run ▶** to execute; watch the **Shell** for I/O.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/01-treasure-hunt-functions/STUDENT_START.md)** and reveal the Full Starter to compare with your approach.

## 1) Plan your helpers (2–3 min)
List small functions and their job (one job each):
- `normalize(text, *, casefold=True)` → return trimmed (and optionally case‑folded) text  
- `is_valid_direction(choice)` → `True/False` for allowed words/shortcuts  
- `expand_shortcut(choice)` → `'n' → 'north'`, etc.  
- `check_direction(choice, *, win)` → return `"win"`, `"continue"`, or `"invalid"`  
- `prompt_direction(prompt="Which way? ")` → read input and **return** normalized text  
- `main()` → drive the loop and print messages

> From the Guide: prefer **return values** from helpers; print in `main()`.

## 2) Create function stubs (3–4 min)
Write each function with a docstring and `pass` so the file runs. You’ll fill them soon.

## 3) Normalize & validate (6–8 min)
Implement `normalize`, `is_valid_direction`, and `expand_shortcut`. Use a constant list of valid words:
```python
VALID = ("north", "south", "east", "west")
```

## 4) Decide with returns (8–10 min)
Implement `check_direction(choice, *, win)` so it **returns** a status string (no long prints). Keep it pure if you can.

**Checklist**
- If not valid → return `"invalid"`  
- Map shortcuts to full words (e.g., `'e' → 'east'`)  
- Compare to `win` → return `"win"` or `"continue"`

## 5) Short, readable `main()` (6–8 min)
- Print a welcome once (separate tiny function optional).  
- Loop: show a simple menu (`for d in VALID: print("-", d)`), then call `prompt_direction`.  
- If `"quit"` → say goodbye and `break`.  
- Else call `check_direction` and handle the **returned** status.  
- Track `tries` and only increment for actual attempts.

## 6) Celebrate & report (1–2 min)
When status is `"win"`, congratulate the player with an f‑string including `tries` and end the loop.

---

# Skeleton Starter (copy/paste, then fill TODOs)
Use the Functions guide + your Basic lab as reference.

```python
# 01 — Treasure Hunt (Functions)

VALID = ("north", "south", "east", "west")
WIN = "???"  # TODO: pick one: "north", "south", "east", or "west"

def normalize(text, *, casefold=True):
    """Return trimmed text; case-folded if requested."""
    # TODO: use .strip() and optionally .casefold()
    return text  # placeholder

def is_valid_direction(choice):
    """True if choice is a valid word or shortcut (n/s/e/w)."""
    # TODO: check full words in VALID or shortcuts in ("n","s","e","w")
    return False  # placeholder

def expand_shortcut(choice):
    """Map n/s/e/w to full words; otherwise return choice unchanged."""
    # TODO: use a dict mapping
    return choice  # placeholder

def check_direction(choice, *, win):
    """Return 'win', 'continue', or 'invalid' without doing I/O."""
    # TODO:
    # 1) validate
    # 2) expand shortcut
    # 3) compare to win and return a status string
    return "invalid"  # placeholder

def prompt_direction(prompt="Which way? "):
    """Read, normalize, and return a direction or 'quit'."""
    # TODO: read input(), normalize, and return
    return ""  # placeholder

def main():
    """Run the game loop until win or quit."""
    print("Welcome to the Treasure Hunt (Functions)!")
    print("Type north/south/east/west (or n/s/e/w). Type 'quit' to leave.")
    tries = 0

    while True:
        # show menu each loop
        for d in VALID:
            print(f"- {d}")

        choice = prompt_direction("Which way? ")
        if choice == "quit":
            print("Thanks for playing. Goodbye!")
            break

        # count real attempts
        tries += 1
        result = check_direction(choice, win=WIN)

        if result == "win":
            print(f"You found the treasure in {tries} moves!")
            break
        elif result == "continue":
            print("Not here—keep exploring...")
        else:  # 'invalid'
            print("Try north, south, east, or west (n/s/e/w).")

if __name__ == "__main__":
    main()

# Quick self-checks:
# - check_direction("  E  ", win="east") should be 'win' after your normalize/expand.
# - main() remains short; helpers do the work.
# - You don't need 'global'—pass values and return results.
```

---

# Demo / Submission Checklist
- [ ] Uses **three or more functions** with single, clear jobs.  
- [ ] `check_direction()` **returns** a status string; `main()` makes the decisions.  
- [ ] Input is cleaned; shortcuts work; **quit** supported.  
- [ ] `main()` is short (helpers handle logic).  
- [ ] Docstrings or short comments clarify each helper.

---

# Make It Yours — Extensions (choose one)
- **MAX_TRIES:** Add a `MAX_TRIES` constant (e.g., 6). End with “Game over” if exceeded.  
- **Hints:** Write `get_hint(last_move, win)` that **returns** a clue string; print it after 3 misses.  
- **Map:** Track a 2×2 grid (`(x, y)`); only the winning cell succeeds. Show position each loop.  
- **Scoring:** Subtract points for bad moves; bonus for winning quickly.

> Tip: Keep helpers **pure** when you can (no print/input). Pure functions are easy to test in the Shell.

---

# Troubleshooting
- **Nothing happens** → Did you call `main()` at the bottom?  
- **Function returns `None`** → You printed but forgot to `return`.  
- **Missing argument** → Your call didn’t match the function’s parameters.  
- **Globals confusion** → Avoid `global`; pass in what you need and return results.  
- **Shortcuts fail** → Double‑check `expand_shortcut` and `is_valid_direction`.

---

# Reflection (1–2 sentences)
- Which helper made your code the most readable?  
- If you had one more hour, what feature would you add next and why?

---

# Next Up
Ready for sensors? Move on to **[02 — Sense HAT](../Labs/02-sense-hat.md)**.
