# 🐢 Python Turtle Graphics Guide – Code & Create Lab

## 🧠 Learning Objectives

- Understand what the `turtle` module is and how to use it
- Learn basic turtle commands: movement, turning, color
- Draw shapes and patterns using code
- Create functions to simplify drawing

---

## 🐢 What is Turtle?

`Turtle` is a Python module that lets you control a turtle on the screen. It's a great way to learn coding by creating drawings.

---

## 🛠️ Getting Started

```python
import turtle

t = turtle.Turtle()
t.forward(100)  # Move forward 100 pixels
t.right(90)     # Turn right 90 degrees
```

Click ▶️ Run to see the turtle move!

---

## ✏️ Drawing a Square

```python
import turtle
t = turtle.Turtle()

for _ in range(4):
    t.forward(100)
    t.right(90)
```

---

## 🔺 Drawing a Star

```python
import turtle
t = turtle.Turtle()

for _ in range(5):
    t.forward(100)
    t.right(144)
```

---

## 🎨 Adding Color

```python
import turtle
t = turtle.Turtle()

t.color("red")
t.begin_fill()
for _ in range(4):
    t.forward(100)
    t.right(90)
t.end_fill()
```

---

## ✨ Fun Pattern Example

```python
import turtle
t = turtle.Turtle()
t.speed(10)

colors = ["red", "green", "blue", "purple"]

for i in range(36):
    t.color(colors[i % 4])
    t.forward(100)
    t.right(60)
    t.forward(100)
    t.right(120)
    t.right(10)
```

---

## 🧩 Create a Function

```python
def draw_square(length):
    for _ in range(4):
        t.forward(length)
        t.right(90)

draw_square(150)
```

---

## ✅ Try These Turtle Challenges

1. **Draw a triangle, square, and hexagon**
2. **Use a loop to make a spiral**
3. **Draw a face or robot using only turtle commands**
4. **Create your own turtle function to draw a shape**
5. **Make a flower or snowflake with repeating shapes**

---

## 📚 More Resources

- [Python Turtle Docs](https://docs.python.org/3/library/turtle.html)
- [Turtle Examples on trinket.io](https://trinket.io/search?q=turtle)

---

## 🧠 Reflect & Share

- What shapes were easy or hard to draw?
- How can loops and functions help you draw better designs?
- What creative turtle art could you make next?

---

Next: Try writing your own shape drawing function and share it with a classmate!
