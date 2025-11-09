# 01 — Treasure Hunt (Functions) — STUDENT_START

> Use this starter to refactor your basic Treasure Hunt into **small helpers**.
> Keep I/O (printing/input) separate from **decision logic**. Functions should
> return values; `main()` decides what to print.

## Your Tasks
1. Fill in the TODOs in each helper below.
2. Keep `main()` short — let helpers do the work.
3. Test helpers in the Thonny Shell (e.g., `check_direction("  e ", win="east")`).

## Copy/Paste Starter

```python
# 01 — Treasure Hunt (Functions) — Starter

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
```

## Mini Self‑Check
- [ ] `check_direction()` **returns** a status string (no prints).  
- [ ] Shortcuts (`n/s/e/w`) work after expansion.  
- [ ] `main()` stays short and readable.  
- [ ] No `global` needed; pass and return values instead.
