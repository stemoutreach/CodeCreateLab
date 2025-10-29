
"""
Treasure Hunt (Functions) — Starter
-----------------------------------
Refactor the basic game using functions. This version runs,
but your job is to extend it (stateful map, hints, lives, etc.).
"""

from typing import Literal, Optional

Direction = Literal["north", "south", "east", "west"]
Result = Literal["win", "continue", "invalid", "quit"]

# --- Game Config ---
TREASURE_DIRECTION: Direction = "east"
ALLOW_QUIT = True

def welcome() -> None:
    print("Welcome to the Treasure Hunt (Functions)!"),
    print("Type a direction (north/south/east/west)" + (" or 'quit'" if ALLOW_QUIT else "") + " to exit.")

def normalize(text: str, casefold: bool = True) -> str:
    text = text.strip()
    return text.casefold() if casefold else text

def get_direction(prompt: str = "Which way? ") -> str:
    return normalize(input(prompt))

def check_direction(direction: str) -> Result:
    """Return: 'win' | 'continue' | 'invalid' | 'quit'"""
    if ALLOW_QUIT and direction == "quit":
        return "quit"
    if direction == TREASURE_DIRECTION:
        print("🎉 You found the treasure!")
        return "win"
    elif direction in {"north", "south", "west", "east"}:
        outcomes = {
            "north": "You hit a wall.",
            "south": "You stepped in a puddle.",
            "west": "It's a dead end.",
            "east": "(east is special in this version)",
        }
        if direction != TREASURE_DIRECTION:
            print(outcomes[direction], "Try again.")
            return "continue"
        # (if equal, we would have returned 'win' already)
    return "invalid"

def main() -> None:
    welcome()
    tries = 0
    while True:
        d = get_direction()
        result = check_direction(d)
        if result == "quit":
            print("Goodbye!")
            break
        tries += 1
        if result == "win":
            print(f"You won in {tries} tries!")
            break
        elif result == "invalid":
            print("Please type north/south/east/west" + (" or 'quit'" if ALLOW_QUIT else "") + ".")


if __name__ == "__main__":
    main()

# --- TODO ideas ---
# 1) Add a 'map' with coordinates (x,y) and only win at a specific cell.
# 2) Add a 'lives' system or a score.
# 3) Extract a 'give_hint()' function after N failed tries.
# 4) Split code into a module + runner for extra credit.
