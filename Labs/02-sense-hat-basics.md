
---
title: Sense HAT Basics — Weather Warning Light
level: 02
estimated_time: 30–45 min
difficulty: Beginner
prereqs:
  - Guide: [02 – Sense HAT](../Guides/02-sense-hat.md)
rubric:
  - ✅ Must: Reads temperature and humidity from Sense HAT
  - ✅ Must: Prints readings and updates LED matrix color each cycle
  - ✅ Must: Uses user-provided thresholds and loops until Ctrl-C
  - ⭐ Stretch: Adds lives/tries, logs to CSV, or adds a simple icon pattern
---

# Goal
Build a **Weather Warning Light**. Every few seconds, read **temperature** and **humidity**.  
If it's **too hot** OR **too dry**, flash the LED matrix **red**; otherwise show **green**.

## Materials
- Raspberry Pi with Sense HAT
- Python 3 (Raspberry Pi OS)

## Steps
1) **Plan** — Pick temperature (°C) and humidity (%) thresholds you consider unsafe.  
2) **Build** — Prompt the user for those thresholds using `input()` (floats).  
3) **Code** — Read sensors, decide status, and set LED color accordingly.  
4) **Test** — Try several thresholds and verify LED behavior and printed output.  
5) **Iterate** — Add one extension from below.

## Starter snippet
```python
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def get_readings():
    """Return (temp_c, humidity_percent)."""
    t = sense.get_temperature()
    h = sense.get_humidity()
    return round(t, 1), round(h, 1)

def show_status(temp, hum, t_limit, h_limit):
    too_hot = temp > t_limit
    too_dry = hum < h_limit
    if too_hot or too_dry:
        sense.clear(255, 0, 0)   # red
        print(f"WARNING: T={temp}°C (>{t_limit}) or H={hum}% (<{h_limit})!")
    else:
        sense.clear(0, 255, 0)   # green
        print(f"OK: T={temp}°C  H={hum}%")

print("Sense HAT — Weather Warning Light")
t_limit = float(input("High temperature limit (°C)? ").strip())
h_limit = float(input("Low humidity limit (%)? ").strip())

try:
    while True:
        temp, hum = get_readings()
        show_status(temp, hum, t_limit, h_limit)
        time.sleep(2)
except KeyboardInterrupt:
    sense.clear()
    print("Program stopped. Stay safe!")
```

## Submission / Demo checklist
- [ ] Loops until **Ctrl‑C** and never crashes on normal input
- [ ] Prints readings and sets LED **green** when safe, **red** when unsafe
- [ ] Thresholds are **entered by the user**

## Extensions (choose one)
- **Icon alert:** Show a red “!” or a green “✓” as an 8×8 pattern instead of solid color.
- **CSV logging:** Append `timestamp,temp,humidity` to a file once per loop.
- **Buzzer via text:** Simulate “beeps” with printed lines when unsafe.

## Troubleshooting
- **No color change** → Ensure `sense.clear(r,g,b)` is called each cycle.  
- **Odd temperature values** → CPU heat can bias readings; add a short idle before reading or subtract an offset.  
- **ValueError on input** → Wrap `float(input(...))` in `try/except` and re‑ask.

## Reflection
- Which part was trickiest—sensor reading, thresholds, or LED control? Why?

## Next up
Level up with **[02.5 – Sense HAT Advanced: Mission Dashboard](../Labs/02-5-sense-hat-advanced.md)**.
