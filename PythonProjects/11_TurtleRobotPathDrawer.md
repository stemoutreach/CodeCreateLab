# Turtle Robot Path Drawer

## Description
Use Turtle graphics to simulate robot commands and draw the path on the screen.

## What To Do
- [ ] Create a function for each command: forward, backward, left turn, right turn.
- [ ] Ask the user for 5 commands using input().
- [ ] Use Turtle to draw each movement on the screen.
- [ ] Challenge: Add a stop command that lifts the pen and prints 'Robot paused'.

---

## 🧪 Starter Code
```python
# Turtle Robot Path Drawer

import turtle

# Setup turtle
t = turtle.Turtle()

# TODO: Define command functions
# def move_forward():
#     t.forward(50)

# def move_backward():
#     t.backward(50)

# def turn_left():
#     t.left(90)

# def turn_right():
#     t.right(90)

# def stop():
#     t.penup()
#     print("Robot paused.")

# TODO: Ask user for 5 commands
# Example commands: forward, backward, left, right, stop
# for i in range(5):
#     cmd = input("Enter command (forward, backward, left, right, stop): ").lower()
#     if cmd == "forward":
#         move_forward()
#     elif cmd == "backward":
#         move_backward()
#     elif cmd == "left":
#         turn_left()
#     elif cmd == "right":
#         turn_right()
#     elif cmd == "stop":
#         stop()
#     else:
#         print("Unknown command")

# Keep the window open until closed by user
turtle.done()
```