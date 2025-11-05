# 02 — Sense HAT Basics

> ### Quick Summary
> **Level:** 02 • **Time:** 45–75 min  
> **Prereqs:** [00 — Python Basics](./00-python-basics.md)  
> **Hardware:** Raspberry Pi + Sense HAT  
> **You’ll practice:** text & pixels on LEDs, reading temperature/humidity/pressure, joystick input, simple loops & timing

# Why This Matters
The Sense HAT turns code into something you can see and feel—lights, sensors, and a tiny joystick. You’ll use these skills to build a weather light and interactive mini‑projects.

---
## What you’ll learn
- Initialize the Sense HAT and display text/colors
- Read temperature, humidity, and pressure safely
- Loop with a sensible sampling rate (1–3 s) to reduce self‑heating
- Handle joystick input (events vs polling)
- Apply thresholds to change LED colors
- Log or print formatted sensor data

## Setup
This setup uses Python 3 on Raspberry Pi OS with the `sense_hat` library installed. Test the LEDs:
```python
from sense_hat import SenseHat
s = SenseHat()
s.show_message("Hello!", scroll_speed=0.08)
s.clear()
```

## Materials  (ONLY include if hardware is involved)
- Raspberry Pi (with power, keyboard/mouse, HDMI)
- Sense HAT (mounted carefully—don’t flex the pins)
- Optional: case / standoffs for stress relief

---
## Walkthrough — Step by Step (with explanations)

### 1) LEDs: pixels and messages
**Idea:** Show information visually.
```python
from sense_hat import SenseHat
s = SenseHat()
s.set_pixel(0, 0, 255, 0, 0)   # red at top-left
s.show_message("Hi", text_colour=(0,255,0))
s.clear()
```
**Anatomy:**
- `(x, y)` is 0–7.
- Colors are `(R,G,B)` from 0–255.

### 2) Read sensors with cadence
**Idea:** Print formatted readings at a steady pace.
```python
import time
from sense_hat import SenseHat

s = SenseHat()
while True:
    t = s.get_temperature()
    h = s.get_humidity()
    p = s.get_pressure()
    print(f"{t:.1f} °C  {h:.0f}%  {p:.0f} hPa")
    time.sleep(2)  # 1–3 s reduces self-heating
```
**Notes & pitfalls:**
- Values drift if you sample too fast.
- Keep your Pi away from heat sources.

### 3) Threshold → color
**Idea:** Use sensor thresholds to change the LED color.
```python
from sense_hat import SenseHat
import time

HOT = 27.0
COLD = 18.0
s = SenseHat()

while True:
    t = s.get_temperature()
    if t >= HOT:
        s.clear(255, 0, 0)   # hot = red
    elif t <= COLD:
        s.clear(0, 0, 255)   # cold = blue
    else:
        s.clear(0, 255, 0)   # good = green
    time.sleep(2)
```
**Notes & pitfalls:**
- Choose thresholds appropriate to your room.
- Don’t leave full-brightness LEDs on for long.

### 4) Joystick input (events)
**Idea:** React to button presses.
```python
from sense_hat import SenseHat
from signal import pause

s = SenseHat()

def on_press(event):
    if event.action == "pressed" and event.direction == "middle":
        s.show_message("OK")

s.stick.direction_any = on_press
pause()  # keep program alive
```
**Notes & pitfalls:**
- Polling alternative: loop over `s.stick.get_events()` if callbacks aren’t available.

---
## Vocabulary
- **Pixel**: One LED at coordinate (x, y) on the 8×8 matrix.
- **RGB**: Red‑Green‑Blue color values 0–255.
- **Sampling rate**: How often you read sensors.
- **Threshold**: A value at which behavior changes.
- **Callback**: Function called when an event happens.
- **Polling**: Actively checking for events in a loop.

---
## Check your understanding
1) Why do we delay 1–3 seconds between sensor reads?  
2) What color model does the LED matrix use?  
3) Where is the origin (0,0) on the LED grid?  
4) How do callbacks differ from polling the joystick?  
5) What happens if you drive LEDs at max brightness constantly?

---
## Try it: Mini-exercises
Make a **Weather Warning Light**: use humidity for blue tint, temperature for red tint, and turn the whole matrix green when comfortable.  
**Stretch goals:**
- Add a scrolling message with the current temperature.
- Log readings to CSV once every 5 seconds.

---
## Troubleshooting
- **No LEDs** → Check Sense HAT firmly seated; try a simple `show_message`.  
- **Crazy numbers** → Slow down sampling; let the board thermally settle.  
- **Joystick unresponsive** → Verify event callbacks; fall back to polling with `get_events()`.

---
## Next up
**[02 – Sense HAT Basics](../Labs/02-sense-hat-basics.md)**
