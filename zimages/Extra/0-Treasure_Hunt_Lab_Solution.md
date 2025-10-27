# Solution: 0 Treasure Hunt Lab: Mini Treasure Hunt Game

Solution Code

```python

import random

def greet_player():
    print("🏴‍☠️  Welcome to the Mini Treasure Hunt!")
    name = input("What’s your explorer name? ")
    print(f"\nAhoy, {name}! Your quest is to find the hidden treasure chest.\n")
    return name

def choose_cave():
    while True:
        choice = input("Do you enter cave 1 or cave 2? (type 1 or 2) ")
        if choice in ("1", "2"):
            return int(choice)
        print("Please choose 1 or 2! 🧐")

def reveal_outcome(chosen_cave, treasure_cave):
    if chosen_cave == treasure_cave:
        print("✨  You found the treasure! Congratulations! 🎉")
        return True
    else:
        print("💥  Oh no! A sneaky trap—better luck next time.")
        return False

def play_game():
    name = greet_player()
    play_again = "yes"
    while play_again == "yes":
        treasure_cave = random.randint(1, 2)
        chosen_cave = choose_cave()
        reveal_outcome(chosen_cave, treasure_cave)
        play_again = input("\nDo you want to play again? (yes/no) ").lower()
    print(f"\nThanks for playing, {name}! See you on the next adventure. 👋")

if __name__ == "__main__":
    play_game()


```
