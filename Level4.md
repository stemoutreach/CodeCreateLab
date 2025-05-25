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

## 📝 Instructions

1. **Blink an LED**:

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

for i in range(10):
    GPIO.output(18, True)
    time.sleep(0.5)
    GPIO.output(18, False)
    time.sleep(0.5)

GPIO.cleanup()
```

2. **Add a Button**: Use GPIO input and `GPIO.wait_for_edge()` or polling.
3. **Sensor Read**: Read an analog sensor with an ADC like MCP3008 if available.

## 🧪 Mini Challenge

* Build a simple traffic light simulator using 2 LEDs and a button.

## ✅ Checkpoint

To pass this level, demonstrate:

* A working LED blink script
* A button controlling a light or script action
* (Optional) Sensor data logging

---

[Back to Main README](README.md)
