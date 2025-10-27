# 🛰️2 Sense HAT Guide

## What is the Sense HAT?

The **Sense HAT** is an add-on board for the Raspberry Pi with built-in sensors and an 8×8 RGB LED display. It was developed by the Raspberry Pi Foundation and flown on the International Space Station to run student-written code.

It includes:
- ✅ 8×8 LED matrix (for output)
- ✅ Joystick (for input)
- ✅ Temperature, Humidity, Pressure sensors
- ✅ Gyroscope, Accelerometer, Magnetometer (IMU)

---

## 🧠 Learning Objectives

After completing this guide, you should be able to:
- Access the Sense HAT’s LED display
- Read environmental sensor data
- Control basic output using code
- Understand real-time data collection on hardware

If you need help with the above concepts, take a look at the following
- [0 Python Basics Guide](/Guides/0-Python_Basics_Guide.md)
- [1 Python Functions Guide](/Guides/1-Python_Functions_Guide.md)

---

## 🛠️ Setup

### Step 1: Connect the Sense HAT
Place it directly on the GPIO pins of your Raspberry Pi. No additional wires needed.

### Step 2: Install the Sense HAT library
Open a terminal and run:

```bash
sudo apt update
sudo apt install sense-hat
```

To test the install:

```bash
from sense_hat import SenseHat
sense = SenseHat()
sense.show_message("Hi!")
```

If “Hi!” scrolls across the LEDs, you're good to go!

---

## 🐍 Example Code – Display a Message

```python
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

sense.show_message("Hello, Code & Create!", text_colour=(0, 255, 0))
```

---

## 🌡️ Example Code – Read Temperature

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while True:
    temp = sense.get_temperature()
    print(f"Temperature: {temp:.1f}°C")
    sleep(2)
```

---

## 🎮 Example Code – Joystick Input

```python
from sense_hat import SenseHat
sense = SenseHat()

def handle_event(event):
    print(f"Direction: {event.direction}, Action: {event.action}")

sense.stick.direction_any = handle_event

while True:
    pass  # Infinite loop so joystick can keep listening
```

---

## 🧪 Try These Challenges

1. **Weather Station**  
   Display the current temperature and humidity every 5 seconds.

2. **Color Toggle**  
   Use the joystick to toggle the LED display color between red and blue.

3. **Shake Detector**  
   Print “Shaken!” if the Pi is shaken using the accelerometer data.

---

## 📚 Resources

- [Official Sense HAT Python API](https://sense-hat.readthedocs.io/en/latest/)
- [Raspberry Pi Sense HAT Overview](https://www.raspberrypi.com/documentation/accessories/sense-hat.html)
- [Trinket.io – Sense HAT emulator](https://trinket.io/sense-hat)

---

## ✅ Next Step

Next [2 Sense Hat Basic Lab: Weather Warning Light](/Labs/2-SenseHat_Basic_Lab.md) 
