# 🏴‍☠️ Mini Treasure Hunt Game – *Student Template*

Welcome, coder! This file **does not** give you the full solution.  
Your challenge is to **fill in all the `TODO:` sections** to make the game work.

---

## 🗺️ What You Need to Build

1. **Greet** the player and ask for their explorer name.  
2. Let them **choose a cave** (1 or 2).  
3. Randomly decide which cave has the **treasure**.  
4. Tell them if they **won** or **hit a trap**.  
5. Ask if they want to **play again**.

You’ll practice:

* `print()` – showing messages  
* `input()` – reading user answers  
* **Conditions** – `if` / `else`  
* **Loops** – `while`  
* **Functions** – breaking your code into bite‑sized parts  

---

## 💻 Skeleton Code (copy to `TreasureHunt_ToDo.py`)

```python
import random

def greet_player():
    """Say hello and ask for the player's name."""
    print("🏴‍☠️  Welcome to the Mini Treasure Hunt!")
    # TODO: Ask for the player's explorer name.
    # TODO: Store the answer in a variable called 'name'.
    # TODO: Print a friendly greeting that uses their name.
    return name  # Make sure 'name' exists!

def choose_cave():
    """Ask the player to pick cave 1 or 2 until they type a valid choice."""
    while True:
        # TODO: Ask the player: "Do you enter cave 1 or cave 2? (type 1 or 2) "
        # TODO: If they typed "1" or "2", return their choice as an int.
        # TODO: Otherwise, print a helpful message and repeat the loop.
        pass  # remove this when you write the code

def reveal_outcome(chosen_cave, treasure_cave):
    """Tell the player if they found treasure or a trap."""
    # TODO: If the caves match, celebrate!
    # TODO: Otherwise, tell them they hit a trap.
    # TODO: Return True if they won, False if they lost.
    pass

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

# TODO: Add the usual Python 'main guard' so the game starts
#       when you run the file directly, but not when you import it.
```

---

## 📝 Tips

* Test after you finish **each** function.
* Use **emoji** or ASCII art to make it fun!
* Stuck? Ask a friend (or your teacher) for one hint—not the whole answer. 😉

---

## 🌟 Stretch Goals (optional)

* Add **3 or more caves**.
* Track a **score** or **lives**.
* Use `turtle` to draw a little map.
* Give players an **inventory** (Python `list`).

Happy coding—and may the treasure be yours! 🧭
