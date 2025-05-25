# Level 5 – PicoBot: 2-Wheel Driving

## 🧠 Learning Objectives

* Understand DC motor basics
* Control motors with Python
* Sequence movements to navigate a simple path

## 🧰 Materials Needed

* PicoBot robot (prebuilt)
* Raspberry Pi Pico with MicroPython
* Thonny IDE with Pico connected via USB

## 📝 Instructions

1. **Connect to the Pico** in Thonny (select MicroPython (Raspberry Pi Pico))
2. **Blink LED to confirm** connection:

```python
from machine import Pin
import time
led = Pin(25, Pin.OUT)
while True:
    led.toggle()
    time.sleep(0.5)
```

3. **Drive motors**:

```python
from machine import Pin
import time
left_motor = Pin(16, Pin.OUT)
right_motor = Pin(17, Pin.OUT)

# Drive forward
left_motor.value(1)
right_motor.value(1)
time.sleep(1)
left_motor.value(0)
right_motor.value(0)
```

(Modify pins to match robot wiring.)

## 🧪 Mini Challenge

* Program your robot to move in a square or triangle pattern using timed movements.

## ✅ Checkpoint

To pass this level, demonstrate:

* A running PicoBot script that controls both wheels
* A repeatable pattern or sequence of movement

---

[Back to Main README](README.md)
