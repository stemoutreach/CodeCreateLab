# Level 1 – Pi Setup & Python Intro

Welcome to Level 1 of the Code and Create Lab! In this level, you’ll learn how to:

* Set up your Raspberry Pi
* Use the terminal
* Write and run your first Python script
* Use `print()` to display messages
* Use `input()` to interact with the user

---

## 🔖 Python Basics

### 📃 What is a Variable?

A **variable** is a way to store information in your program so you can use it later. Think of it as a labeled box that holds something:

```python
name = "Scott"
age = 12
```

In this example:

* `name` holds the text "Scott"
* `age` holds the number 12

### 📝 What is `print()`?

The `print()` function tells the computer to show a message on the screen.

```python
print("Hello, world!")
```

This will display:

```
Hello, world!
```

You can also use it to show variables:

```python
name = "Scott"
print("My name is", name)
```

---

## 💻 Activity 1: Print Statements

Create a Python script that:

* Prints your name
* Prints the result of `5 + 3`
* Uses `input()` to ask the user their favorite color

---

## 🧐 Understanding `input()` in Python

### What is `input()`?

The `input()` function lets you ask the user to type something while your program is running.
Whatever the user types gets stored as **text** (a **string**).

### How to Use `input()`

```python
variable_name = input("Your message here: ")
```

* `"Your message here"` is the prompt.
* `variable_name` saves what the user typed.

### Example:

```python
name = input("What is your name? ")
print("Hello, " + name + "!")
```

### Input Numbers:

Use `int()` or `float()` to convert input to a number.

```python
age = input("How old are you? ")
age = int(age)
print("In 5 years, you will be", age + 5)
```

---

## 🎯 More Beginner Python Script Ideas

Try one or more of these practice activities:

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

6. **Emoji Banner**

```python
emoji = input("Enter your favorite emoji (like 😀): ")
print(emoji * 5)
```

7. **Custom Robot Name**

```python
first = input("Enter a word: ")
number = input("Enter a number: ")
print("Your robot name is:", first + number)
```

8. **ASCII Art**

```python
print("  ^  ")
print(" / \")
print("/___\")
print("|   |")
print("|___|")
```

9. **Repeat User Input**

```python
word = input("Say something: ")
print("You said:", word)
```

10. **Build a Phrase**

```python
word1 = input("Word 1: ")
word2 = input("Word 2: ")
word3 = input("Word 3: ")
print("You created the phrase:", word1 + " " + word2 + " " + word3)
```

---

## ✅ What’s Next?

In Level 2, you’ll begin using variables, loops, and conditionals to build smarter and more interactive programs!
