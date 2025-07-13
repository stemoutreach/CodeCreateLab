# 🐍 Python Basics Guide – Getting Started

This guide includes an introduction to Python basics: printing, input, conditionals, loops, and functions.

---

# Python Intro: Print and Input

Welcome to Python Intro for Code and Create Lab! Now it’s time to write your first Python code using Thonny.

---

## 🧠 Learning Objectives

* Open Thonny Python editor
* Understand variables
* Use `print()` to display messages
* Use `input()` to get user input

---

## 📒 What is Thonny?

Thonny is a beginner-friendly Python editor already installed on Raspberry Pi.

### Open Thonny:

* Go to **Raspberry Pi Menu → Programming → Thonny Python IDE**

---

## 📃 What is a Variable?

A **variable** is a way to store information in your program.

```python
name = "Alex"
age = 12
```

---

## 📄 What is `print()`?

The `print()` function tells Python to show something on the screen.

```python
print("Hello, world!")
```

Output:

```
Hello, world!
```

You can also print variables:

```python
name = "Alex"
print("My name is", name)
```

---

## 🤔 What is `input()`?

`input()` asks the user to type something.

```python
name = input("What is your name? ")
print("Hello,", name)
```

### Input Numbers:

Use `int()` to turn text into a number:

```python
age = input("How old are you? ")
age = int(age)
print("In 5 years, you will be", age + 5)
```


## 🎯 More Beginner Python Script Ideas

1. **Favorite Food**

```python
food = input("What is your favorite food? ")
print("Yum! I like", food, "too!")
```

2. **Simple Mad Libs**

```python
noun = input("Give me a noun: ")
verb = input("Give me a verb: ")
print("The", noun, "loves to", verb, "every day.")
```

3. **Greeting Generator**

```python
name = input("What's your name? ")
print("Hello " + name + "! Nice to meet you.")
```

4. **Math with Input**

```python
num1 = input("Enter a number: ")
num2 = input("Enter another number: ")
print("Their sum is:", int(num1) + int(num2))
```

5. **Age in 5 Years**

```python
age = input("How old are you? ")
future_age = int(age) + 5
print("In 5 years, you will be", future_age, "years old.")
```

6. **Custom Robot Name**

```python
first = input("Enter a word: ")
number = input("Enter a number: ")
print("Your robot name is:", first + number)
```

7. **ASCII Art**

```python
print("  ^  ")
print(" / \ ")
print("/___\ ")
print("|   |")
print("|___|")
```

8. **Repeat User Input**

```python
word = input("Say something: ")
print("You said:", word)
```

9. **Build a Phrase**

```python
word1 = input("Word 1: ")
word2 = input("Word 2: ")
word3 = input("Word 3: ")
print("You created the phrase:", word1 + " " + word2 + " " + word3)
```





---

# Python Basics:  If Conditions, For and While Loops

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



---

# Python Basics: Functions

## 🧠 Learning Objectives

* Write and call functions

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

[0 Treasure Hunt Lab](/Labs/0-Treasure_Hunt_Lab.md)
