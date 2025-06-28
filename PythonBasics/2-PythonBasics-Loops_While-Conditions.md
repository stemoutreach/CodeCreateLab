# Level 2 – Python Basics

## 🧠 Learning Objectives


* Understand and use loops (`for`, `while`)
* Use conditionals (`if`, `else`, `elif`)

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

