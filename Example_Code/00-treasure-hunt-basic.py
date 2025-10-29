
"""
Treasure Hunt (Basic) — Starter
--------------------------------
Goal: Build a tiny text adventure that loops until the player finds the treasure.

You can run this file as-is to see a working baseline.
Then, improve it to meet your lab rubric and extensions.
"""

# --- Game Settings (change these!)
TREASURE_DIRECTION = "east"   # <- pick: 'north' | 'south' | 'east' | 'west'
MAX_TRIES = None              # <- set to an int (e.g., 5) to limit attempts, or None for unlimited

# --- Helper (optional) ---
def normalize(text: str) -> str:
    """Trim spaces and make input case-insensitive."""
    return text.strip().lower()

# --- Game ---
print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing a direction: north, south, east, or west.")
if MAX_TRIES:
    print(f"(You have {MAX_TRIES} tries.)")

found = False
tries = 0

while not found:
    direction = normalize(input("Which way? "))

    # Validate
    if direction not in {"north", "south", "east", "west"}:
        print("I don't understand that direction. Try north/south/east/west.")
        continue

    tries += 1

    # Decide
    if direction == TREASURE_DIRECTION:
        print("🎉 You found the treasure!")
        found = True
    elif direction == "north":
        print("You hit a wall. Try again.")
    elif direction == "south":
        print("You fell into a puddle. Soggy socks… try again.")
    elif direction == "west":
        print("It's a dead end. Try another way.")

    # Optional: lives/tries
    if MAX_TRIES and not found:
        remaining = MAX_TRIES - tries
        if remaining <= 0:
            print("Out of tries! Game over.")
            break
        print(f"({remaining} tries left.)")

if found:
    print(f"You won in {tries} tries!")

# --- TODO ideas ---
# 1) Add an intro story or ASCII art.
# 2) Add a mini-map: start at (0,0); moving east to (1,0) is treasure.
# 3) Add hints after 3 wrong attempts.
# 4) Add 'quit' to exit early.
