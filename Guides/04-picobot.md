# PicoBot — Motors with L298N (No Sensors Yet)

> ### Quick Summary
> **Level:** 04 • **Time:** 60–90 min  
> **Prereqs:** Guides: [Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> **Hardware:** Raspberry Pi Pico (or Pico W); L298N motor driver; 2× DC gear motors + wheels + chassis; external motor battery pack; breadboard/jumper wires; (recommended) switch  
> **You’ll practice:** wiring L298N safely, mapping GPIO pins, writing motor movement functions (forward/back/left/right/stop), testing motion, and basic debugging

# Why This Matters
Before adding sensors and autonomy, you need a **reliable drive base**. In this guide you’ll wire the Pico to an **L298N motor driver** and write **reusable movement functions**. Getting this right now makes future labs (like obstacle avoidance and maze navigation) far easier.

---
## What you’ll learn
- Safe power practices for Pico + L298N (separate motor supply, shared ground)
- Mapping Pico **GPIO** pins to **L298N** inputs (IN1–IN4, ENA/ENB)
- Using `machine.Pin` to control H‑bridge direction
- Writing and testing helper functions: `forward`, `backward`, `left`, `right`, `stop`
- Verifying and correcting motor direction

## Setup
_This setup uses **MicroPython** with **Thonny**._  
- Flash MicroPython to the Pico (if needed).  
- In Thonny: select MicroPython (Raspberry Pi Pico) as the interpreter.  
- Create a new file `motors.py` on the Pico.  
- Prepare a **separate** battery pack for motors (e.g., 4×AA or 2S Li‑ion). Do **not** power motors from the Pico.

## Materials
- Raspberry Pi Pico (or Pico W) + micro‑USB cable  
- L298N motor driver board  
- 2× DC gear motors + wheels + chassis (PicoBot)  
- External motor battery pack and power switch  
- Breadboard and jumper wires  
- (Optional) standoffs/zip ties for cable management

---
## Walkthrough — Step by Step (with explanations)

### 1) Wiring the L298N to the Pico
**Idea:** Connect Pico GPIO pins to L298N inputs, and wire the motor battery to the L298N. Share **GND** between Pico and L298N.

| L298N pin            | Connects to                  |
|----------------------|------------------------------|
| ENA (Enable A)       | Pico **GP8** (can be PWM later) |
| IN1 (Motor A)        | Pico **GP6**                 |
| IN2 (Motor A)        | Pico **GP7**                 |
| INB / ENB (Enable B) | Pico **GP2** (can be PWM later) |
| IN3 (Motor B)        | Pico **GP4**                 |
| IN4 (Motor B)        | Pico **GP3**                 |
| L298N **VIN**        | Motor battery **+**          |
| L298N **GND**        | Motor battery **–** and **Pico GND** (shared) |

### Photos (reference)
> These show typical wiring with the Pico + L298N + Ultrasonic.

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/Pico-L298N.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot17.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot19.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot18.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot20.jpg" width="600">
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot25.jpg" width="600">

> **Power tip:** Power **motors** from a separate battery pack into the L298N (VIN + GND). Share **GND** between the L298N and the Pico. Power the **Pico** via USB (for development) or a regulated 5V → VSYS.

**Notes & pitfalls**
- **Separate supplies:** Pico via USB (VSYS) for logic; motors via battery into L298N **VIN/GND**.  
- **Shared ground:** Always connect **Pico GND ↔ L298N GND**.  
- If “forward” spins the **wrong way**, swap a motor’s leads **or** flip the logic in code.  
- If present, you can remove the L298N 5V‑EN jumper and power logic separately; not required for this guide.

### 2) Starter code: set up pins and basic motion
**Idea:** Use `machine.Pin` to define direction pins and enable pins, then build simple movement helpers.

```python
from machine import Pin
import time

# Motor A (OUT1, OUT2) - left or right depending on your build
IN1 = Pin(6, Pin.OUT)
IN2 = Pin(7, Pin.OUT)
ENA = Pin(8, Pin.OUT)   # set HIGH to enable A

# Motor B (OUT3, OUT4)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(3, Pin.OUT)
ENB = Pin(2, Pin.OUT)   # set HIGH to enable B

# Enable both channels (digital HIGH; later you can switch to PWM for speed)
ENA.high()
ENB.high()

def stop():
    IN1.low(); IN2.low()
    IN3.low(); IN4.low()

def forward():
    IN1.high(); IN2.low()
    IN3.high(); IN4.low()

def backward():
    IN1.low();  IN2.high()
    IN3.low();  IN4.high()

def left():
    # Pivot left: A backward, B forward (adjust for your bot)
    IN1.low();  IN2.high()
    IN3.high(); IN4.low()

def right():
    # Pivot right: A forward, B backward
    IN1.high(); IN2.low()
    IN3.low();  IN4.high()

# Quick smoke test
forward(); time.sleep(1.5)
stop();    time.sleep(0.3)
backward();time.sleep(1.0)
stop()
```

**Notes & pitfalls**
- If one wheel runs backward in `forward()`, your motor leads might be reversed. Swap one motor’s leads or flip the function logic.  
- If nothing moves: check battery **voltage**, **switch**, and that **ENA/ENB** are set **HIGH**.

### 3) Create small motion routines for testing
**Idea:** Build short scripts to validate wiring and turning behavior; tune `sleep()` durations for your chassis and battery.

```python
def nudge_forward(ms=300):
    forward(); time.sleep(ms/1000); stop()

def spin_in_place(ms=500):
    right(); time.sleep(ms/1000); stop()

def square_drive(side_ms=800, turn_ms=400):
    for _ in range(4):
        forward(); time.sleep(side_ms/1000); stop(); time.sleep(0.2)
        right();   time.sleep(turn_ms/1000); stop(); time.sleep(0.2)
```

**Notes & pitfalls**
- Turning timing depends on **surface**, **battery level**, and **wheelbase**. Expect to tune.  
- Keep total runtime short while testing to avoid motors overheating on stalled turns.

---
## Vocabulary
- **H‑bridge:** Circuit that lets you drive a DC motor **forward** or **reverse** by switching polarity.  
- **Enable (EN):** Pin that turns a motor channel **on/off**; with PWM it controls **speed**.  
- **PWM:** Pulse‑Width Modulation—rapid on/off switching to control average power (speed).  
- **Shared ground:** Both logic and motor circuits reference the **same 0V** node.  
- **Pivot turn:** One wheel forward, the other backward, to rotate in place.

---
## Check your understanding
1) Why must the Pico **GND** be connected to the L298N **GND**?  
2) What is the role of **ENA/ENB** on the L298N?  
3) If calling `forward()` spins in place, what two quick fixes can you try?  
4) Why might your 90° turn timing change over a session?

---
## Try it: Mini-exercises
- Write `triangle_drive()` to move in an approximate triangle (three forward legs + turns).  
- Add `spin_left(ms)` and `spin_right(ms)` helpers and compare pivot vs. spin behavior.  
- **Stretch:** Convert `ENA` and `ENB` to **PWM** (e.g., `PWM(Pin(8))`) and add a `speed=0..65535` parameter to `forward()`.

---
## Troubleshooting
- **Motors don’t spin** → Make sure **ENA/ENB** are **HIGH**; verify battery is connected to **VIN/GND** on the L298N; check the switch.  
- **Only one side moves** → Check that IN1/IN2 vs. IN3/IN4 go to the correct Pico pins; verify solder joints and jumpers.  
- **Moves backward when calling `forward()`** → Swap one motor’s leads or flip the logic for that side.  
- **Random resets** → Motor noise sagging voltage; use fresh batteries and keep Pico on USB power; ensure grounds are shared.

---
## Next up
Do the matching lab: **[04 – PicoBot Maze Explorer](../Labs/04-picobot-maze-explorer.md)**
