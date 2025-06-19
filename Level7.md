# Level 6 – MasterPi: Mecanum Movement

## 🧠 Learning Objectives

* Understand mecanum wheel mechanics
* Drive the robot forward, backward, and sideways
* Write sequences using movement commands

## 🧰 Materials Needed

* MasterPi robot with Raspberry Pi
* Installed Python SDK (Hiwonder or custom)
* Sample code for movement control

## 📝 Instructions

1. **Test all motors** individually to confirm wiring
2. **Use SDK commands** for directional movement:

```python
from Robot import Robot
robot = Robot()
robot.forward()
robot.backward()
robot.left()
robot.right()
robot.stop()
```

3. **Create a motion sequence** combining directional commands and timed delays

## 🧪 Mini Challenge

* Program your MasterPi to drive in a figure-8 or box pattern

## ✅ Checkpoint

To pass this level, demonstrate:

* Controlled use of mecanum drive to move in multiple directions
* A timed driving routine

---

[Back to Main README](README.md)
