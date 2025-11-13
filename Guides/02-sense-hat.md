# 02 — Sense HAT

> ### Quick Summary
> **Level:** 02 • **Time:** 45–90 min  
> **Prereqs:** [00 — Python Basics](../Guides/00-python-basics.md), [01 — Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT (Raspberry Pi OS)  
> **You’ll practice:** install/import, LED text & pixels, color tuples, temp/humidity/pressure, joystick menu, brightness/rotation/flip, letters/icons, bar graphs, optional CSV logging, safe loops & cleanup

> **Learn → Try**: Each section first explains the concept, then gives a tiny Try it task before moving on.

# Why This Matters
The Sense HAT turns your Pi into a tiny lab: an 8×8 color LED matrix for output, real‑world sensors (temperature, humidity, pressure), and a mini‑joystick for input — all **without breadboards**. You’ll use these skills in the Sense HAT Basics lab to build status badges, mini‑dashboards, and simple games.

---

## Table of contents
- [2) LED text (scrolling options)](#2-led-text-scrolling-options)
- [3) Pixels & colors (coordinates 0..7)](#3-pixels--colors-coordinates-07)
- [4) Environment sensors (°C, %RH, hPa)](#4-environment-sensors-c-%rh-hpa)
- [5) Joystick: tiny menu (left/right/select)](#5-joystick-tiny-menu-leftrightselect)
- [6) Display tweaks: brightness, rotation & flips](#6-display-tweaks-brightness-rotation--flips)
- [7) Letters & quick icons](#7-letters--quick-icons)
- [8) Sensor bar graph (tiny dashboard)](#8-sensor-bar-graph-tiny-dashboard)
- [Vocabulary](#vocabulary)


---

## What you’ll learn
- Install the Sense HAT library and import it in Python
- Safely create a `SenseHat()` object and use a main-guard
- Scroll text on the LED matrix with speed and color options
- Address individual pixels with `(x,y)` and draw simple sprites
- Read **temperature**, **humidity**, **pressure** (with units + smoothing)
- Handle joystick events and build a **tiny menu**
- Use `show_letter()` for quick **status icons**
- Build a simple **bar graph** for live sensor data
- Clean up properly with `sense.clear()` even on errors

---

## Setup
- Classroom default: **Raspberry Pi 500** running Raspberry Pi OS, editor **Thonny**.  

---

## 1) Import & first message (install + main-guard)
**Learn:** Import the library and create a `SenseHat` object. Use a main-guard so this file can be safely imported later without auto-running.

```python
# sense_playground.py
from sense_hat import SenseHat

def main():
    sense = SenseHat()
    sense.clear()
    sense.show_message("Hello, Sense HAT!", scroll_speed=0.08)
    sense.clear()

if __name__ == "__main__":
    main()
```

**Try it**
- Run the script. Change `scroll_speed` to make it slower/faster.
- Change the message text. Make sure the LEDs clear at the end.

---

## 2) LED text (scrolling options)
**Learn:** `show_message(text, scroll_speed, text_colour, back_colour)` scrolls characters across the 8×8 display. Colors are RGB tuples (0–255 each).

```python
from sense_hat import SenseHat

sense = SenseHat()
YELLOW = (255, 255, 0)
NAVY   = (0, 0, 30)

sense.clear()
sense.show_message("Welcome", scroll_speed=0.09,
                   text_colour=YELLOW, back_colour=NAVY)
sense.clear()
```

**Tips**
- Lower `scroll_speed` = faster scroll.
- Prefer dimmer colors (e.g., `(120,0,0)`) to avoid glare.
- `\n` won’t wrap — text scrolls horizontally.

**Try it**
- Show your name in your favorite color on a dark background.
- Make a 2‑word message by calling `show_message` twice with different colors.

---

## 3) Pixels & colors (coordinates 0..7)
**Learn:** The matrix is 8×8. `(0,0)` is top‑left, `x` grows → right, `y` grows → down. Use `set_pixel(x, y, (r,g,b))` and `set_pixels(list_of_64_colors)`.

```python
from sense_hat import SenseHat
sense = SenseHat()

def draw_corners():
    RED   = (200, 0, 0)
    GREEN = (0, 180, 0)
    BLUE  = (0, 0, 200)
    sense.clear()
    sense.set_pixel(0, 0, RED)      # top-left
    sense.set_pixel(7, 0, GREEN)    # top-right
    sense.set_pixel(0, 7, BLUE)     # bottom-left
    sense.set_pixel(7, 7, (255,255,255))  # bottom-right

draw_corners()
```

**Sprite with `set_pixels` (64 tuples, row‑major)**
```python
from sense_hat import SenseHat
sense = SenseHat()

X = (255,0,0)   # red
_ = (0,0,0)     # off

heart = [
    _,_,X,_,_,X,_,_,
    _,X,X,X,X,X,X,_,
    X,X,X,X,X,X,X,X,
    X,X,X,X,X,X,X,X,
    _,X,X,X,X,X,X,_,
    _,_,X,X,X,X,_,_,
    _,_,_,X,X,_,_,_,
    _,_,_,_,_,_,_,_,
]
sense.set_pixels(heart)
```

**Try it**
- Draw a smiley or an initial. Keep values 0–255.
- Write a helper `color(r,g,b)` that clamps values into range.

**Common mistakes**
- Coordinates outside `0..7` raise errors — validate before drawing.
- Tuples need parentheses: `(r, g, b)`.

---

## 4) Environment sensors (°C, %RH, hPa)
**Learn:** Read temperature, humidity, and pressure. Temperature can appear high due to CPU heating — apply a small offset and/or average several readings.

```python
from sense_hat import SenseHat
from time import sleep
from collections import deque

sense = SenseHat()
CPU_OFFSET = -3.0            # tweak for your classroom after comparison
window = deque(maxlen=5)     # simple moving average

try:
    while True:
        t = sense.get_temperature_from_humidity() + CPU_OFFSET
        h = sense.get_humidity()
        p = sense.get_pressure()
        window.append(t)
        avg_t = sum(window) / len(window)
        print(f"T={avg_t:.1f}°C  H={h:.1f}%  P={p:.1f} hPa")
        sleep(1.5)
finally:
    sense.clear()
```

**Try it**
- Print raw temp vs. averaged temp side‑by‑side.
- Change the window size (3→7) and see how smooth it feels.

**Tips**
- Always include units in your printouts.
- Read every 1–3 seconds to reduce self‑heating.

---

## 5) Joystick: tiny menu (left/right/select)
**Learn:** Build a simple menu controlled by the mini‑joystick. Left/right cycles items, middle selects. Then we display the chosen reading.

```python
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
menu = ["T", "H", "P"]   # Temperature, Humidity, Pressure
idx = 0

def show_menu():
    # highlight current choice as a letter
    sense.clear(0,0,30)
    sense.show_letter(menu[idx], text_colour=(255,255,255), back_colour=(0,0,30))

def show_value(ch):
    if ch == "T":
        val = round(sense.get_temperature_from_humidity(), 1)
        msg = f"T {val}°C"
    elif ch == "H":
        val = round(sense.get_humidity(), 1)
        msg = f"H {val}%"
    else:
        val = round(sense.get_pressure(), 1)
        msg = f"P {val} hPa"
    sense.show_message(msg, scroll_speed=0.07, text_colour=(200,200,255))

show_menu()
try:
    while True:
        for e in sense.stick.get_events():
            if e.action != "pressed":
                continue
            if e.direction == "left":
                idx = (idx - 1) % len(menu)
                show_menu()
            elif e.direction == "right":
                idx = (idx + 1) % len(menu)
                show_menu()
            elif e.direction == "middle":
                show_value(menu[idx])
        sleep(0.05)
finally:
    sense.clear()
```

**Try it**
- Add colors: blue for H, orange for T, yellow for P.  
- Add a fourth menu item that shows a small icon (like a heart).

---

## 6) Display tweaks: brightness, rotation & flips
**Learn:** You can dim the LEDs, rotate the display, and mirror it — no IMU required.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
sense.low_light = True

WHITE = (255,255,255)

def draw_L():
    sense.clear()
    # An asymmetric "L" shape so flips are easy to see
    for y in range(8):        # vertical bar (left edge)
        sense.set_pixel(0, y, WHITE)
    for x in range(8):        # bottom bar
        sense.set_pixel(x, 7, WHITE)

# 1) Show the shape
draw_L()
sleep(1.0)

# 2) Flip horizontally (mirrors left↔right)
sense.flip_h()
sleep(1.0)

# 3) Flip vertically (mirrors top↔bottom)
sense.flip_v()
sleep(1.0)

# 4) Rotate the drawing by 90°, then 180°, then back to 0°
for angle in (90, 180, 0):
    sense.set_rotation(angle)
    # Use a letter so you can see rotation without redrawing pixels
    sense.show_letter("R")
    sleep(1.0)

sense.clear()

```
**What each call does**
- sense.low_light = True dims the whole matrix (no sensors involved).
- sense.flip_h() mirrors the current 8×8 image left↔right.
- sense.flip_v() mirrors the current 8×8 image top↔bottom.
- sense.set_rotation(0|90|180|270) rotates how things are drawn. Anything you draw afterward follows that orientation (letters included).

---

## 7) Letters & quick icons
**Learn:** `show_letter(ch, text_colour, back_colour)` is a fast way to display status icons (✓, !, arrows) without scrolling a whole message.

```python
from sense_hat import SenseHat
sense = SenseHat()

GREEN = (0, 180, 0)
RED   = (200, 0, 0)
NAVY  = (0, 0, 30)

sense.clear(NAVY)
sense.show_letter("✓", text_colour=GREEN, back_colour=NAVY)  # success
```

**Try it**
- Make a tiny status sequence: ".", ".", "✓" (each for 0.5s).  
- Show arrows "↑↓←→" when the joystick is pressed in each direction.

---

## 8) Sensor bar graph (tiny dashboard)
**Learn:** Turn numbers into a simple bar graph. We’ll map ranges to how many LEDs to light in a column.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

def bar(col, height, color):
    # Draw a vertical bar in column col (0..7), height 0..8.
    h = max(0, min(8, height))
    for y in range(8):
        pixel = color if y >= 8 - h else (0, 0, 0)
        sense.set_pixel(col, y, pixel)

def temp_to_height(c):
    # Map 15–35°C → 0–8 LEDs (clamp outside)
    c = max(15, min(35, c))
    return int(round((c - 15) / (35 - 15) * 8))

def rh_to_height(rh):
    # Map 20–80% → 0–8 LEDs
    rh = max(20, min(80, rh))
    return int(round((rh - 20) / (80 - 20) * 8))

def press_to_height(hpa):
    # Map 980–1040 hPa → 0–8 LEDs
    hpa = max(980, min(1040, hpa))
    return int(round((hpa - 980) / (1040 - 980) * 8))

try:
    while True:
        t = sense.get_temperature_from_humidity()
        h = sense.get_humidity()
        p = sense.get_pressure()
        sense.clear()
        bar(1, temp_to_height(t),   (255, 80, 80))   # temp column
        bar(3, rh_to_height(h),     (80, 160, 255))  # humidity column
        bar(5, press_to_height(p),  (255, 200, 80))  # pressure column
        sleep(0.8)
finally:
    sense.clear()
```

**Try it**
- Change the mapping ranges for your classroom values.
- Add a 4th column that lights green if `t < 28°C`, red otherwise.

---

## Vocabulary
- LED matrix — 8×8 RGB LEDs you can set with colors.
- Color tuple — `(r,g,b)` with each 0–255.
- Joystick event — `direction` + `action` like `"left"` + `"pressed"`.
- Rotation — turning the display by 0/90/180/270 degrees.
- Flip — mirroring horizontally or vertically.
- Smoothing — averaging recent readings to reduce noise.
- Bar graph — a column of lit pixels showing how big a value is.

---

## Check your understanding
1) Where is `(0,0)` and what happens if you call `set_pixel(8,8,...)`?  
2) Why might temperature read high, and two ways to compensate?  
3) What two fields are in a joystick event, and what do they mean?  
4) What does `low_light` do, and when would you use it?  
5) How would you map 20–80% humidity to a bar height of 0–8?

---

## Mini-projects
**A) Weather Badge**  
- Every 3 sec, read temp & humidity.  
- If `temp > 28°C`, flash a red "!" for 1 sec; else show a green "✓".  
- Stretch: Map humidity to brightness.

**B) Reaction Timer (joystick)**  
- After 1–3 sec random delay, turn the screen green.  
- Measure time until middle press; print milliseconds.  
- Stretch: Keep best time (high score).

**C) Tiny Menu Plus**  
- Add a fourth menu item that shows a small icon or animation.  
- Stretch: Color-code menu items (e.g., blue=humidity, orange=temp).

**D) Pixel Art Animator**  
- Alternate between two 8×8 sprites every 300 ms (blink or heartbeat).

---

## Troubleshooting
- `ModuleNotFoundError: sense_hat` → Install with `sudo apt install sense-hat` (on a Raspberry Pi), then reboot.  
- Nothing shows on LEDs → Check HAT seated on GPIO, power, try `sense.clear()` first.  
- Joystick silent → Keep your script running (`while True:` or `signal.pause()`); handle `"pressed"`.  
- High temperature → Use `_from_humidity/_from_pressure`, read less often, apply a small offset, average readings.  
- Too bright colors → Use lower RGB values (e.g., `(120,0,0)` instead of full `(255,0,0)`).

---

## Next up
Do the lab: **[02 — Sense HAT Basics](../Labs/02-sense-hat-basics.md)**.

---
---

**Install (if needed)**
```bash
sudo apt update && sudo apt install -y sense-hat
sudo reboot
```
If sensors don’t respond, enable I2C in `raspi-config` and reboot.

---
