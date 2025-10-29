---
title: PicoBot – Motors & Ultrasonic
level: 04
estimated_time: 60–90 min
prereqs:
  - Guide: ../Guides/03-pico-breadboarding.md
outcomes:
  - Wire an L298N motor driver to the Pico and power the motors safely
  - Write reusable motor control functions (forward, backward, stop, left, right)
  - Read distance with an HC‑SR04 (ultrasonic) using MicroPython
  - Combine movement + sensing for simple obstacle-avoidance behaviors
hardware:
  - Raspberry Pi Pico (or Pico W)
  - L298N motor driver + 2 DC gear motors + wheels + chassis
  - External battery pack for motors (e.g., 4xAA or 2S Li‑ion)
  - Breadboard/jumper wires
  - HC‑SR04 ultrasonic sensor
  - (Recommended) switch and separate 5V regulator for logic
---

# BLUF
In this guide, you’ll **wire** your PicoBot, create **reusable motor functions**, and add an **ultrasonic distance sensor**. These foundations set you up for the matching lab, **PicoBot Maze Explorer**, where the bot navigates around obstacles.

## What you’ll learn
- L298N wiring and safe power practices
- MicroPython `machine.Pin` for motor direction control
- Creating and testing movement helper functions
- Reading distance with `time_pulse_us`
- Combining sensor input with motion to make decisions

## Materials
- PicoBot chassis (motors, wheels, caster)
- Raspberry Pi Pico + micro‑USB
- L298N motor driver
- HC‑SR04 ultrasonic sensor
- External battery pack for motors (do **not** power motors from the Pico’s 5V)
- Breadboard, jumpers, switch, resistors as needed

## Wiring
Use this reference mapping (adjust if your kit differs):

| Component              | Pico GPIO |
| ---------------------- | --------- |
| Motor A IN1            | GP6       |
| Motor A IN2            | GP7       |
| Enable A               | GP8       |
| Motor B IN3            | GP4       |
| Motor B IN4            | GP3       |
| Enable B               | GP2       |
| Ultrasonic Trigger     | GP14      |
| Ultrasonic Echo        | GP15      |

### Photos (reference)
> These show typical wiring with the Pico + L298N + Ultrasonic.

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/Pico-L298N.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot17.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot19.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot18.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot20.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot25.jpg" width="600">

> **Power tip:** Power **motors** from a separate battery pack into the L298N (VIN + GND). Share **GND** between the L298N and the Pico. Power the **Pico** via USB (for development) or a regulated 5V → VSYS.

## Walkthrough

### 1) Starter code: set up pins and basic motion
```python
from machine import Pin
import time

# Motor A (OUT1, OUT2)
In1 = Pin(6, Pin.OUT)
In2 = Pin(7, Pin.OUT)
EN_A = Pin(8, Pin.OUT)

# Motor B (OUT3, OUT4)
In3 = Pin(4, Pin.OUT)
In4 = Pin(3, Pin.OUT)
EN_B = Pin(2, Pin.OUT)

# Enable both motors
EN_A.high()
EN_B.high()

def stop():
    In1.low(); In2.low()
    In3.low(); In4.low()

def move_forward():
    In1.high(); In2.low()
    In3.high(); In4.low()

def move_backward():
    In1.low();  In2.high()
    In3.low();  In4.high()

def turn_left():
    # Left = A backward, B forward (pivot-ish)
    In1.low();  In2.high()
    In3.high(); In4.low()

def turn_right():
    # Right = A forward, B backward (pivot-ish)
    In1.high(); In2.low()
    In3.low();  In4.high()

# Quick test
move_forward()
time.sleep(2)
stop()
```

> If motors spin the wrong way, swap the wires on one motor **or** flip the logic in your functions.

### 2) Add ultrasonic distance
```python
from machine import Pin, time_pulse_us
import time

TRIG = Pin(14, Pin.OUT)
ECHO = Pin(15, Pin.IN)

def read_distance_cm(timeout_us=25000):
    # Ensure trigger is low
    TRIG.low()
    time.sleep_us(2)
    # 10µs trigger pulse
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()

    # Measure echo pulse width (HIGH duration)
    duration = time_pulse_us(ECHO, 1, timeout_us)
    if duration < 0:
        return None  # timeout or invalid

    # Sound speed ~343 m/s → 0.0343 cm/µs; divide by 2 (out-and-back)
    dist_cm = (duration * 0.0343) / 2.0
    return dist_cm

# Demo read
for _ in range(5):
    d = read_distance_cm()
    print("distance:", "timeout" if d is None else f"{d:.1f} cm")
    time.sleep(0.3)
```

### 3) Combine motion + sensing (simple avoid)
```python
def drive_with_avoid(threshold_cm=20):
    try:
        while True:
            d = read_distance_cm()
            if d is None:
                stop()
                time.sleep(0.1)
                continue

            if d < threshold_cm:
                stop()
                time.sleep(0.2)
                move_backward()
                time.sleep(0.5)
                turn_right()
                time.sleep(0.4)
                stop()
            else:
                move_forward()
            time.sleep(0.05)
    except KeyboardInterrupt:
        stop()

# drive_with_avoid()
```

> Tweak `threshold_cm` and timings for your bot. Add randomness to turns to reduce getting stuck.

## Check your understanding
1. Why must the motor battery’s **GND** be connected to the Pico’s **GND**?
2. What does `time_pulse_us(ECHO, 1, timeout)` measure?
3. Why do we divide the ultrasonic distance by **2**?

## Try it: Mini‑exercise
Create `square_drive(side_ms=800)` to drive a rough square:
1. Forward for `side_ms`  
2. Stop briefly  
3. Turn right ~90° (experiment with `sleep` value)  
4. Repeat 4 times  
> Stretch: add a `speed` notion later with PWM (requires changing EN pins to PWM).

## Troubleshooting
- **Motors don’t spin** → Check L298N enable pins are **HIGH**. Verify battery voltage and polarity. Ensure shared **GND**.
- **Spins in place when “forward”** → One motor is reversed. Swap the leads on one motor **or** adjust the logic.
- **Ultrasonic always `None`** → Confirm TRIG/ECHO pins; ensure nothing blocks the sensor; increase `timeout_us`.
- **Distance seems wrong** → Keep sensor upright; avoid soft/angled targets; add a small average over multiple reads.

## Next up
Do the matching lab: **[04 – PicoBot Maze Explorer](../Labs/04-picobot-maze-explorer.md)**

## Attributions & License
- Wiring and starter ideas adapted from the original “4 PicoBot Guide” and PicoBot repo images.
- See repository LICENSE for terms.
