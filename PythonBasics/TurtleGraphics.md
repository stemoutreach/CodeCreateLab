# Level 2 – Python Basics

## 🧠 Learning Objectives

* Use Python variables and data types
* Understand and use loops (`for`, `while`)
* Use conditionals (`if`, `else`, `elif`)
* Write and call functions

---

## 🔁 Loops

### What is a Loop?
A loop repeats a block of code multiple times.

### 🔹 For Loop
Use when you know how many times to repeat.

```python
for i in range(5):
    print("This is loop number", i)
```

This will print 0 through 4.

### 🔹 While Loop
Use when repeating until something changes.

```python
count = 0
while count < 5:
    print("Counting:", count)
    count += 1
```

---

## 🔀 Conditionals

### What is a Conditional?
A conditional checks if something is true or false and runs different code depending on the result.

```python
age = int(input("Enter your age: "))

if age < 13:
    print("You're a kid!")
elif age < 18:
    print("You're a teen!")
else:
    print("You're an adult!")
```

Use `if`, `elif` (else if), and `else` to create branching paths.

---

## 🧩 Functions

### What is a Function?
A function is a reusable block of code. You define it once and use (call) it many times.

```python
def greet(name):
    print("Hello", name)

greet("Ada")
greet("Alan")
```

### Function with Return Value

```python
def add(x, y):
    return x + y

result = add(5, 3)
print("5 + 3 =", result)
```

---

## 🐢 Turtle Graphics

### What is Turtle?
Turtle is a Python module that lets you draw pictures and shapes by controlling a virtual "turtle" on the screen.

### How to Use It
1. Start by importing the module:
   ```python
   import turtle
   ```
2. Create a turtle:
   ```python
   t = turtle.Turtle()
   ```
3. Move and draw:
   ```python
   t.forward(100)
   t.right(90)
   ```

### Simple Examples

Draw a square:
```python
import turtle
t = turtle.Turtle()

for _ in range(4):
    t.forward(100)
    t.right(90)
```

Draw a star:
```python
import turtle
t = turtle.Turtle()

for _ in range(5):
    t.forward(100)
    t.right(144)
```

Click the "X" on the turtle window to close it when done.

---

## 🧪 Practice Ideas

Try building these in Thonny:

- A loop that counts from 1 to 10
- A program that asks a number and tells if it’s even or odd
- A function that returns double the input number
- A while loop that repeats until the user types "exit"

---

## ✅ Checkpoint

To complete Level 2, show:

* A working script with:
  - One loop (`for` or `while`)
  - One `if`/`else` conditional
  - One custom function

Optional: Draw a shape with `turtle`.

---

## 🧪 Ready to Level Up?

Complete the [Level 2 – Challenge](Challenges/Level2Challenge.md) and show your work to a mentor or coach to move on.
