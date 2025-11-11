# 02 — Sense HAT (Do Lab)

> ### Quick Summary  
> **Level:** 02 • **Time:** 60–90 min  
> **Prereqs:** 00 — Python Basics, 01 — Python Functions  
> **Hardware:** Raspberry Pi 500 + Sense HAT (Raspberry Pi OS)  
> **Editor:** Thonny  
> **You’ll practice:** LED text & icons, pixel art, brightness & rotation, sensors (temp/humidity/pressure), joystick menus, bar graphs, optional CSV logging


# Why this matters
The Sense HAT gives instant visual feedback and real-world sensor input without any breadboarding. In this lab you’ll combine text, pixel art, live sensor reads, and a joystick-driven menu to build a small, reusable dashboard you can extend later.


---
## Objectives

- Scroll text and show quick status icons on the 8×8 LED matrix
- Draw simple pixel art using coordinates and 8×8 sprites
- Adjust brightness and rotation for classroom conditions
- Read temperature, humidity, and pressure (with friendly units)
- Build a joystick mini‑menu to switch display modes
- Visualize values as bar graphs
- (Optional) Log readings to CSV for later analysis


## Setup (Pi 500 + Thonny)

**Classroom default:** Raspberry Pi 500 running Raspberry Pi OS, editor Thonny.

1) Open **Thonny** → File → New → save your project in: `~/Documents/CodeCreate/SenseHAT/`
2) Verify Sense HAT library (usually preinstalled on Pi OS):
   ```bash
   sudo apt update && sudo apt install -y sense-hat
   sudo reboot
   ```
3) Test: create `00_check.py`
   ```python
   from sense_hat import SenseHat
   s = SenseHat()
   s.show_message("Hello!", scroll_speed=0.06)
   s.clear()
   ```

**Run vs Import (main-guard):**
Place this at the bottom of scripts that should run *only* when executed directly:
```python
if __name__ == "__main__":
    main()
```


---
## Starter files

- **01_text_and_icons.py** — Show a marquee and a few quick icons using `show_message` and `show_letter`. Provide helper functions for colors and a simple `quick_icon(name)`.
- **02_pixel_art.py** — Create a `show_image(pixels)` helper (expects 64 RGB tuples). Include one sprite (e.g., a heart) and a TODO for a custom mascot.
- **03_display_tweaks.py** — Demonstrate `low_light` and `set_rotation(...)` with a clear letter or asymmetric pattern so changes are visible.
- **04_sensors_bar.py** — Read temp/humidity/pressure. Print with units. Map each value to a simple bar graph.
- **05_menu.py** — Joystick mini‑menu. Left/right cycle modes, center shows the current value or runs a mode action.
- **06_logger_optional.py** — (Optional) Append timestamped readings to `sense_log.csv` in your project folder.


## Checkpoints

- [ ] Text & icons display correctly; colors are readable
- [ ] Custom 8×8 sprite renders and clears
- [ ] Brightness/rotation behave as expected
- [ ] Sensors print values with units; bar graphs map correctly
- [ ] Joystick menu cycles modes and shows values
- [ ] Optional CSV file grows with timestamped rows

---
## Tasks

### Task 1 — Text & Quick Icons  
**File:** `01_text_and_icons.py`

```python
from sense_hat import SenseHat
from time import sleep

s = SenseHat()

def marquee(msg, speed=0.07, text=(255,255,255), back=(0,0,0)):
    s.show_message(msg, scroll_speed=speed, text_colour=text, back_colour=back)

def letter(ch, color=(255,255,255), back=(0,0,0)):
    s.show_letter(ch, text_colour=color, back_colour=back)

QUICK = {
    "ok":    ("✓", (0,200,0)),
    "warn":  ("!", (255,200,0)),
    "x":     ("✗", (220,0,0)),
    "heart": ("♥", (255,0,80)),
}

def quick_icon(name):
    glyph, color = QUICK[name]
    letter(glyph, color)

def main():
    marquee("Sense HAT", speed=0.08, text=(255,255,255), back=(0,0,30))
    sleep(0.4)
    for key in ("heart","ok","warn","x"):
        quick_icon(key); sleep(0.5)
    s.clear()

if __name__ == "__main__":
    main()
```

**To Do**
- Change colors and add **your initials** as a marquee.
- Add **one new icon** to `QUICK` and display it.

### Task 2 — Pixel Art Helper  
**File:** `02_pixel_art.py`

```python
from sense_hat import SenseHat
from time import sleep
s = SenseHat()

# Colors
X = (0,0,0)   # off
R = (255,0,0)
W = (255,255,255)
P = (255,0,80)

def show_image(pixels):
    if len(pixels) != 64:
        raise ValueError("Provide exactly 64 pixels (8x8).")
    s.set_pixels(pixels)

def heart():
    img = [
        X,R,R,X,X,R,R,X,
        R,P,P,R,R,P,P,R,
        R,P,P,P,P,P,P,R,
        X,R,P,P,P,P,R,X,
        X,X,R,P,P,R,X,X,
        X,X,X,R,R,X,X,X,
        X,X,X,X,R,X,X,X,
        X,X,X,X,X,X,X,X,
    ]
    show_image(img)

def main():
    heart(); sleep(1.5); s.clear()

if __name__ == "__main__":
    main()
```

**To Do**
- Make a **mascot()** sprite for your team.
- Tip: sketch on 8×8 graph paper before coding.

### Task 3 — Brightness & Rotation  
**File:** `03_display_tweaks.py`

```python
from sense_hat import SenseHat
from time import sleep
s = SenseHat()

def demo():
    s.low_light = True   # gentle brightness
    for angle in (0, 90, 180, 270):
        s.set_rotation(angle)
        s.show_letter("D")
        sleep(0.6)
    s.low_light = False
    s.clear()

if __name__ == "__main__":
    demo()
```

**To Do**
- Toggle `low_light` and compare in your room.
- Pick the rotation that matches how your HAT is mounted.

### Task 4 — Sensors + Bar Graph  
**File:** `04_sensors_bar.py`

```python
from sense_hat import SenseHat
from time import sleep

s = SenseHat()

def bar_graph(value, min_v, max_v, color=(0,255,0), back=(0,0,0)):
    v = max(min_v, min(max_v, value))
    ratio = 0 if max_v == min_v else (v - min_v) / (max_v - min_v)
    lit = int(round(ratio * 64))
    pixels = [color if i < lit else back for i in range(64)]
    s.set_pixels(pixels)

def main():
    t = s.get_temperature_from_humidity()
    h = s.get_humidity()
    p = s.get_pressure()

    print(f"T={t:.1f}°C  H={h:.1f}%  P={p:.0f} hPa")

    bar_graph(t, 15, 35, (255,120,0))
    sleep(0.8)
    bar_graph(h, 0, 100, (80,160,255))
    sleep(0.8)
    bar_graph(p, 950, 1050, (200,200,255))
    sleep(0.8)
    s.clear()

if __name__ == "__main__":
    main()
```

**To Do**
- Adjust ranges so your bars use more of the matrix.
- Show a **legend**: call `show_message("Temp")` before the temperature bar, etc.

### Task 5 — Joystick Mini‑Menu  
**File:** `05_menu.py`

```python
from sense_hat import SenseHat
from time import sleep

s = SenseHat()
MODES = ["TEXT","TEMP","HUM","PRESS"]
idx = 0

def show_mode(mode):
    if mode == "TEXT":
        s.show_message("Hi!", scroll_speed=0.06, text_colour=(255,255,255))
    elif mode == "TEMP":
        s.show_message(f"T {s.get_temperature_from_humidity():.1f}C", text_colour=(255,140,0))
    elif mode == "HUM":
        s.show_message(f"H {s.get_humidity():.1f}%", text_colour=(80,160,255))
    elif mode == "PRESS":
        s.show_message(f"P {s.get_pressure():.0f} hPa", text_colour=(200,200,255))

def indicator():
    s.show_letter(MODES[idx][0])
    sleep(0.2)
    s.clear()

def main():
    global idx
    indicator()
    while True:
        for e in s.stick.get_events():
            if e.action != "pressed":
                continue
            if e.direction == "right":
                idx = (idx + 1) % len(MODES); indicator()
            elif e.direction == "left":
                idx = (idx - 1) % len(MODES); indicator()
            elif e.direction == "up":
                s.low_light = not s.low_light   # toggle brightness
            elif e.direction == "middle":
                show_mode(MODES[idx])
        sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    finally:
        s.clear()
```

**To Do**
- Change the indicator to the **full word** briefly (scroll) instead of one letter.
- Add **rotation toggle** on `down`.

### Task 6 (Optional) — CSV Logger  
**File:** `06_logger_optional.py`

```python
from sense_hat import SenseHat
from time import sleep
from datetime import datetime
from pathlib import Path
import csv

s = SenseHat()
LOG = Path.home() / "Documents" / "CodeCreate" / "SenseHAT" / "sense_log.csv"

def write_row(dt, t, h, p):
    newfile = not LOG.exists()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if newfile:
            w.writerow(["timestamp","temp_c","humidity_pct","pressure_hpa"])
        w.writerow([dt.isoformat(), f"{t:.2f}", f"{h:.2f}", f"{p:.2f}"])

def main():
    print(f"Logging to {LOG}")
    for _ in range(20):
        now = datetime.now()
        t = s.get_temperature_from_humidity()
        h = s.get_humidity()
        p = s.get_pressure()
        write_row(now, t, h, p)
        sleep(3)

if __name__ == "__main__":
    main()
```

**To Do**
- Flash **red** if temp > 30°C while logging.
- Add a constant at the top to change the interval (seconds).


---
## Extensions (pick one)

- Emoji animation: blink or bounce a pixel
- Rainbow marquee: cycle text colors while scrolling
- Multi‑bar dashboard: separate columns for T/H/P
- CSV stats viewer: print min/max/avg from your log


## Submission
- Zip your `SenseHAT/` folder or submit the six `.py` files.
- Include a short README noting any extension you completed.
- (Optional) Attach `sense_log.csv` if you did Task 6.


## Rubric

- **Core features (Tasks 1–5)** — 70%
- **Code quality (functions, comments, main‑guard, cleanup)** — 15%
- **Stretch or Logger** — 15%


## Troubleshooting

- Nothing on LEDs → ensure HAT is seated on GPIO; try `s.clear()` and a simple `show_message`.
- `ModuleNotFoundError: sense_hat` → install with `sudo apt install sense-hat` on a Raspberry Pi, then reboot.
- Joystick events missing → keep the loop running; react on `e.action == 'pressed'`.
- High temperature readings → prefer `get_temperature_from_humidity()`, read less often, apply a small offset/averaging.
- Display upside‑down → use `set_rotation(90/180/270)`; for glare use `low_light = True`.