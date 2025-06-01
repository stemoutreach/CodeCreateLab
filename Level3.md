# 🧠 Level 3 – Sense HAT Lab

## 🚀 Overview
The **Sense HAT** is an add-on board for the Raspberry Pi featuring:
- An 8x8 RGB LED matrix
- A 5-button joystick
- Sensors for temperature, humidity, pressure, and orientation (gyroscope, accelerometer, magnetometer)

It’s a great tool for learning **input/output**, **sensor data**, and **interactive display**.

## 🌐 Helpful References
- [Raspberry Pi Sense HAT Documentation](https://www.raspberrypi.com/documentation/accessories/sense-hat.html)
- [Trinket Sense HAT Simulator](https://trinket.io/sense-hat)
- [Sense HAT Python API Docs](https://sense-hat.readthedocs.io/en/latest/)

## 🧰 Materials Needed
- Raspberry Pi with Sense HAT attached
- Thonny Python IDE
- `sense_hat` Python library (pre-installed on Raspberry Pi OS)

## 📚 Sense HAT Library Basics

### 1️⃣ Import the Library
```python
from sense_hat import SenseHat
sense = SenseHat()
```

### 2️⃣ Display a Message
```python
sense.show_message("Hello!", text_colour=[255, 0, 0])
```
This scrolls a message across the LED display.

### 3️⃣ Read Sensor Data
```python
temp = sense.get_temperature()
humidity = sense.get_humidity()
pressure = sense.get_pressure()
print(f"Temp: {temp:.1f} C, Humidity: {humidity:.1f}%, Pressure: {pressure:.1f} hPa")
```

### 4️⃣ Joystick Input
```python
for event in sense.stick.get_events():
    print(event.direction, event.action)
```
Directions include `'up'`, `'down'`, `'left'`, `'right'`, `'middle'`.

---

## 🧪 Mini Challenges

### 🔷 Challenge 1: Scroll Your Name
Use `show_message()` to scroll your name in your favorite color.

### 🔷 Challenge 2: Weather Station
- Show temperature and humidity on the LED display.
- Use the joystick to switch between temperature and humidity display.

### 🔷 Challenge 3: Tilt Detector
Print a message when the Pi is tilted beyond a certain angle.

> 💡 Hint: Use `get_orientation()` to check pitch, roll, yaw.

---

## ✅ Level 3 Checkpoint

Demonstrate all of the following:
- [ ] Scroll a custom message on the LED matrix
- [ ] Capture and respond to a joystick direction
- [ ] Read at least one sensor and display the result

---

[Back to Main README](../README.md)
