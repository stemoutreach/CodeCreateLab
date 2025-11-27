
# 04 — PicoBot — Drive Basics

> ### Quick Summary
> **Level:** 04 • **Time:** 40–60 min  
> **Prereqs:** [Guide: 03 — Pico + Breadboarding](../Guides/03-pico-breadboarding.md), [Guide: 04 — PicoBot](../Guides/04-picobot.md)  
> **Hardware:** Raspberry Pi Pico, L298N motor driver, 2× DC gear motors, battery pack, chassis/wheels  
> **You’ll practice:** motor wiring check, L298N enable/direction, PWM speed control, trim/balance, safe stop

# Why This Matters
Driving is the foundation for every mobile robot behavior you’ll write later (maze, line following, pickup tasks). Solid motor control, correct pin setup, and safe-stops now will make later sensor labs much easier.

---
## What you’ll learn
- Map Pico GPIO pins to L298N inputs and enables
- Generate PWM on `ENA/ENB` for speed control
- Implement `forward()`, `turn_left()`, `turn_right()`, `stop()`
- Calibrate left/right **trim** so the robot drives straight
- Drive a timed **square route** as a functional test
- Apply safe-stop patterns to avoid runaway motors

## Setup
> **Classroom default:** Raspberry Pi 500 + **Thonny**  
> In Thonny choose **MicroPython (Raspberry Pi Pico)** and save code on the Pico as **`main.py`** so it runs on boot.

1. Review [Guide: 04 — PicoBot](../Guides/04-picobot.updated.md) for the pin map and wiring diagram.  
2. Mount the Pico + L298N + motors and double‑check polarity on the motor terminals.  
3. Keep wheels **off the table** for first power‑on tests.

---
# Steps
> 🆘 **Need a hint?** See the scaffold and tips in:  
> `../Example_Code/04-picobot-drive-basics/STUDENT_START.md`

## 1) Verify wiring & create your project
- Confirm your pin choices (example from the guide): `ENA=GP2`, `ENB=GP3`, `IN1=GP4`, `IN2=GP5`, `IN3=GP6`, `IN4=GP7`.  
- In Thonny, create a new file named **`main.py`** on the Pico.

**Discovery (pseudo-steps):**
- Set all IN pins **LOW**; set PWM on EN pins to **0** duty → wheels do **not** move.
- Nudge duty to a low value → confirm wheels start turning smoothly.

## 2) Implement basic motion helpers
You will create:
- `stop()` — cut power to both motors (all IN pins low; EN duty 0).  
- `forward(ms)` — both sides forward for `ms` milliseconds, then `stop()`.  
- `turn_left(ms)` — left reverse, right forward; pivot left, then `stop()`.  
- `turn_right(ms)` — mirror of `turn_left`.

> Keep **PWM_FREQ ~ 1 kHz** and start **duty ~ 55–70%** of 65535 (MicroPython).

## 3) Add trim & make it drive straight
- Create `set_trim(left, right)` to scale PWM on each side (e.g., 1.00 vs 0.95).  
- Test a 1‑meter forward drive; tweak trim until it’s straight.

## 4) Demo route — the timed square
- Write `demo_square(side_ms=1000, turn_ms=500)` that calls `forward()` then `turn_right()` **four** times.  
- Tune `side_ms`/`turn_ms` until you get clean 90° corners.

## 5) Safety & cleanup
- Wrap your `main()` loop with `try/except KeyboardInterrupt` and call `stop()` in `finally:` so motors always stop.

---
## Skeleton Starter (paste into `main.py` and complete the TODOs)
```python
from machine import Pin, PWM
from time import sleep_ms

# === PINS: update to match your wiring ===
ENA_PIN = 2   # PWM enable (left)
ENB_PIN = 3   # PWM enable (right)
IN1_PIN = 4   # Left IN1
IN2_PIN = 5   # Left IN2
IN3_PIN = 6   # Right IN3
IN4_PIN = 7   # Right IN4

PWM_FREQ = 1000
PWM_DUTY = 65000     # ~70% of 65535 is a good start
TRIM_LEFT = 1.00
TRIM_RIGHT = 1.00

ena = PWM(Pin(ENA_PIN)); enb = PWM(Pin(ENB_PIN))
ena.freq(PWM_FREQ); enb.freq(PWM_FREQ)
in1 = Pin(IN1_PIN, Pin.OUT); in2 = Pin(IN2_PIN, Pin.OUT)
in3 = Pin(IN3_PIN, Pin.OUT); in4 = Pin(IN4_PIN, Pin.OUT)

def set_trim(left: float, right: float):
    """TODO: store trim multipliers to balance left/right speed."""
    # TODO: assign to TRIM_LEFT/TRIM_RIGHT, clamped to a reasonable range (0.0..1.2)
    pass

def _drive_raw(left_duty: int, right_duty: int):
    """Low-level direction & PWM. +forward, -reverse, 0 stop."""
    # TODO: set (in1,in2) and (in3,in4) based on sign of each duty
    # TODO: apply trim to absolute duty and write via duty_u16()
    pass

def stop():
    """TODO: immediately stop both sides."""
    pass

def forward(ms: int):
    """TODO: drive forward for ms milliseconds, then stop."""
    pass

def turn_left(ms: int):
    """TODO: pivot left for ms milliseconds (left backward, right forward)."""
    pass

def turn_right(ms: int):
    """TODO: pivot right for ms milliseconds (left forward, right backward)."""
    pass

def demo_square(side_ms=1000, turn_ms=500):
    for _ in range(4):
        forward(side_ms)
        sleep_ms(250)
        turn_right(turn_ms)
        sleep_ms(250)

def main():
    try:
        # Example: slight trim if your bot veers right
        # set_trim(1.00, 0.95)
        demo_square()
    except KeyboardInterrupt:
        pass
    finally:
        stop()

if __name__ == "__main__":
    main()
```

---
## Testing & troubleshooting
- **Wheels don’t move:** check ENA/ENB PWM duty. Many motors need a minimum duty to overcome stiction.  
- **Drifts right/left:** adjust `set_trim()` (e.g., 1.00 vs 0.95).  
- **Jerky motion:** lower PWM duty or check battery voltage.  
- **Keeps running after error:** confirm `stop()` is called in `finally:` block.

## Submission checklist
- [ ] Implemented `stop`, `forward`, `turn_left`, `turn_right`, and `set_trim`  
- [ ] Robot drives a reasonably straight line with trim applied  
- [ ] Timed square completes with ~90° turns  
- [ ] Code formatted and commented (pin map at top)  
- [ ] Safety: `try/except/finally` pattern with `stop()`

## Rubric
- **Must (Pass):** forward/turn/stop work; safe stop; square route completes  
- **Should (Good):** trim applied for straight driving; clean 90° corners  
- **Stretch (Great):** parameterized speeds; add `turn_angle()` that estimates ms per degree

## Extensions (optional)
- Add a `drive(distance_cm, speed)` and `turn(angle_deg)` using your timing calibration.  
- Experiment with smoother turns by using differential PWM instead of full pivots.

---
**No spoilers:** Full reference code is available for coaches in `../Example_Code/04-picobot-drive-basics/SOLUTION.md`. Students should use the `STUDENT_START.md` and TODOs above.
