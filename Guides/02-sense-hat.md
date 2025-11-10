# 02 — Sense HAT

> ### Quick Summary
> **Level:** 02 • **Time:** 45–90 min  
> **Prereqs:** [00 — Python Basics](../Guides/00-python-basics.md), [01 — Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT (Raspberry Pi OS)  
> **You’ll practice:** install/import, LED text & pixels, color tuples, reading temp/humidity/pressure, joystick events, basic IMU, safe loops & cleanup

> **Learn → Try**: Each section first **explains** the concept, then gives a tiny **Try it** task before moving on.

# Why This Matters
The Sense HAT turns your Pi into a tiny lab: an 8×8 color LED matrix for output, real‑world sensors (temperature, humidity, pressure), an IMU for motion, and a mini‑joystick for input. You’ll use these skills in the **Sense HAT Basics** lab to build interactive widgets and mini‑games.

---

## Table of contents
- [1) Import & first message (install + main‑guard)](#1-import--first-message-install--main-guard)
- [2) LED text (scrolling options)](#2-led-text-scrolling-options)
- [3) Pixels & colors (coordinates 0..7)](#3-pixels--colors-coordinates-07)
- [4) Environment sensors (°C, %RH, hPa)](#4-environment-sensors-c-%rh-hpa)
- [5) Joystick events (pressed/held/released)](#5-joystick-events-pressedheldreleased)
- [6) Basic motion via IMU (accel/orientation)](#6-basic-motion-via-imu-accelorientation)
- [Vocabulary](#vocabulary)

---

## What you’ll learn
- Install the Sense HAT library and **import** it in Python
- Safely create a `SenseHat()` object and use a **main‑guard**
- Scroll text on the LED matrix with speed and color options
- Address individual pixels with `(x,y)` and draw simple sprites
- Read **temperature**, **humidity**, **pressure** (with units + smoothing)
- Handle **joystick** directions and actions
- Sample **accelerometer** and **orientation** (pitch/roll/yaw)
- Clean up properly with `sense.clear()` even on errors

---

## Setup
- **Classroom default:** **Raspberry Pi 500** running Raspberry Pi OS, editor **Thonny**.  
- In Thonny: **File → New**, save as `sense_playground.py` in `~/Documents/CodeCreate/`.

**Install (if needed)**
```bash
sudo apt update && sudo apt install -y sense-hat
sudo reboot
```
_If sensors don’t respond, enable I2C in `raspi-config` and reboot._

---

## 1) Import & first message (install + main‑guard)
**Learn:** You must import the library and create a `SenseHat` object. Use a **main‑guard** so this file can be safely imported later without auto‑running.

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

**Why main‑guard?** When you run this file directly, `__name__ == "__main__"` so `main()` runs. If another file imports this one, the message won’t auto‑scroll. This keeps your helpers reusable.

**Try it**
- Run the script. Change `scroll_speed` to make it slower/faster.
- Change the message text. Make sure the LEDs clear at the end.

---

## 2) LED text (scrolling options)
**Learn:** `show_message(text, scroll_speed, text_colour, back_colour)` scrolls characters across the 8×8 display. Colors are **RGB tuples** (0–255 each).

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
- `\n` won’t wrap—text scrolls horizontally.

**Try it**
- Show your name in your favorite color on a dark background.
- Make a 2‑word message by calling `show_message` twice with different colors.

---

## 3) Pixels & colors (coordinates 0..7)
**Learn:** The matrix is 8×8. `(0,0)` is **top‑left**, `x` grows → right, `y` grows → down. Use `set_pixel(x, y, (r,g,b))` and `set_pixels(list_of_64_colors)`.

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
- Coordinates outside `0..7` raise errors—validate before drawing.
- Tuples need parentheses: `(r, g, b)`.

---

## 4) Environment sensors (°C, %RH, hPa)
**Learn:** Read temperature, humidity, pressure. Temperature can appear high due to CPU heating—apply a small offset and/or average several readings.

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
- Change the window size (3→7) and see how “smooth” it feels.

**Tips**
- Always include **units** in your printouts.
- Read every 1–3 seconds to reduce self‑heating.

---

## 5) Joystick events (pressed/held/released)
**Learn:** The mini‑stick provides a stream of events: `direction` (`"up","down","left","right","middle"`) and `action` (`"pressed","held","released"`). Use callbacks **or** poll with `get_events()`.

**Callback style**
```python
from sense_hat import SenseHat
from signal import pause

sense = SenseHat()

def on_any(e):
    if e.action != "pressed":
        return
    print(f"{e.direction} pressed")

sense.stick.direction_any = on_any
pause()  # keep program alive
```

**Poll style + move a pixel**
```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
x, y = 3, 3

def draw():
    sense.clear()
    sense.set_pixel(x, y, (255,255,255))

draw()
while True:
    for e in sense.stick.get_events():
        if e.action != "pressed":
            continue
        if e.direction == "up":    y = max(0, y-1)
        if e.direction == "down":  y = min(7, y+1)
        if e.direction == "left":  x = max(0, x-1)
        if e.direction == "right": x = min(7, x+1)
        draw()
    sleep(0.02)
```

**Try it**
- Make the pixel turn **green** when moving and **white** when idle.
- Use the **middle** press to clear the screen.

**Pitfalls**
- If the program exits, you won’t see events—keep it running.
- Handle only `"pressed"` to avoid repeats while held.

---

## 6) Basic motion via IMU (accel/orientation)
**Learn:** The IMU provides raw acceleration (`g`s) and fused orientation angles (degrees). Motion is noisy—consider averaging.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.set_imu_config(compass=True, gyroscope=True, accelerometer=True)

while True:
    accel = sense.get_accelerometer_raw()
    ax, ay, az = accel["x"], accel["y"], accel["z"]
    o = sense.get_orientation()       # pitch/roll/yaw 0..360
    pitch, roll, yaw = o["pitch"], o["roll"], o["yaw"]
    print(f"accel x={ax:.2f} y={ay:.2f} z={az:.2f} | pitch={pitch:.1f} roll={roll:.1f} yaw={yaw:.1f}")
    sleep(0.2)
```

**Keep text upright (auto‑rotation by roll)**
```python
o = sense.get_orientation()
r = o["roll"]
angle = 0
if r > 315 or r <= 45:   angle = 0
elif 45 < r <= 135:      angle = 270
elif 135 < r <= 225:     angle = 180
else:                    angle = 90
sense.set_rotation(angle)
sense.show_message("Aligned!")
```

**Try it**
- Map tilt (roll/pitch) to a pixel position—tilt to steer the dot.
- Show a red “!” if |ax| or |ay| exceeds 0.6 (shake alert).

**Pitfalls**
- Yaw needs good compass calibration; keep away from magnets/metal.
- Average readings to reduce jitter.

---

## Vocabulary
- **LED matrix** — 8×8 RGB LEDs you can set with colors.
- **Color tuple** — `(r,g,b)` with each 0–255.
- **Joystick event** — `direction` + `action` like `"left"` + `"pressed"`.
- **IMU** — Inertial Measurement Unit (accel + gyro + compass).
- **Orientation** — fused angles: pitch/roll/yaw (degrees).
- **Smoothing** — averaging recent readings to reduce noise.

---

## Check your understanding
1) Where is `(0,0)` and what happens if you call `set_pixel(8,8,...)`?  
2) Why might temperature read high, and two ways to compensate?  
3) What two fields are in a joystick event, and what do they mean?  
4) What’s the difference between `get_accelerometer_raw()` and `get_orientation()`?  
5) Why use a `try/finally` or `main()` function with `sense.clear()` at the end?

---

## Mini‑projects
**A) Weather Badge**  
- Every 3 sec, read temp & humidity.  
- If `temp > 28°C`, flash a red “!” for 1 sec; else show a green “✓”.  
- *Stretch:* Map humidity to brightness.

**B) Tilt‑Etch‑A‑Sketch**  
- Use accelerometer X/Y to move a “pen”.  
- Press **middle** to clear.

**C) Reaction Timer**  
- After 1–3 sec random delay, turn the screen **green**.  
- Measure time until **middle** press; print milliseconds.  
- *Stretch:* Keep best time (high score).

---

## Troubleshooting
- **`ModuleNotFoundError: sense_hat`** → Install with `sudo apt install sense-hat` (on a Raspberry Pi), then reboot.  
- **Nothing shows on LEDs** → Check HAT seated on GPIO, power, try `sense.clear()` first.  
- **Joystick silent** → Keep your script running (`while True:` or `signal.pause()`); handle `"pressed"`.  
- **High temperature** → Use `_from_humidity/_from_pressure`, read less often, apply a small offset, average readings.  
- **Too bright colors** → Use lower RGB values (e.g., `(120,0,0)` instead of full `(255,0,0)`).

---

## Next up
Do the lab: **[02 — Sense HAT Basics](../Labs/02-sense-hat-basics.md)**.
