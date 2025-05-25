# Level 7 – MasterPi: Integrating Ultrasonic Sensor

## 🧠 Learning Objectives

* Understand how ultrasonic sensors work
* Measure distance to obstacles
* Use sensor input to adjust robot movement

## 🧰 Materials Needed

* MasterPi robot with ultrasonic sensor connected
* Raspberry Pi with Python SDK
* Hiwonder or custom sensor library

## 📝 Instructions

1. **Read Distance**:

```python
from Robot import Ultrasonic
sensor = Ultrasonic()
distance = sensor.get_distance()
print(f"Distance: {distance} cm")
```

2. **Obstacle Avoidance**:

* Read distance repeatedly
* Stop or turn the robot if an object is detected within a set threshold

## 🧪 Mini Challenge

* Program the robot to drive forward and stop when an object is closer than 20 cm

## ✅ Checkpoint

To pass this level, demonstrate:

* A working ultrasonic sensor
* Movement logic that reacts to nearby obstacles

---

[Back to Main README](README.md)
