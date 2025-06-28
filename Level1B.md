# Level 1B – Python Intro: Print, Input, and Variables

Welcome to Lesson 1B of the Code and Create Lab! Now that your Raspberry Pi is set up, it’s time to write your first Python code using Thonny.

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

---

## 🎯 Practice Activities

Try these in Thonny:

1. Print your name
2. Print `5 + 3`
3. Ask the user their favorite color and repeat it
4. Ask for two numbers and print their sum
5. Make a greeting using a name

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

## 🧪 Ready to Level Up?

Complete the [Level 1 – Challenge](Challenges/Level1Challenge.md) and show your work to a mentor or coach to move on.


