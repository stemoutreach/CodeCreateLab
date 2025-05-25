# Level 3 – Sense HAT Lab

## 🧠 Learning Objectives

* Display text on the LED matrix
* Use the joystick as input
* Read temperature, humidity, and orientation sensors

## 🧰 Materials Needed

* Raspberry Pi with Sense HAT attached
* Thonny Python IDE
* `sense_hat` Python library (included in Raspberry Pi OS)

## 📝 Instructions

1. **Import the Library**:

```python
from sense_hat import SenseHat
sense = SenseHat()
```

2. **Display a Message**:

```python
sense.show_message("Hello Pi!", text_colour=[0, 255, 0])
```

3. **Use Joystick Input**:

```python
for event in sense.stick.get_events():
    print(event.direction, event.action)
```

4. **Read Sensor Data**:

```python
temp = sense.get_temperature()
humidity = sense.get_humidity()
print(f"Temp: {temp:.1f} C, Humidity: {humidity:.1f}%")
```

## 🧪 Mini Challenge

* Create a weather station script that displays temperature and humidity on the LED display.
* Add joystick controls to cycle between sensors.

## ✅ Checkpoint

To pass this level, demonstrate:

* A message displayed on the LED matrix
* A working joystick input script
* A weather station reading at least one sensor

---

[Back to Main README](README.md)
