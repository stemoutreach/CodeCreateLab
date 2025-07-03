# 🏴‍☠️ Mini Treasure Hunt Game (Python)

Welcome to the **Mini Treasure Hunt Game** – a fun way to learn Python by creating an interactive adventure! You'll use `print`, `input`, conditions (`if`), loops (`while`), and functions to build your very own treasure hunt.

---

## 🎮 Game Overview

In this game:
- The player is greeted and asked for their explorer name.
- They're told to choose between two mysterious caves.
- One cave has **treasure**, the other has a **trap**!
- The player finds out what happens based on their choice.
- They can choose to **play again** or exit.

---

## 🧠 Python Concepts You'll Learn

| Concept     | Python Example                | What It Does                            |
|-------------|-------------------------------|------------------------------------------|
| `print()`   | `print("Welcome!")`           | Shows messages on screen                 |
| `input()`   | `input("Your name: ")`        | Gets user input                          |
| `if` / `else` | `if choice == 1:`            | Checks conditions and runs different code |
| `while`     | `while play_again == "yes":`  | Repeats parts of your code               |
| `def`       | `def greet_player():`         | Creates a function you can call later    |

---

## 🧱 Step-by-Step Instructions

### 1️⃣ Greet the Player

Start with a function to say hello and ask for their name.

```python
def greet_player():
    print("🏴‍☠️  Welcome to the Mini Treasure Hunt!")
    name = input("What’s your explorer name? ")
    print(f"\nAhoy, {name}! Your quest is to find the hidden treasure chest.\n")
    return name
```

---

### 2️⃣ Let the Player Choose a Cave

Use a loop to make sure they choose **1** or **2**.

```python
def choose_cave():
    while True:
        choice = input("Do you enter cave 1 or cave 2? (type 1 or 2) ")
        if choice in ("1", "2"):
            return int(choice)
        print("Please choose 1 or 2! 🧐")
```

---

### 3️⃣ Determine the Outcome

Use `random` to secretly pick the treasure cave. Then check if the player guessed right.

```python
import random

def reveal_outcome(chosen_cave, treasure_cave):
    if chosen_cave == treasure_cave:
        print("✨  You found the treasure! Congratulations! 🎉")
        return True
    else:
        print("💥  Oh no! A sneaky trap—better luck next time.")
        return False
```

---

### 4️⃣ Build the Main Game Loop

Create a main function that calls the others and repeats the game if the player wants to.

```python
def play_game():
    name = greet_player()
    play_again = "yes"
    while play_again == "yes":
        treasure_cave = random.randint(1, 2)
        chosen_cave = choose_cave()
        reveal_outcome(chosen_cave, treasure_cave)
        play_again = input("\nDo you want to play again? (yes/no) ").lower()
    print(f"\nThanks for playing, {name}! See you on the next adventure. 👋")
```

Then run it:

```python
if __name__ == "__main__":
    play_game()
```

---

## 💡 Bonus Ideas

Want to make it cooler?

- Add more than 2 caves (3 or 4!)
- Create a map using `print()` or even `turtle`
- Add traps, monsters, or keys
- Give players health or score
- Let players create their own cave descriptions

---

## 🧪 Challenge Yourself

After finishing the game:
- Modify the story and theme
- Add sound or color with external libraries
- Share your game with a friend!

---

Happy coding, adventurer! 🧭
