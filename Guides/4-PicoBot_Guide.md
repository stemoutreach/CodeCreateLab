# 4 PicoBot Guide

## Overview

In this guide, you'll create reusable functions for your PicoBot to control motors and sensors effectively. Complete each step using provided ToDos with guidance.

## Areas to Complete

### 1. Wiring the Robot

**Objective:**
Wire your PicoBot correctly using the provided materials and instructions.

**Materials:**

* PicoBot Chassis
* Raspberry Pi Pico
* Ultrasonic Sensor
* L298N Motor Driver

**Wiring Reference:**

| Component          | GPIO Pin |
| ------------------ | -------- |
| Motor A IN1        | GP6      |
| Motor A IN2        | GP7      |
| Enable A           | GP8      |
| Motor B IN3        | GP4      |
| Motor B IN4        | GP3      |
| Enable B           | GP2      |
| Ultrasonic Trigger | GP14     |
| Ultrasonic Echo    | GP15     |

# **2. Wire PicoBot**

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/Pico-L298N.jpg" width="600" > 

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot17.jpg" width="600" > 

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot19.jpg" width="600" > 

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot18.jpg" width="600" > 

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot20.jpg" width="600" > 

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot25.jpg" width="600" > 


### 2. Writing Movement Functions

**Objective:**
Create and test individual functions for robot movements.

## 🧱 Starter Code with Comments

```python
from machine import Pin        # Lets us control the Pi Pico’s pins
import time                    # Lets us pause the program

# Motor A (connected to OUT1 and OUT2 on the L298N)
In1 = Pin(6, Pin.OUT)          # Sets GPIO 6 as an output for Motor A direction
In2 = Pin(7, Pin.OUT)          # Sets GPIO 7 as an output for Motor A direction
EN_A = Pin(8, Pin.OUT)         # Sets GPIO 8 as output to enable Motor A

# Motor B (connected to OUT3 and OUT4 on the L298N)
In3 = Pin(4, Pin.OUT)          # Sets GPIO 4 as an output for Motor B direction
In4 = Pin(3, Pin.OUT)          # Sets GPIO 3 as an output for Motor B direction
EN_B = Pin(2, Pin.OUT)         # Sets GPIO 2 as output to enable Motor B

# Turn both motors ON by setting enable pins HIGH
EN_A.high()                    # Turns on Motor A
EN_B.high()                    # Turns on Motor B

# Function to move the robot forward
def move_forward():
    In1.high()                 # Motor A spins forward
    In2.low()
    In3.high()                 # Motor B spins forward
    In4.low()

# Function to stop both motors
def stop():
    In1.low()                  # Stop Motor A
    In2.low()
    In3.low()                  # Stop Motor B
    In4.low()

# TODO: Write your own functions below!

def move_backward():
    # Hint: reverse both motors by switching the direction pins
    pass

def turn_left():
    # Hint: try stopping or reversing one motor
    pass

def turn_right():
    # Hint: try the opposite of turn_left
    pass

# Try it out!
move_forward()                 # Move forward
time.sleep(2)                  # Wait for 2 seconds
stop()                         # Stop the robot
```

### 3. Adding Ultrasonic Sensor

**Objective:**
Add sensor reading capabilities.

**Ultrasonic Function with ToDos:**

```python
from machine import Pin, time_pulse_us

# TODO: Set up your trigger and echo pins based on your wiring

def read_distance():
    # TODO: Implement the ultrasonic sensor reading and return distance in cm
    pass
```

---

Next [4 PicoBot Lab-Maze Explorer](/Labs/4-PicoBot_Lab-Maze_Explorer.md) 
