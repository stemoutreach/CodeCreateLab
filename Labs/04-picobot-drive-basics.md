# 04 — PicoBot Drive Basics (No Sensors)

> ### Quick Summary
> **Level:** 04 • **Time:** 60–90 min  
> **Prereqs:** [Guide: 04 — PicoBot: Drive with L298N (No Sensors)](../Guides/04-picobot.md)  
> **Hardware:** Raspberry Pi 500 + Pico + **L298N** + 2× DC motors + chassis + battery  
> **You’ll practice:** Motor polarity, forward/turn/stop helpers, **PWM** speed control, **trim**, timed square

# Why This Matters
Before sensors and autonomy, your robot needs **predictable motion**. In this lab you’ll verify wiring, create simple drive helpers, add PWM speed control with trim, and prove it by tracing a timed **square**.

> **Learn → Try → Do**  
> - **Learn** the patterns in the Guide  
> - **Try** tiny tests in the Guide  
> - **Do** the full drive routine here in the Lab

---
# What You’ll Build
A drive program with small, reusable functions that:
- Start/stop safely
- Drive forward with **PWM** (plus **LEFT/RIGHT trim** to correct drift)
- Turn left/right in place
- Trace a **square** using timing

# Outcomes
By the end you can:
- Map Pico pins to L298N **ENA/IN1/IN2** and **ENB/IN3/IN4**
- Implement **forward**, **turn_left**, **turn_right**, and **stop**
- Apply **PWM trim** and tune duty cycles
- Build a **timed square** routine and adjust timing for your bot

# Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**  
- Connect the **Pico** via micro-USB (wheels **off the table** for first tests)  
- Thonny → **Tools ▸ Options ▸ Interpreter** → **MicroPython (Raspberry Pi Pico)**; flash UF2 if prompted  
- Create `picobot_drive.py` in `~/Documents/CodeCreate/`, then **Run ▶** and watch the **Shell**

**Power & safety**  
- Keep motor power **off** during wiring.  
- Share **GND** between Pico and the L298N/motor battery.  
- Start with **low duty** (e.g., 40–60%) and lift wheels for first runs.

---
# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/04-picobot-drive-basics/STUDENT_START.md)**.

## 1) Wire & name your pins (5–8 min)
Confirm your L298N mapping and put it into named constants. Example (adjust to match your wiring):
- **Left motor**: ENA=GP2 (PWM), IN1=GP3, IN2=GP4  
- **Right motor**: ENB=GP5 (PWM), IN3=GP6, IN4=GP7

## 2) Low-level wheel helpers (8–12 min)
Write **single-purpose** helpers:
- `set_left(direction, duty)` and `set_right(direction, duty)` where `direction` is `1` (forward) or `-1` (reverse).  
- Stop = both IN pins low + duty 0.

## 3) Drive primitives (6–10 min)
- `forward(duty)` → both wheels forward (with trim).  
- `turn_left(duty)` / `turn_right(duty)` → in-place turns using opposite wheel directions.

## 4) Speed trim (5–10 min)
Add `LEFT_TRIM` and `RIGHT_TRIM` (e.g., `-0.10..+0.10`) and apply them in `forward`. Tune until the robot tracks straight.

## 5) Timed square (10–15 min)
Implement `drive_square(side_ms=1200, turn_ms=700, duty=0.6)`:
1) `forward(duty)`; `sleep_ms(side_ms)` → **stop** → short pause  
2) `turn_right(duty)`; `sleep_ms(turn_ms)` → **stop** → short pause  
3) Repeat 1–2 four times; then **stop**.

## 6) Demo & iterate (5–8 min)
- Start with wheels up; then move to a safe test area.  
- Adjust `duty`, `side_ms`, and `turn_ms` to tighten the square.

---
# Skeleton Starter
Use this **single** starter. Fill each **TODO**. No full solutions here.

```python
# 04 — PicoBot Drive Basics (No Sensors)

from machine import Pin, PWM
from time import sleep_ms

# === Pin map (EDIT to match your wiring) ===
ENA = 2   # PWM (left enable)
IN1 = 3   # left dir 1
IN2 = 4   # left dir 2

ENB = 5   # PWM (right enable)
IN3 = 6   # right dir 1
IN4 = 7   # right dir 2

# === Tuning ===
BASE_DUTY = 0.6      # 0.0..1.0
LEFT_TRIM = 0.00     # + makes left faster; - slower
RIGHT_TRIM = 0.00    # + makes right faster; - slower

# === Hardware ===
pwm_left = PWM(Pin(ENA)); pwm_left.freq(1000)
pwm_right = PWM(Pin(ENB)); pwm_right.freq(1000)
in1 = Pin(IN1, Pin.OUT); in2 = Pin(IN2, Pin.OUT)
in3 = Pin(IN3, Pin.OUT); in4 = Pin(IN4, Pin.OUT)

def duty_to_u16(frac: float) -> int:
    """Convert 0.0..1.0 to 0..65535."""
    frac = max(0.0, min(1.0, float(frac)))
    return int(frac * 65535)

def stop():
    """Coast/stop both motors."""
    in1.value(0); in2.value(0)
    in3.value(0); in4.value(0)
    pwm_left.duty_u16(0); pwm_right.duty_u16(0)

def set_left(direction: int, duty: float):
    """direction: 1 forward, -1 reverse"""
    # TODO: set IN1/IN2 for direction and apply PWM duty
    pass

def set_right(direction: int, duty: float):
    """direction: 1 forward, -1 reverse"""
    # TODO: set IN3/IN4 for direction and apply PWM duty
    pass

def forward(duty=BASE_DUTY):
    """Forward with trim applied."""
    # TODO: compute left = duty + LEFT_TRIM, right = duty + RIGHT_TRIM
    # set_left(1, left); set_right(1, right)
    pass

def turn_left(duty=BASE_DUTY):
    """In-place left turn."""
    # TODO: left reverse, right forward
    pass

def turn_right(duty=BASE_DUTY):
    """In-place right turn."""
    # TODO: left forward, right reverse
    pass

def drive_square(side_ms=1200, turn_ms=700, duty=BASE_DUTY):
    """Drive a timed square and stop."""
    # TODO: loop 4 times: forward->sleep->stop->pause->turn_right->sleep->stop
    pass

def main():
    print("PicoBot Drive Basics — wheels OFF table for first run!")
    try:
        stop()
        # Quick spin test (wheels up)
        # TODO: call forward(0.5); sleep_ms(400); stop(); then turn_right(0.5); sleep_ms(400); stop()
        
        # Place robot down, then try the square:
        # TODO: drive_square()
    finally:
        stop()
        print("Stopped.")

if __name__ == "__main__":
    main()
```

---
# Demo / Submission Checklist
- [ ] Correct **pin map** matches your wiring (comment updated)  
- [ ] **forward/turn/stop** helpers work and are used (no copy-paste everywhere)  
- [ ] **Speed trim** applied in `forward` (values documented)  
- [ ] Robot traces a **square** on the floor (timings tuned for your bot)  
- [ ] Safe run: wheels up for first tests; clean **stop()** in `finally`

---
# Extensions (pick one)
- **Gentle start/stop:** ramp duty up/down to reduce jerk.  
- **Differential turn:** try arc turns (one wheel slow, one fast) and compare to in-place turns.  
- **Calibration log:** print measured side/turn timings you found; save as comments.  
- **Reverse escape:** add a `back_up(ms)` and try a square in reverse.

---
# Troubleshooting
- **Both wheels spin same way but robot turns** → Apply **LEFT/RIGHT_TRIM** until it tracks straight.  
- **One wheel backward** → Swap that motor’s **IN1/IN2** or change your direction bits.  
- **No movement** → Check **GND common**, motor battery, and that **ENA/ENB** are PWM pins.  
- **Launches too fast** → Lower `BASE_DUTY` to ~0.4 for first tests.

---
# Reflection
What trim values worked for your floor and batteries? How would your square routine change with sensor feedback?

---
# Next Up
When your drivetrain is solid, you’re ready for sensing (e.g., ultrasonic) or navigation aids. For now, commit your tuned timings.
