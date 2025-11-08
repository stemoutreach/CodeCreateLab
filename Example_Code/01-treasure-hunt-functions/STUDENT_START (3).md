# STUDENT_START — 01 Treasure Hunt (Functions)

**Use this only if you're stuck for 5–7 minutes.**
This gives you function **stubs** and a tiny `main()` shape — no full solution.

---

## Goal
- Keep `main()` short; make helpers do the work.
- Normalize input.
- Drive the loop using **return values** (not globals).

---

## Starter Stubs
```python
WIN = "???"   # TODO: pick one: "north", "south", "east", or "west"

def welcome():
    """Print game intro."""
    print("Welcome to the Treasure Hunt (Functions)!")
    print("Type a direction (north/south/east/west) or 'quit' to exit.")

def normalize(text, casefold=True):
    """Return text trimmed; case-folded if requested."""
    # TODO: implement using .strip() and optionally .casefold()
    return text

def get_direction(prompt="Which way? "):
    """Read input and return a normalized direction."""
    # TODO: read input(), then normalize and return it
    return ""

def check_direction(direction):
    """Return one of: 'win', 'continue', 'invalid'."""
    # TODO: compare to WIN and return a status string
    # Keep prints short; let main() decide what to do.
    return "invalid"

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
```

### Self-check
- `normalize()` actually trims/case-folds.
- `check_direction()` **returns** a status string (not printing everything).
- You handle `'quit'` in `main()`.
