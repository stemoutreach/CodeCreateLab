# Level 4 – Breadboarding Basics

## 🧠 Learning Objectives

* Wire an LED with a resistor and control it with GPIO
* Use a button to trigger actions
* Read values from simple sensors (e.g., temperature or light sensor)

## 🧰 Materials Needed

* Raspberry Pi with GPIO access
* Breadboard, jumper wires
* LED, resistor (220Ω–330Ω)
* Push button
* (Optional) sensor such as TMP36 or photoresistor

## section title

### What Is the Raspberry Pi 3? (10 min)
- Overview of ports (USB, HDMI, GPIO, SD card)
- Differences from a regular laptop
- Introduce concept of general-purpose computing and sensors

    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/RPi3-B-intro.jpg" width="400" > 

### Intro to GPIO & Breadboarding (10–15 min)
- What are GPIO pins?
- Why and how to use a breadboard
- Show how a Pi pin can power an LED

     <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/SimpleLEDBreadboardExample.jpg" width="400" > 

    [GPIO Pin Numbering](https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering)

### 5. Blink an LED Using GPIOZero (30 min)
- Wire LED + resistor to GPIO pin using a breadboard
- Use the gpiozero library for easy code

**Example Code:**
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

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/BlinkLED-GPIO17.jpg" width="400" > 

## 🧪 Mini Challenge

* Build a simple traffic light simulator using 2 LEDs and a button.

## ✅ Checkpoint

To pass this level, demonstrate:

* A working LED blink script
* A button controlling a light or script action
* (Optional) Sensor data logging

---

[Back to Main README](README.md)
