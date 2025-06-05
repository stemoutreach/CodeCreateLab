
# Level 4 – Breadboarding Basics: Learn by Recipe

## 🧠 Learning Objectives

- Learn how to use GPIO pins through real-world projects
- Understand how inputs (buttons/sensors) and outputs (LEDs) work together
- Explore and modify recipes from the official [GPIOZero Recipes](https://gpiozero.readthedocs.io/en/latest/recipes.html)

## 🧰 Materials Needed

- Raspberry Pi with GPIO access
- Breadboard and jumper wires
- LEDs (2–3) and resistors (220–330Ω)
- Push button
- (Optional) sensors like TMP36 or light sensor

---

## 🔌 Intro to GPIO & Breadboards

GPIO stands for General Purpose Input/Output. These are the physical pins on your Raspberry Pi that can be used to control electronic components like LEDs, buttons, and sensors.

Breadboards are tools for prototyping electronic circuits without soldering. They allow you to easily connect components together using jumper wires.

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Insidebread.jpg" width="400" >




### Key Concepts:
- GPIO pins can send or receive signals
- Breadboards help you organize and test circuits
- Use resistors to protect LEDs from too much current
- Each GPIO pin has a number — use the [GPIO Pinout Guide](https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering)

Example:
Connect an LED's long leg (positive) to GPIO17 through a resistor, and the short leg (ground) to a GND pin on the Pi.

---

## 🧭 Explore GPIOZero Recipes

Visit: [GPIOZero Recipes](https://gpiozero.readthedocs.io/en/latest/recipes.html)  
Start exploring how to blink an LED, use a button, and interact with sensors. Below are a few recommended recipes to try.

### 💡 Recipe 1: Blink an LED
[Recipe: Blinking an LED](https://gpiozero.readthedocs.io/en/latest/recipes.html#led)

```python
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

> 💬 Try: Change the timing, or make it blink twice quickly, then pause.

---

### 🟢 Recipe 2: Button Press LED
[Recipe: Button Input](https://gpiozero.readthedocs.io/en/latest/recipes.html#button)

```python
from gpiozero import LED, Button

led = LED(17)
button = Button(2)

button.when_pressed = led.on
button.when_released = led.off
```

> 💬 Try: Reverse the behavior, or make it toggle instead of just on/off.

---

### 🚦 Mini Challenge: Traffic Light Controller

Use 2 LEDs (red and green) and a button to create a basic traffic light:
- Green is on by default.
- When button is pressed, red turns on.
- After a few seconds, green turns back on.

---

### 🌡️ Recipe 3 (Optional): Read a Sensor Value
If you have a TMP36 or light sensor, try this advanced recipe:
[Analog Sensor with MCP3008](https://gpiozero.readthedocs.io/en/latest/recipes.html#light-sensor)

---

## ✅ Level Checkpoint

To pass this level, show:
- Working LED blink or button project
- You modified a recipe in some way (change pins, timing, behavior)
- (Optional) Used a sensor to read or display data

---

## 🧠 Reflect & Share

- What did you change or experiment with?
- Did you encounter an error? How did you figure it out?
- What’s one idea you’d like to try next?

---

[🔙 Back to Main README](README.md)
