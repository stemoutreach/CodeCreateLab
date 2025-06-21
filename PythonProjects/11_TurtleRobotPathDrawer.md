# Turtle Robot Path Drawer

## Description
Use Turtle graphics to simulate robot commands and draw the path on the screen.

## What To Do
- [ ] Define a function for the `forward` command using Turtle.
- [ ] Add your own functions for `backward`, `left`, and `right`.
- [ ] Ask the user for 5 commands using input().
- [ ] Use your functions to move the turtle and draw the robot’s path.
- [ ] Challenge: Add a stop command that lifts the pen and prints 'Robot paused'.

---

## 🧪 Starter Code
```python
import turtle

# Setup turtle
t = turtle.Turtle()

# Example: Move forward
def move_forward():
    t.forward(50)

# TODO: Define move_backward
# def move_backward():
#     ...

# TODO: Define turn_left
# def turn_left():
#     ...

# TODO: Define turn_right
# def turn_right():
#     ...

# TODO: Define stop (optional challenge)
# def stop():
#     ...

# Get 5 commands from user
for i in range(5):
    cmd = input("Enter command (forward, backward, left, right, stop): ").lower()
    if cmd == "forward":
        move_forward()
    elif cmd == "backward":
        # call your move_backward function
        pass
    elif cmd == "left":
        # call your turn_left function
        pass
    elif cmd == "right":
        # call your turn_right function
        pass
    elif cmd == "stop":
        # call your stop function
        pass
    else:
        print("Unknown command.")

turtle.done()
```