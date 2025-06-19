# Level 8 – MasterPi: Arm Movement

## 🧠 Learning Objectives

* Control servos with code
* Understand arm angles and basic kinematics
* Move the robotic arm to preset positions

## 🧰 Materials Needed

* MasterPi robot with servo arm
* Raspberry Pi + servo controller
* Python control library for servos (Hiwonder SDK or PWM driver)

## 📝 Instructions

1. **Move a Single Servo**:

```python
from Robot import Arm
arm = Arm()
arm.move_to(90)  # Set to 90 degrees
```

2. **Move Multiple Servos**:

* Coordinate multiple angles for basic pick-and-place movements

3. **Loop Through Motions**:

* Write functions to reset, pick, and place objects

## 🧪 Mini Challenge

* Program a sequence to move the arm from a rest position to a pick location and back

## ✅ Checkpoint

To pass this level, demonstrate:

* At least two servo movements to set positions
* A simple pick/place or sweep routine

---

[Back to Main README](README.md)
