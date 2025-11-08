# 00 — Python Basics

> ### Quick Summary
> **Level:** 00 • **Time:** 30–45 min  
> **Prereqs:** None  
> **Hardware:** Computer only  
> **You’ll practice:** print/input, variables & types, conditionals, **for loops**, **f-strings**, boolean logic, indentation

# Why This Matters
These are your day‑one Python moves. You’ll use them in every lab—from Sense HAT pixels to driving a robot. Keep it simple, get quick wins, and build confidence.

---
## What you’ll learn
- Print and read input
- Store data in variables and check types
- Make decisions with `if / elif / else`
- Repeat actions with a **for loop** and `range()`
- Format output with **f‑strings**
- Combine conditions with **and / or / not**
- Keep code readable with **comments** and **indentation**

## Setup
- We use **Raspberry Pi 500** computers running Raspberry Pi OS.
- Open **Thonny** (Menu → Programming → Thonny).
- Create a new file named `basics.py`, then **Save** it in a folder you can find later (e.g., `Documents/CodeCreate/`).
- Click **Run ▶** to execute your program and check the **Shell** for output.

---
## 1) Say hello & read input
```python
name = input("What is your name? ")
print("Hello,", name)
```

---
## 2) Variables & types
```python
age = 12            # integer
height = 1.55       # float (meters)
is_student = True   # boolean
print(type(age), type(height), type(is_student))
```

---
## 3) Decisions: `if / elif / else`
```python
score = 87
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("Keep going!")
```

---
## 4) **for** loop (just one pattern)
Use `for` when you know how many times to repeat.
```python
for i in range(5):   # 0,1,2,3,4
    print(i)
```
Try: print numbers **1–5** instead.

---
## 5) Clean printing with **f‑strings**
```python
name = "Kai"
score = 87
print(f"{name} scored {score}")
```
No `+` needed—just write what you want to see.

---
## 6) Boolean logic (names only, one example)
```python
age = 12
with_adult = True
if age >= 13 or with_adult:
    print("Allowed")
```
Use **and**, **or**, **not** to combine conditions.

---
## 7) Comments & indentation
```python
# This is a comment
if True:
    print("Indented lines belong together")
```
Same indentation = same block.

---
## Mini practice (pick 1)
- **Loop count:** print numbers 1–5.  
- **Name letters:** ask for a name, then print each letter with a `for` loop.  
- **Score card:** ask for a name + score, print `"<name> scored <score>"` using an **f‑string**.

### Stretch (optional)
- Print the **squares** from 1–10 on one line.  
- Change the logic so *only* ages **13–18** are allowed (no adult override).

---
## Troubleshooting
- **IndentationError** → lines in a block don’t line up.  
- **`TypeError: can only concatenate str (not "int") to str`** → use an **f‑string** or `str(number)`.  
- **Nothing prints in a loop** → check your range and print is inside the loop.

---
## Next up
Continue to **[01 — Python Functions](01-python-functions.md)**, then try the matching lab **Treasure Hunt (Functions)**.
