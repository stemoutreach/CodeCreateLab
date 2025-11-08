# 02.5 — Sense HAT Advanced — Mission Dashboard

> ### Quick Summary
> **Level:** 02.5 • **Time:** 45–75 min  
> **Prereqs:** [Lab: 02 — Sense HAT Basics](../Labs/02-sense-hat-basics.md), [Guide: 02 — Sense HAT](../Guides/02-sense-hat.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT  
> **You’ll practice:** function design, joystick callbacks, lists/state, timing, simple math, clean shutdown

# Why This Matters
Real devices switch between **modes** and keep running while you interact. This lab turns your Sense HAT into a tiny dashboard with three modes, a joystick UI, and clean exit behavior.

> **Learn → Try → Do**  
> - **Learn** & **Try** in the Guide  
> - **Do** here in the Lab

---
# What You’ll Build
A **Mission Dashboard** that cycles between three modes:
1) **Orientation** — Arrow shows which way “up” is (pitch/roll).  
2) **Environment** — Scroll temperature, humidity, and pressure (color-coded).  
3) **Compass** — Center dot + red “needle” pointing toward magnetic north.

# Outcomes
By the end you can:
- Structure a program into **helper functions** that each do one job
- Use a **joystick callback** to cycle a mode index
- Maintain a simple **state machine** (list of modes, current index)
- Handle **Ctrl‑C** and clear the LED matrix on exit

# Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**  
- Open **Thonny** (Menu → Programming → Thonny)  
- Create `mission_dashboard.py` in `~/Documents/CodeCreate/`, then **Run ▶** and view output in the **Shell**

**If Sense HAT support isn’t installed on your Pi:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y sense-hat
sudo reboot
```
Optional: enable I2C in `raspi-config` if needed.

Quick test in Python:
```python
from sense_hat import SenseHat
SenseHat().show_message("Hello!")
```

---
# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/02-5-sense-hat-advanced/STUDENT_START.md)**.

## 1) Plan your modes (2–3 min)
- Decide **colors** and basic **8×8 arrow patterns** (up/down/left/right).  
- Modes list: `["orientation", "environment", "compass"]` and a `mode_index = 0`.

## 2) Make helper functions (10–15 min)
Create stubs (no heavy logic yet):
- `draw_orientation_arrow(sense)`: choose a pattern based on pitch/roll and display it.  
- `scroll_environment(sense)`: read T/H/P and show 3 short messages.  
- `draw_compass(sense, heading)`: draw a center pixel and a red “needle” pixel.

> Keep each function **short** and **single-purpose**.

## 3) Wire the joystick (5–7 min)
- Write `on_joystick(event)` so **center press** advances the mode index.  
- Attach with `sense.stick.direction_any = on_joystick` (or similar).

## 4) Main loop (5–10 min)
- Based on `m = MODES[mode_index]`, call the matching helper.  
- Use a small sleep (e.g., `time.sleep(0.1)`).  
- On **Ctrl‑C**, **clear** the matrix and print “Goodbye!”.

## 5) Tune & demo (5–10 min)
- Adjust arrow thresholds/rotation, scroll speed, and colors.  
- Demo all three modes and a clean exit.

---
# Skeleton Starter
Use this **single** starter. Fill each **TODO**. No full solutions here; see the helper only if truly stuck.

```python
from sense_hat import SenseHat, ACTION_PRESSED
import time, math

sense = SenseHat()
sense.clear()
# Optional: set rotation if your Pi orientation differs
# sense.set_rotation(180)

# Colors
R = (255, 0, 0); G = (0, 255, 0); B = (0, 0, 255); W = (255,255,255); K = (0,0,0)

# TODO: define simple 8x8 arrow patterns: ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT
# Hint: use a list of 64 color tuples, row by row

MODES = ["orientation", "environment", "compass"]
mode_index = 0

def draw_orientation_arrow(sense):
    """Show an arrow based on pitch/roll."""
    # TODO: get orientation (pitch, roll); choose a pattern; set pixels
    pass

def scroll_environment(sense):
    """Scroll T/H/P with colors."""
    # TODO: read temperature/humidity/pressure; scroll messages with colors
    pass

def draw_compass(sense, heading):
    """Draw a center dot and a red needle pixel toward heading degrees."""
    # TODO: convert degrees to a small vector; clamp to 0..7; set pixels
    pass

def on_joystick(event):
    """Advance mode on center press."""
    global mode_index
    # TODO: if event.action == ACTION_PRESSED and event.direction == "middle": advance index and clear
    pass

def main():
    # Attach joystick callback
    # TODO: sense.stick.direction_any = on_joystick
    try:
        while True:
            m = MODES[mode_index]
            if m == "orientation":
                draw_orientation_arrow(sense)
            elif m == "environment":
                scroll_environment(sense)
            else:
                # TODO: get compass heading and draw
                pass
            time.sleep(0.1)
    except KeyboardInterrupt:
        sense.clear()
        print("Goodbye!")

if __name__ == "__main__":
    main()
```

---
# Demo / Submission Checklist
- [ ] Orientation arrow responds sensibly to movement/tilt  
- [ ] Environment mode scrolls **T/H/P** with your chosen colors  
- [ ] Compass shows a center pixel and a rotating **red** needle  
- [ ] Joystick **center** cycles modes; **Ctrl‑C** clears LEDs and exits cleanly

---
# Extensions (choose one)
- **CSV logging:** `timestamp,t,h,p,heading` once per second.  
- **Accelerometer meter:** turn the 8×8 matrix into a bar showing |a|.  
- **Threshold alert:** flash **red** if temp exceeds a limit.

---
# Troubleshooting
- **No joystick events** → Ensure callback is set; keep your main loop running.  
- **Compass “drifts”** → Move away from magnets/metal; try a slow figure‑8 calibration.  
- **Wrong arrow** → Tune thresholds or rotation; verify your 8×8 lists are 64 items.

---
# Reflection
Which mode needed the most tuning? What UX change would help most on an 8×8 display?

---
# Next Up
Continue to **[03 — Pico Breadboard Lab](../Labs/03-pico-breadboard-lab.md)**.
