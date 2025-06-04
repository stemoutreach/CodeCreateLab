# 🔍 Level 2 Challenge: Python Basics

## 🎯 Challenge Overview
Complete each task below to show you’ve mastered loops, conditionals, and functions. Be ready to explain your code!

---

## ✅ Challenge 1: Looping Countdown
Write a **`for` loop** that counts down from 10 to 1 and then prints **"Blast off!"**

### Sample Output:
```
10
9
...
1
Blast off!
```

---

## ✅ Challenge 2: Odd or Even Checker
Ask the user to enter a number. Use an **`if/else` conditional** to print whether the number is **odd or even**.

> 💡 Hint: Use the modulo operator `%` to find the remainder.

---

## ✅ Challenge 3: Your Own Greeting Function
Write a **function** called `greet_user(name)` that prints a custom greeting. Then call it at least twice with different names.

Example:
```python
greet_user("Sam") → "Hello, Sam! Welcome!"
```

---

## ✅ Challenge 4: Keep Asking (While Loop)
Use a **`while` loop** to keep asking the user to type a password until they get it right. When they do, print "Access granted."

> Bonus: Count how many tries it took.

---

## ✅ Challenge 5: Double Trouble Function
Write a function `double_number(num)` that returns **twice** the number you give it. Ask the user for a number and use your function to print the result.

---

## ✅ Challenge 6: Turtle Art
Write a turtle program to that completes this image

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/turtle.jpg" width="400" > 

Finish the code for the 4th design in the above image.
```python
import turtle
import random
wn = turtle.Screen()
t = turtle.Turtle()

wn.bgcolor("blue")
t.color("white")

t.penup()
t.backward(600)
t.right(90)
t.forward(200)
t.left(90)
t.forward(700)
t.pendown()

for i in range(2):
  t.forward(100)
  t.right(60)
  t.forward(100)
  t.right(120)

t.penup()
t.forward(-350)
t.pendown()

for i in range(3):
  for i in range(2):
    t.forward(100)
    t.right(60)
    t.forward(100)
    t.right(120)
  t.right(120)
  
t.penup()
t.right(90)
t.forward(-400)
t.left(90)
t.pendown()

for i in range(5):
  for i in range(2):
    t.forward(100)
    t.right(60)
    t.forward(100)
    t.right(120)
  t.right(72)

t.penup()
t.forward(350)
t.pendown()

wn.exitonclick()
```



## 🎓 Bonus Challenge: Mix It Up
Create a simple math quiz:
- Ask the user a random addition question (e.g., 5 + 3)
- Get their answer
- Check if it’s correct using an `if` statement
- Use a `function` to generate and return random questions

---

## 📸 Submission Checklist
Before moving to Level 3, your script should include:
- [ ] One `for` or `while` loop
- [ ] One `if`/`else` statement
- [ ] One function (custom-defined)
- [ ] User input and printed output

---

## 🧪 Leveling Up?

Once you've completed the above tasks, show your work to a mentor or coach to be able to move on.

---

## ✅ What’s Next?

You’re ready for  **[Level 3 – Sense HAT Lab](../Level3.md)**!, where you’ll learn about Sense HAT where you will Code interactive input/output using the Sense HAT without breadboarding.
