# 00-treasure-hunt-basic — Coaches Solution
# (Filename matches the lab slug for consistency)
#
# Concepts: print(), input(), variables (bool/int/str/list), list membership,
# boolean OR for shortcut letters, while loop, tiny for menu, f-strings.

print("Welcome to the Treasure Hunt!")
print("Find the treasure by typing north, south, east, or west.")

found = False
tries = 0
valid = ["north", "south", "east", "west"]
WIN = "east"  # choose one: "north", "south", "east", or "west"

while not found:
    for d in valid:
        print(f"- {d}")

    direction = input("Which way? ").strip().lower()
    tries += 1

    is_east  = (direction == "east")  or (direction == "e")
    is_west  = (direction == "west")  or (direction == "w")
    is_north = (direction == "north") or (direction == "n")
    is_south = (direction == "south") or (direction == "s")

    if (WIN == "east"  and is_east) or        (WIN == "west"  and is_west) or        (WIN == "north" and is_north) or        (WIN == "south" and is_south):
        print(f"You found the treasure in {tries} moves!")
        found = True
    elif direction in valid or direction in ["n", "s", "e", "w"]:
        print("Not here—keep exploring...")
    else:
        print("Try north, south, east, or west (n/s/e/w).")

print(f"You won in {tries} tries!")