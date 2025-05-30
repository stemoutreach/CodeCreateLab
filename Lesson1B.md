# Lesson 1B – Python Intro: Print, Input, and Variables

Welcome to Lesson 1B of the Code and Create Lab! Now that your Raspberry Pi is set up, it’s time to write your first Python code using Thonny.

---

## 🎓 Goals

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

---

## 🎯 Practice Activities

Try these in Thonny:

1. Print your name
2. Print `5 + 3`
3. Ask the user their favorite color and repeat it
4. Ask for two numbers and print their sum
5. Make a greeting using a name

---

## ✅ What’s Next?

You’re ready for Level 2, where you’ll learn about loops, conditionals, and functions!
