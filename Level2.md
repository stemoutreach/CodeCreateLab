
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
[Back to Main README](README.md)
