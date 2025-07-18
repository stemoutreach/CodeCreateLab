# Lab 0 – Treasure Hunt (Basic) - Solution

print("Welcome to the Treasure Hunt!")

found_treasure = False

while not found_treasure:
    direction = input("Choose a direction (north, south, east, west): ").lower()
    if direction == "north":
        print("You hit a wall. Try again.")
    elif direction == "south":
        print("You fell in a pit. Try again.")
    elif direction == "west":
        print("It's a dead end. Try again.")
    elif direction == "east":
        print("Congratulations! You found the treasure!")
        found_treasure = True
    else:
        print("That's not a valid direction.")
