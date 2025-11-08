# 02 — Sense HAT Basics (Weather Warning Light)

> ### Quick Summary
> **Level:** 02 • **Time:** 35–60 min  
> **Prereqs:** [Guide: 02 — Sense HAT](../Guides/02-sense-hat.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT
> **You’ll practice:** reading sensors, loops, decisions, LED control, basic debugging

# Why This Matters

> **Learn → Try → Do**
> - **Learn** in the Guide
> - **Try** quick practice in the Guide
> - **Do** this Lab project
Real systems react to their environment. Using the Sense HAT’s sensors and LED matrix, you’ll build a tiny safety indicator and practice reading data, making decisions, and giving instant visual feedback—skills you’ll reuse in later labs.

---

# What You’ll Build
A loop that reads **temperature** (°C) and **humidity** (%) every few seconds and changes the LED matrix: **GREEN** when safe, **RED** when too hot or too dry. You’ll choose your own thresholds and print readable status lines to the console.

---

# Outcomes
By the end you can:
- Initialize and read `SenseHat` temperature and humidity
- Decide based on thresholds and update LED color accordingly
- Run a safe, stoppable loop and print labeled values with units

---

# Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**
- Open **Thonny** (Menu → Programming → Thonny)
- Create `weather_warning_light.py` in `~/Documents/CodeCreate/`, then **Run ▶** and view the **Shell**

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
sense = SenseHat()
sense.show_message("Hello!")
```

---

# Steps


> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/02-sense-hat-basics/STUDENT_START.md)**.

## 1) Plan (2–3 min)
Pick limits that make sense in your room (e.g., **temp high = 28°C**, **humidity low = 35%**). Decide your sampling interval (e.g., **2 seconds**).

## 2) Build / Prep (3–5 min)
- Verify the HAT’s LED matrix works: `python3 -c "from sense_hat import SenseHat; SenseHat().clear(0,255,0)"` then `clear(0,0,0)`.
- Create a project folder and file: `labs/02-sense-hat-basics/weather_warning_light.py`.

## 3) Code (8–12 min)
Start with a minimal structure and **leave TODOs** for your logic.

```python
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def read_readings():
    """Return (temp_c, humidity_percent). Round for printing."""
    # TODO: read temperature (get_temperature or get_temperature_from_humidity)
    # TODO: read humidity with get_humidity()
    # TODO: round to 1 decimal and return (t, h)
    return 0.0, 0.0

def show_status(temp, hum, t_limit, h_limit):
    """Set LED color and print a message based on limits."""
    # TODO: compute too_hot (temp > t_limit) and too_dry (hum < h_limit)
    # TODO: set LED: RED if unsafe else GREEN
    # TODO: print a readable line with units and limits

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

## 4) Discovery (checklist + pseudocode) (8–12 min)
**Checklist**
- [ ] Compare `temp` to `t_limit` (hot if `temp > t_limit`)
- [ ] Compare `hum` to `h_limit` (dry if `hum < h_limit`)
- [ ] Unsafe if **either** is true; safe otherwise
- [ ] Print values with **units** and limits (e.g., `T=24.3°C  H=44.7% (limits: 28°C/35%)`)
- [ ] Update LED color every cycle

**Pseudocode (guide, not code)**
```
too_hot = temp > t_limit
too_dry = hum < h_limit
if (too_hot or too_dry):
    LED = RED
    print "WARNING — too hot or too dry"
else:
    LED = GREEN
    print "OK — within limits"
```

## 5) Test (3–5 min)
- Try multiple thresholds; slow sampling to 2–3s to observe changes.
- Sanity-check print format and the LED reaction as values cross limits.

## 6) Iterate (2–3 min)
- If temps read high (CPU heat), try a constant offset (e.g., `temp -= 3.0`) and **label it** in your output.
- Consider switching to `get_temperature_from_humidity()` and compare readings.

---

# Skeleton Starter (start here)
Use the code skeleton in **Step 3** or the starter file in **Example_Code/02-sense-hat-basics/** (no full solutions—focus on TODOs).

```python
# Tip: keep helper functions small; return values, don't print inside sensor reads.
```

---

# Demo / Submission Checklist
- [ ] Loop runs until **Ctrl-C** and exits cleanly (LED cleared)
- [ ] Console prints labeled values with **units** and chosen **limits**
- [ ] LED shows **GREEN** when safe, **RED** when too hot or too dry
- [ ] Thresholds are **entered by the user** (not hard-coded)

---

# Extensions (choose one)
- **Icon alert:** Render a red “!” or green “✓” (8×8) instead of solid color.
- **CSV logging:** Append `timestamp,temp_c,humidity_percent` each cycle.
- **Smoothing:** Use a moving average (e.g., last 5 temps) before decision.
- **Joystick quick-clear:** Middle press clears LED to black for 1s, then resumes.

---

# Troubleshooting
- **`ModuleNotFoundError: sense_hat`** → Install package; run on Raspberry Pi OS (not your laptop).  
- **No LED output** → Ensure program loops; HAT seated; try `sense.clear()` at start.  
- **Numbers seem high** → CPU warms sensors; slow the loop and/or subtract a small offset.  
- **`ValueError` on input** → Wrap `float(input())` in `try/except` and re-ask.

---

# Reflection (1–2 sentences)
- What limits did you choose and why?  
- If you applied smoothing or an offset, how did it change behavior?

---

# Next Up
Move to **Sense HAT Advanced: Mission Dashboard** to add joystick interactivity and IMU-driven displays.
