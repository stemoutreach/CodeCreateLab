# 1 Treasure Hunt Lab (With Functions) - Solution

def welcome():
    print("Welcome to the improved Treasure Hunt!")

def get_direction():
    return input("Choose a direction (north, south, east, west): ").lower()

def check_direction(direction):
    if direction == "north":
        print("You hit a wall. Try again.")
        return False
    elif direction == "south":
        print("You fell in a pit. Try again.")
        return False
    elif direction == "west":
        print("It's a dead end. Try again.")
        return False
    elif direction == "east":
        print("Congratulations! You found the treasure!")
        return True
    else:
        print("That's not a valid direction.")
        return False

# Main game loop
welcome()
found = False
while not found:
    direction = get_direction()
    found = check_direction(direction)
