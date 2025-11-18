# 04 — PicoBot: Drive with L298N (No Sensors)

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/picobot1.jpeg" width="400" >

> ### Quick Summary  
> **Level:** 04 • **Time:** 60–90 min
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md) & [03 — Pico Breadboarding](./03-pico-breadboarding.md)  
> **Hardware:** Raspberry Pi Pico, L298N motor driver, 2 DC motors + chassis, motor battery pack (pre-wired), jumper wires  
> **You’ll practice:** wiring driver inputs, sharing common ground, mapping GPIO pins, writing drive helpers, timed turns, optional PWM speed control  

> **Learn → Try → Do:** Learn the patterns here, practice with mini-exercises, then **Do** the matching PicoBot Lab.

# Why This Matters

If you can make your robot drive on purpose, you can make it do… almost anything. In this guide you’ll wire the Pico to the L298N **inputs** (the “control pins”) and write simple functions like `forward()`, `back()`, `left()`, and `right()`. These drive skills are the base for your later maze, sensor, and autonomy challenges.

---

## What you’ll learn

- Read the wiring plan for Pico ↔ L298N safely  
- Connect **6 control pins + 1 ground** between Pico and L298N  
- Map Pico GPIO numbers to motor driver pins in code  
- Write and reuse drive helpers (`forward`, `back`, `left`, `right`, `stop`)  
- Use timing to move a set distance or turn about 90°  
- (Optional) Use ENA/ENB with PWM to control speed  

## Setup

_Classroom default: **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**._

1. Connect your **Pico** to the Raspberry Pi 500 using a USB cable.  
2. Open **Thonny** → `Tools ▸ Options ▸ Interpreter`  
   - Set Interpreter to **MicroPython (Raspberry Pi Pico)**.  
   - If Thonny offers to install MicroPython, say **Yes** and follow the prompts.  
3. Create a new file and save it as:  
   `~/Documents/CodeCreate/picobot_drive.py`  
4. Make sure your **robot’s wheels are off the table** (up on a box or stand) for first tests.  
5. Hardware status for this guide:
   - The **L298N power** and **motors** are **already wired for you**.
   - You will only connect:
     - 6 signal pins: `ENA`, `IN1`, `IN2`, `IN3`, `IN4`, `ENB`  
     - 1 **GND** between Pico and L298N  
     - 1 **POWER** between Pico and L298N  

⚠️ **Safety notes**

- Pico GPIO pins are **3.3V**. Do **not** connect your Pico to any **12V** or motor power pins.  
- L298N logic inputs accept 3.3V, so Pico pins can safely drive `IN1–IN4`, `ENA`, `ENB`.  
- Always share a **common ground**: Pico `GND` ↔ L298N `GND`.

---

## Walkthrough — Step by Step (with explanations)

### 1) Wire the Pico to the L298N (signals only)

**Idea:** The motors and battery are already wired. You only add the **control wires** from the Pico to the L298N plus a **shared ground** so they can “speak the same voltage language.”

#### Wiring plan
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/picobot2.jpeg" width="400" >
Your teacher may give you a specific pin map. Here is a **suggested** map:

| Pico GPIO | L298N Pin | Role      |
|----------:|-----------|-----------|
| GP10      | IN1       | Left motor input 1 |
| GP11      | IN2       | Left motor input 2 |
| GP12      | IN3       | Right motor input 1 |
| GP13      | IN4       | Right motor input 2 |
| GP14      | ENA       | Left enable / speed |
| GP15      | ENB       | Right enable / speed |
| any GND   | GND       | Common ground      |

> If your kit uses **different GPIOs**, that’s okay—just update the pin numbers in code.
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/Pico-L298N.jpg" width="600" >

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot17.jpg" width="100" > <img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot19.jpg" width="100" > 
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot18.jpg" width="100" > <img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/PicoBot20.jpg" width="100" > 

#### Code: set up pin objects

In `picobot_drive.py`:

```python
from machine import Pin
import time

# === L298N pin mapping (EDIT if your wiring is different) ===
IN1 = Pin(10, Pin.OUT)   # Left motor input 1
IN2 = Pin(11, Pin.OUT)   # Left motor input 2
IN3 = Pin(12, Pin.OUT)   # Right motor input 1
IN4 = Pin(13, Pin.OUT)   # Right motor input 2

ENA = Pin(14, Pin.OUT)   # Left enable (on/off or PWM later)
ENB = Pin(15, Pin.OUT)   # Right enable (on/off or PWM later)

# Turn both sides on (full speed for now)
ENA.value(1)
ENB.value(1)

print("Pin setup complete.")
```

Run the file once. You shouldn’t see motion yet, but you should **not** see errors in the Shell.

**Notes & pitfalls**

- Make sure **Pico GND** is connected to **L298N GND**. If not, your pins may do nothing or behave strangely.  
- Double-check that your `IN1–IN4` wires match the left/right motor sides your teacher specified.  

---

### 2) Make it move: stop, forward, back

**Idea:** Driving a DC motor is just about setting pairs of inputs **high/low**. We’ll write helper functions so you don’t repeat the same code everywhere.

Add this below your pin setup:

```python
def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


def forward():
    # Left motor forward
    IN1.value(1)
    IN2.value(0)

    # Right motor forward
    IN3.value(1)
    IN4.value(0)


def back():
    # Left motor backward
    IN1.value(0)
    IN2.value(1)

    # Right motor backward
    IN3.value(0)
    IN4.value(1)


# --- quick test ---
print("Forward test...")
stop()
time.sleep(1)

forward()
time.sleep(1.0)

stop()
print("Done.")
```

Run the script:

- The wheels should **pause**, then drive **forward** for ~1 second, then stop.

**Anatomy / Breaking it down**

- Each motor uses **two inputs**:
  - `10/11` control the **left motor** direction.  
  - `12/13` control the **right motor** direction.  
- Only **one** of the pair should be `1` at a time for normal forward/back motion.  
- `stop()` sets **all inputs to 0** so the motors coast or brake (depending on your driver).

**Common mistakes**

- Wheels spin **backward**:  
  - Either swap the two motor wires on that side **or** swap the `1` and `0` values in your `forward()` function for that motor.
- Robot moves as soon as you plug it in:  
  - You might be calling `forward()` at the top of the file. Make sure you call `stop()` first and only test motion in a clear area.

---

### 3) Turn and choreograph a pattern

**Idea:** To turn in place, you can run one side forward and the other backward. With **timing**, you can make a “square” or other shapes.

Add turning helpers:

```python
def left():
    # Left motor backward, right motor forward
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right():
    # Left motor forward, right motor backward
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)
```

Now add a simple pattern at the bottom of the file:

```python
# --- square pattern test ---
stop()
time.sleep(1)

FORWARD_TIME = 1.2   # seconds; adjust for your robot
TURN_TIME = 0.45     # seconds; adjust for ~90 degrees

for _ in range(4):
    forward()
    time.sleep(FORWARD_TIME)

    right()
    time.sleep(TURN_TIME)

stop()
print("Square pattern complete.")
```

**Notes & pitfalls**

- These times are just **starting guesses**. Your battery level, floor type, and wheel friction all change the actual distance and turn angle.
- If your robot **overshoots** the turn, lower `TURN_TIME`. If it **undercuts**, increase it slightly.
- Always test new patterns with the wheels **off the table** first to confirm functions work as expected.

---

### 4) (Optional) Add speed control with PWM

**Idea:** `ENA` and `ENB` are “enable” pins. With **PWM** (Pulse-Width Modulation), you can run the motors slower while still giving them short bursts of full power.

> This step assumes the small jumpers on ENA/ENB have been **removed** and that ENA/ENB are wired to Pico GPIO pins.

Replace the `ENA` and `ENB` setup with PWM:

```python
from machine import PWM

# Replace previous ENA/ENB definitions with PWM versions
ENA = PWM(Pin(14))
ENB = PWM(Pin(15))

ENA.freq(1000)  # 1 kHz is a common motor PWM frequency
ENB.freq(1000)


def set_speed(percent):
    """Set speed for both motors: 0-100%."""
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100

    duty = int(percent / 100 * 65535)

    ENA.duty_u16(duty)
    ENB.duty_u16(duty)


# Example: slow forward
set_speed(60)
forward()
time.sleep(1.5)
stop()
```

You can call `set_speed(60)`, `set_speed(80)`, or `set_speed(100)` before moving.

**Notes & pitfalls**

- Some L298N boards ship with ENA/ENB jumpers installed; if they are still in place, your PWM won’t change the speed. The board is forcing “always on.”  
- If your robot **won’t start moving** at a low speed, increase to 60–80%. Motors need enough power to overcome friction (“stall torque”).  
- If you see a **huge slowdown** or stuttering when lowering speed, your battery might be weak.

---

## Vocabulary

- **L298N** – A motor driver board that can control two DC motors forward and backward.  
- **H-bridge** – An electronic circuit that lets you reverse the direction of a DC motor.  
- **Enable pin (ENA/ENB)** – Turns a motor channel on/off and can be used with PWM for speed.  
- **Common ground** – When all parts share the same `GND` reference so signals line up correctly.  
- **PWM (Pulse-Width Modulation)** – A way to change speed by turning power on and off very quickly.  
- **Duty cycle** – The percentage of time the PWM signal is “on” during each cycle.  
- **Calibration** – Adjusting timing or values so your robot moves how you expect (e.g., real 90° turns).  

---

## Check your understanding

1. **Why is the common ground important?**  
   The motors already spin with the battery—why do we still need to connect Pico `GND` to L298N `GND`?

2. **Pin logic:**  
   In the `forward()` function, why do we set `IN1=1, IN2=0` for a motor instead of setting both to `1`?

3. **Predict the motion pattern:**  
   Look at this snippet:
   ```python
   set_speed(80)
   forward()
   time.sleep(1)
   left()
   time.sleep(0.4)
   forward()
   time.sleep(1)
   stop()
   ```
   Assuming the times are calibrated, describe how the robot moves on the floor (roughly).

4. **Bug hunt – what’s wrong here?**
   ```python
   def back():
       IN1.value(1)
       IN2.value(0)
       IN3.value(0)
       IN4.value(1)
   ```
   a) What will this actually do?  
   b) How should you fix it so the robot truly moves backward?

5. **PWM concept:**  
   If `set_speed(40)` feels like the motors don’t move at all, what is one likely reason and how could you fix it?

6. **Safety check:**  
   Why do we test new drive code with the wheels lifted off the table first, even if we think the code is correct?

---

## Try it: Mini-exercises

Try these small tasks in your `picobot_drive.py` file (or a copy). Each can be done in a few minutes.

1. **Drive helper with time:**  
   Write a function `drive_forward_ms(ms)` that drives forward for `ms` milliseconds and then stops. (Hint: convert ms to seconds with `ms / 1000`.)

2. **Back-up helper:**  
   Add a `back_up_and_stop(ms)` that backs up for a short time and then stops. Use it to create a “bump then reverse” pattern.

3. **Simple menu in the Shell:**  
   At the bottom of your file, add:
   ```python
   while True:
       choice = input("Command (w/a/s/d/q): ")
       if choice == "w":
           forward()
       elif choice == "s":
           back()
       elif choice == "a":
           left()
       elif choice == "d":
           right()
       elif choice == "q":
           stop()
           break
       else:
           print("Unknown command")

       time.sleep(0.5)
       stop()
   ```
   Experiment with driving the robot by typing `w`, `a`, `s`, `d`, `q` in the Shell.

4. **Tune your square:**  
   Adjust `FORWARD_TIME` and `TURN_TIME` until your robot drives a square that ends close to its starting point. Record your times in a comment.

5. **Slow vs fast:**  
   Use `set_speed()` to compare a “slow square” (e.g., 50%) and a “fast square” (e.g., 100%). Which one tracks straighter?

### Stretch

- **Speed ramp:**  
  Make a function that slowly ramps speed from 40% → 100% while driving forward, then slows back down to 40%.

- **Pattern list:**  
  Store a sequence of moves in a list, like:
  ```python
  pattern = [
      ("forward", 1.0),
      ("right", 0.4),
      ("forward", 1.0),
      ("left", 0.4),
  ]
  ```
  Loop over the pattern and call the correct function for each step.

- **Measure a meter:**  
  Use a tape measure and timing to find how long your robot needs to drive to go about 1 meter. Save that as a constant (e.g., `ONE_METER_TIME`).

---

## Troubleshooting

- **Symptom: One side of the robot does not move at all.**  
  → **Fix:** Check that side’s `IN` pins and the `ENA`/`ENB` pin are wired to the correct Pico GPIOs. Confirm those pins are set as `Pin.OUT` (or PWM) in your code.

- **Symptom: Robot only turns in one direction, never straight.**  
  → **Fix:** One motor might be wired backward or your `forward()` logic is mismatched. Try swapping that motor’s wires or flip the `1`/`0` pattern for that side in `forward()`.

- **Symptom: PWM changes have no effect on speed.**  
  → **Fix:** Check if ENA/ENB jumpers are still installed on the L298N. If they are, PWM is being overridden—remove the jumpers (ask your teacher first).

- **Symptom: Thonny shows `NameError: name 'forward' is not defined`.**  
  → **Fix:** Make sure you defined `def forward():` **above** where you call it, and check the spelling of the function name.

- **Symptom: Robot suddenly slows down or behaves randomly.**  
  → **Fix:** Your motor battery might be low. Replace or recharge batteries and test again.

---

## Next up

**[04 – PicoBot Maze Explorer (Drive Basics)](../Labs/04-picobot-maze-explorer.md)**
