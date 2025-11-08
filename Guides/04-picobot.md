# 04 — PicoBot: Drive with L298N (No Sensors)

> ### Quick Summary
> **Level:** 04 • **Time:** 60–90 min  
> **Prereqs:** [03 — Pico Breadboarding](./03-pico-breadboarding.md)  
> **Hardware:** Pico + L298N driver, 2 DC motors with wheels, battery pack, chassis, jumpers  
> **You’ll practice:** motor driver wiring, safe power & common ground, direction control, basic turning, optional PWM speed control

> **Learn → Try**: Learn concepts here with tiny examples, then Try a quick practice before you Do the matching Lab.

# Why This Matters
Driving a robot is the foundation for navigation challenges. You’ll wire a Pico to an L298N and write helpers for forward/back/turn/stop—skills you’ll reuse when we add sensors later.

---
## What you’ll learn
- Wire the L298N to two DC motors safely
- Share **GND** between motor battery, driver, and Pico
- Map Pico GPIOs to `IN1..IN4` and optional `ENA/ENB` PWM
- Write movement helpers (`forward`, `back`, `left`, `right`, `stop`)
- Calibrate straight driving and turning time
- Add optional speed control with PWM

## Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**
- Connect the **Pico** via micro‑USB
- Thonny → **Tools ▸ Options ▸ Interpreter** → **MicroPython (Raspberry Pi Pico)**; flash MicroPython (UF2) if prompted
- Create `drive.py` in `~/Documents/CodeCreate/`, then **Run ▶** and watch the **Shell**
- Keep the robot **wheels off the table** for first tests

## Materials  (ONLY include if hardware is involved)
- Raspberry Pi Pico / Pico W
- L298N dual H‑bridge module
- 2× DC gear motors + wheels, chassis
- Battery pack for motors (e.g., 4×AA) + switch
- Jumper wires; optional standoffs/zip ties

---
## Walkthrough — Step by Step (with explanations)

### 1) Power & ground
**Idea:** Separate motor power but share ground.
- Motor battery → L298N `+12V` and `GND`
- Pico 5V **not required**; power Pico via USB
- **Common GND**: connect Pico `GND` to L298N `GND`
**Notes & pitfalls:**
- Never power motors from Pico 3.3V.
- Double‑check polarity before switching on.

### 2) Pin map and first spin
**Idea:** Drive each side forward by setting inputs.
```python
from machine import Pin
import time

# EDIT pins to match your wiring
IN1, IN2 = Pin(10, Pin.OUT), Pin(11, Pin.OUT)  # Left
IN3, IN4 = Pin(12, Pin.OUT), Pin(13, Pin.OUT)  # Right

def stop():
    IN1.off(); IN2.off(); IN3.off(); IN4.off()

def forward():
    IN1.on();  IN2.off()
    IN3.on();  IN4.off()

def back():
    IN1.off(); IN2.on()
    IN3.off(); IN4.on()

stop(); time.sleep(1)
forward(); time.sleep(1.0)
stop()
```
**Notes & pitfalls:**
- If wheels spin backward, swap a motor’s leads **or** flip the logic.

### 3) Turns and simple choreography
**Idea:** Opposite wheel directions to pivot.
```python
def left():
    IN1.off(); IN2.on()   # left backward
    IN3.on();  IN4.off()  # right forward

def right():
    IN1.on();  IN2.off()
    IN3.off(); IN4.on()

# square path
for _ in range(4):
    forward(); time.sleep(1.2)
    right();   time.sleep(0.45)
stop()
```
**Notes & pitfalls:**
- Calibrate times for *your* floor and battery.

### 4) (Optional) PWM speed control
**Idea:** Use ENA/ENB with PWM for speed.
```python
from machine import PWM

ENA = PWM(Pin(8))   # if L298N EN jumpers are removed
ENB = PWM(Pin(9))
ENA.freq(1000); ENB.freq(1000)

def set_speed(pct):  # 0–100
    duty = int(pct/100 * 65535)
    ENA.duty_u16(duty)
    ENB.duty_u16(duty)
```
**Notes & pitfalls:**
- Some L298N boards have jumpers tying ENA/ENB high—remove them to use PWM.
- Start at 60–80% to overcome stall torque.

---
## Vocabulary
- **H‑bridge**: Circuit that lets you drive a motor forward/backward.
- **Common ground**: All modules share GND for a stable reference.
- **PWM**: Controls average power to motors for speed.
- **Stall**: Motor stopped while powered—draws highest current.

---
## Check your understanding
1) Why must Pico GND and L298N GND be connected?  
2) What are two ways to fix reversed wheel direction?  
3) What do `IN1..IN4` control on the L298N?  
4) Why might PWM be ignored on ENA/ENB?  
5) How do you calibrate a 90° turn without sensors?

---
## Try it: Mini-exercises
Program a **“drive square”** routine using your helpers and tuned timings.  
**Stretch goals:**
- Add `set_speed(pct)` and try 60%, 80%, 100%.
- Add a `dance()` that mixes forward/back/turns.

---
## Troubleshooting
- **One side doesn’t move** → Check that pair’s `IN` pins and motor wiring.  
- **Everything brown‑outs** → Motor battery is low or wrong voltage.  
- **No PWM effect** → ENA/ENB jumpers still installed; remove them.  
- **Wobbly straight line** → Slight motor mismatch; reduce speed or micro‑adjust timings.

---
## Next up
**[04 — PicoBot Maze Explorer (Drive Basics)](../Labs/04-picobot-maze-explorer.md)**
