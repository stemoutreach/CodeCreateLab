"""
01 — Treasure Hunt (Functions) — SOLUTION (Coach reference)
-----------------------------------------------------------------
COACH NOTE:
- Keep helpers "pure" when possible (no I/O), so they're easy to test.
- `main()` owns the loop and prints based on helpers' return values.
- This solution also demonstrates optional MAX_TRIES and a simple hint helper.
"""

from typing import Literal

VALID: tuple[str, str, str, str] = ("north", "south", "east", "west")
WIN: Literal["north", "south", "east", "west"] = "east"

# Optional extension knobs
USE_HINTS = True
MAX_TRIES = 8  # set None to disable cap

def normalize(text: str, *, casefold: bool = True) -> str:
    """Return trimmed text; case-folded if requested.
    Pure helper: no printing.
    """
    text = text.strip()
    return text.casefold() if casefold else text

def is_valid_direction(choice: str) -> bool:
    """True if choice is a valid word or shortcut (n/s/e/w)."""
    return choice in VALID or choice in ("n", "s", "e", "w")

def expand_shortcut(choice: str) -> str:
    """Map n/s/e/w to full words; otherwise return choice unchanged."""
    mapping = {"n": "north", "s": "south", "e": "east", "w": "west"}
    return mapping.get(choice, choice)

def check_direction(choice: str, *, win: str) -> Literal["win", "continue", "invalid"]:
    """Return a status string for the current move.
    - 'invalid'   -> not a recognized direction
    - 'win'       -> matches the winning direction
    - 'continue'  -> valid but not winning
    Pure helper: no printing or input calls.
    """
    # Normalize first so users can type messy input like "  E  "
    normalized = normalize(choice, casefold=True)

    if normalized == "quit":
        # Caller handles quitting; we treat it separately in main()
        # (Return 'continue' so it won't be counted as a win/invalid)
        return "continue"

    if not is_valid_direction(normalized):
        return "invalid"

    full = expand_shortcut(normalized)
    return "win" if full == win else "continue"

# ----- Optional: simple hint logic ----------------------------------------

def get_hint(last_move: str, win: str) -> str:
    """Return a small textual hint given the last move and the winning direction.
    Example: If player guessed 'north' and win is 'east', suggest "Try more east-ish...".
    Pure helper: returns a string; main() decides when to print.
    """
    last_full = expand_shortcut(normalize(last_move))
    if last_full not in VALID:
        return "Focus on valid directions: north, south, east, or west."

    if last_full == win:
        return "You already found it!"

    # Super-simple directional nudge
    if (last_full, win) in {("north", "south"), ("south", "north")}:
        return "You're close—think the *other* vertical direction."
    if (last_full, win) in {("east", "west"), ("west", "east")}:
        return "You're close—think the *other* horizontal direction."
    return "Not quite—adjust your direction."

# ----- Thin I/O wrapper ----------------------------------------------------

def prompt_direction(prompt: str = "Which way? ") -> str:
    """Read, normalize, and return a direction or 'quit' (lowercased).
    I/O wrapper: isolates input() from the rest of the logic.
    """
    raw = input(prompt)
    return normalize(raw)

# ----- Short, readable main() ---------------------------------------------

def main() -> None:
    """Run the game loop until win, quit, or MAX_TRIES is exceeded."""
    print("Welcome to the Treasure Hunt (Functions)!")
    print("Type north/south/east/west (or n/s/e/w). Type 'quit' to leave.")
    tries = 0
    last_move = ""

    while True:
        # Show menu
        for d in VALID:
            print(f"- {d}")

        choice = prompt_direction("Which way? ")
        if choice == "quit":
            print("Thanks for playing. Goodbye!")
            break

        # Count only real attempts
        tries += 1
        status = check_direction(choice, win=WIN)

        if status == "win":
            print(f"You found the treasure in {tries} moves!")
            break
        elif status == "continue":
            print("Not here—keep exploring...")
        else:
            print("Try north, south, east, or west (n/s/e/w).")

        # Optional: hints after 3 misses
        if USE_HINTS and tries >= 3:
            print(get_hint(choice, WIN))

        # Optional: max tries cap
        if MAX_TRIES is not None and tries >= MAX_TRIES:
            print("Game over—out of moves. Better luck next time!")
            break

        last_move = choice

# Main-guard ensures safe import (no auto-run when used as a module)
if __name__ == "__main__":
    main()
