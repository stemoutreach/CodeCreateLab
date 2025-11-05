---
title: Sense HAT Basics — Weather Warning Light
level: 02
estimated_time: 35–60 min
difficulty: Beginner
prereqs:
  - Guide: [02 – Sense HAT](../Guides/02-sense-hat.md)
rubric:
  - ✅ Must: Read temperature (°C) and humidity (%) from Sense HAT
  - ✅ Must: Print readings and update LED color each cycle
  - ✅ Must: Thresholds come from user input; runs until Ctrl-C
  - ⭐ Stretch: Icon pattern, CSV logging, joystick clear, or smoothing offset
---

# Goal
Build a **Weather Warning Light**. Every few seconds, read **temperature** and **humidity**.  
If it’s **too hot** OR **too dry**, flash **red**; otherwise show **green**.

# What you’ll practice
- Importing and initializing `SenseHat`
- Reading temp/humidity and labeling units (°C, %)
- Simple decision logic → LED color feedback
- Loops, user input, and basic debugging

# Materials
- Raspberry Pi with Raspberry Pi OS
- Sense HAT attached and seated
- Power supply, keyboard/mouse, display
- Terminal or Thonny
- Internet for installing packages (if needed)

# Steps

> 🆘 **Need a hint?** Read the minimal patterns in **`Example_Code/00-treasure-hunt-basic/STUDENT_START.md`** and adapt them to this lab’s tasks.

## 1) Get ready
- Ensure Sense HAT support is installed: `sudo apt install -y sense-hat`  
- Open a terminal or Thonny. (See the Guide’s setup & quick test snippet.)

> 📝 Tip: Sense HAT temperatures can read a bit high due to CPU heat; you may apply a small offset later.

## 2) Skeleton Starter
Use this starter and fill in the **TODOs** (don’t paste a full solution). There is **exactly one** starter.

```python
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def read_readings():
    """Return (temp_c, humidity_percent). Round for printing."""
    # TODO: read temperature (choose get_temperature or *_from_humidity)
    # TODO: read humidity with get_humidity()
    # TODO: round both to 1 decimal and return (t, h)
    return 0.0, 0.0

def show_status(temp, hum, t_limit, h_limit):
    """Set LED color and print a message based on limits."""
    # TODO: compute too_hot and too_dry using > and <
    # TODO: if unsafe, clear RED; else clear GREEN
    # TODO: print a readable status line including units and limits

print("Sense HAT — Weather Warning Light")
# TODO: ask user for high temp limit (°C) and low humidity limit (%) as float
t_limit = 0.0
h_limit = 0.0

try:
    while True:
        temp, hum = read_readings()
        show_status(temp, hum, t_limit, h_limit)
        time.sleep(2)   # adjust sample rate
except KeyboardInterrupt:
    sense.clear()
    print("Stopped. Stay safe!")
```

## 3) Read sensors (mini-guide)
- Temperature: `sense.get_temperature()` or `sense.get_temperature_from_humidity()`  
- Humidity: `sense.get_humidity()`  
- LED colors: `sense.clear(r, g, b)` (e.g., green `(0,255,0)`, red `(255,0,0)`)  
(See the Guide for examples of reading sensors and controlling LEDs.)

## 4) Decide What Happens (discovery)
Use this **checklist** and **brief pseudocode**—then implement in your starter. **No solution code here.**

**Checklist**
- [ ] Compare `temp` to `t_limit` (hot if `temp > t_limit`)
- [ ] Compare `hum` to `h_limit` (dry if `hum < h_limit`)
- [ ] Unsafe if **either** is true; safe otherwise
- [ ] Print values with **units** and limits (e.g., `T=24.3°C  H=44.7%`)
- [ ] Update LED color every cycle

**Pseudocode**
```
too_hot = temp > t_limit
too_dry = hum < h_limit
if (too_hot or too_dry):
    LED = RED
    print "WARNING ... "
else:
    LED = GREEN
    print "OK ..."
```

## 5) Test and tune
- Try different thresholds (e.g., `28°C` and `35%`).
- Make it obvious: slow the loop to ~2s; print each cycle.
- If your temperature seems high, apply a small negative offset to your reading and note it in your printout (e.g., `CPU_OFFSET = -3.0`).

## 6) Submission / Demo checklist
- [ ] Loops until **Ctrl-C** without crashing on normal input  
- [ ] Prints readings with **units** and sets LED **green** when safe, **red** when unsafe  
- [ ] Thresholds are **entered by the user**  

# Extensions (pick one)
- **Icon alert:** Instead of solid colors, show a red “!” or green “✓” with an 8×8 pixel pattern. (Use `set_pixels`.)
- **CSV logging:** Append `timestamp,temp_c,humidity_percent` to a file per loop.
- **Smoothing:** Keep a small moving average window (e.g., last 5 temps) before comparing.
- **Joystick quick-clear:** Press **middle** to clear to black for 1s, then resume. (Use `sense.stick.get_events()`).

# Troubleshooting
- **`ModuleNotFoundError: sense_hat`** → Install package on Raspberry Pi OS.  
- **No LED output** → Ensure program keeps running and the HAT is seated; try `sense.clear()` once at start.  
- **Odd temp values** → CPU heat can bias readings; slow your loop and/or subtract a small offset; consider `_from_humidity` vs `_from_pressure`.
- **`ValueError` on input** → Wrap `float(input(...))` in `try/except` and re-ask.

# Reflection
- What did you choose for your thresholds and why?  
- Where did you apply smoothing or offsets (if any), and how did it change behavior?

# Next up
Level up with **[02.5 – Sense HAT Advanced: Mission Dashboard](../Labs/02-5-sense-hat-advanced.md)** for joystick interactivity and IMU-driven displays.
