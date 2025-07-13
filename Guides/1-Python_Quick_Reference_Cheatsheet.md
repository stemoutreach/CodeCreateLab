# 🐍 1 Python Quick-Reference Cheatsheet

## 🧰 Basics

```python
# Print to the screen
print("Hello, world!")

# Variables
temp = 23.5
name = "SenseBot"

# Data types
number = 42        # int
decimal = 3.14     # float
word = "text"      # string
flag = True        # bool
```

---

## 🔁 Loops & Conditions

```python
# If-else condition
if temp > 30:
    print("It's hot!")
elif temp < 10:
    print("It's cold!")
else:
    print("Nice weather.")

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# For loop
for i in range(5):
    print(i)
```

---

## 📦 Functions

```python
# Define a function
def greet(name):
    print("Hi " + name)

# Call it
greet("Alice")
```

---

## 🎮 Sense HAT (Basic)

```python
from sense_hat import SenseHat
sense = SenseHat()

# Show a message
sense.show_message("Hello!")

# Get sensor data
t = sense.get_temperature()
h = sense.get_humidity()
p = sense.get_pressure()

# Set LED color (x, y, [R,G,B])
sense.set_pixel(3, 3, [255, 0, 0])
sense.clear()  # Turns off LEDs
```

---

## 🎮 Sense HAT Joystick

```python
from sense_hat import ACTION_PRESSED

def handle_joystick(event):
    if event.action == ACTION_PRESSED:
        print("You pressed", event.direction)

sense.stick.direction_any = handle_joystick
```

---

✅ **Tip:** Use `Ctrl + C` to stop a running program safely.

