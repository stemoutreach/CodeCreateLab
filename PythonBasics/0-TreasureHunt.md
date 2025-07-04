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
    """Say hello and ask for the player's name."""
    print("🏴‍☠️  Welcome to the Mini Treasure Hunt!")
    # TODO: Ask for the player's explorer name.
    # TODO: Store the answer in a variable called 'name'.
    # TODO: Print a friendly greeting that uses their name.
    return name  # Make sure 'name' exists!
```

---

### 2️⃣ Let the Player Choose a Cave

Use a loop to make sure they choose **1** or **2**.

```python
def choose_cave():
    """Ask the player to pick cave 1 or 2 until they type a valid choice."""
    while True:
        # TODO: Ask the player: "Do you enter cave 1 or cave 2? (type 1 or 2) "
        # TODO: If they typed "1" or "2", return their choice as an int.
        # TODO: Otherwise, print a helpful message and repeat the loop.
        pass  # remove this when you write the code

```

---

### 3️⃣ Determine the Outcome

 Then check if the player guessed right.

```python
def reveal_outcome(chosen_cave, treasure_cave):
    """Tell the player if they found treasure or a trap."""
    # TODO: If the caves match, celebrate!
    # TODO: Otherwise, tell them they hit a trap.
    # TODO: Return True if they won, False if they lost.
    pass
```

---

### 4️⃣ Build the Main Game Loop

Create a main function that calls the others and repeats the game if the player wants to. Use `random` to secretly pick the treasure cave.

```python
import random

def play_game():
    """Main game loop so players can play many times."""
    # TODO: Call greet_player() and save the returned name.
    # TODO: Set a variable 'play_again' to "yes".
    # TODO: While the player wants to keep playing:
    #       * Pick a random treasure cave (1 or 2) with random.randint()
    #       * Call choose_cave() to get the player's guess
    #       * Call reveal_outcome() to see if they won
    #       * Ask if they want to play again (yes/no)
    # TODO: After the loop ends, say goodbye to the player by name.
    pass
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
