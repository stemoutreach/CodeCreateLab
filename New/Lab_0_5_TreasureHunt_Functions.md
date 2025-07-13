# Lab 0.5 – Treasure Hunt (With Functions)

Time to level up! In this version of the Treasure Hunt, you'll improve your code by using functions.

## 🎯 Goal

Rewrite the basic treasure hunt program by organizing logic into functions.

## 🧰 What You Need to Know

Complete the guide:
- `Python_Functions_Guide.md`

## ✅ Requirements

- Create a function to display a welcome message.
- Create a function to get user input.
- Create a function to check the input and return a result.
- Use a loop to call your functions until the treasure is found.

## 🧠 Tips

Use functions like:
```python
def get_direction():
    return input("Choose a direction: ").lower()

def check_direction(direction):
    if direction == "north":
        print("There's a wall.")
        return False
    elif direction == "east":
        print("You found the treasure!")
        return True
    # Add other conditions
```

## 📝 To Do

```python
# TODO: Define a function for getting input
# TODO: Define a function for checking direction
# TODO: Define a function for printing welcome
# TODO: Use a loop to run the game
```

Keep your code clean and organized!
