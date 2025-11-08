# Sense HAT

> ### Quick Summary
> **Level:** 02 • **Time:** 45–90 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)   
> **Hardware:** Raspberry Pi + Sense HAT   
> **You’ll practice:** installing/importing, LED text & pixels, reading temp/humidity/pressure, joystick events, and basic motion/IMU readings

> **Learn → Try**: Learn concepts here with tiny examples, then Try quick practice before you Do the matching Lab.

# Why This Matters
The Sense HAT turns your Pi into a tiny lab: an 8×8 color LED matrix for output, sensors for the real world (temperature, humidity, pressure), and motion/joystick input for interaction. You’ll use these skills in the **Sense HAT Basics** lab to make small, responsive projects.

---

## What you’ll learn
- Show text and draw pixels on the 8×8 LED matrix
- Read environmental sensors (temperature, humidity, pressure)
- Handle joystick input (pressed/held/released)
- Use simple IMU readings (accelerometer/gyroscope/orientation)

---

## Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**.
- Open **Thonny** (Menu → Programming → Thonny).
- Create `sense_playground.py` in `~/Documents/CodeCreate/`, then **Run ▶** and view output in the **Shell**.

**If Sense HAT support isn’t installed on your Pi:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y sense-hat
sudo reboot
```
_Optional_: enable I2C in `raspi-config` if needed.

Quick test in Python:
```python
from sense_hat import SenseHat
sense = SenseHat()
sense.show_message("Hello!")
```

---

## Materials
- Raspberry Pi (with power and microSD)
- Sense HAT (mounted on GPIO header)
- Optional: HDMI display, keyboard/mouse; or SSH access

## Walkthrough — Step by Step (with explanations)

### 1) Display text on the LED matrix
**Idea:** Use `show_message()` to scroll a string across the 8×8 LEDs.  
**Key options:**  
- `scroll_speed` — lower is faster (e.g., `0.05` fast, `0.12` slower)  
- `text_colour=(r,g,b)` — each 0–255  
- `back_colour=(r,g,b)` — background color

```python
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()  # turn off any previous pixels
sense.show_message(
    "Hello!", 
    scroll_speed=0.08,
    text_colour=(255, 255, 0),   # yellow
    back_colour=(0, 0, 20)       # dark blue background
)
```

**Notes & pitfalls**
- Strings are printed **one character at a time** across the display—newline `\n` won’t “wrap.”  
- Use `sense.clear()` to blank the display at the end of your program.  
- If nothing shows, check power/seating of the HAT and that your script keeps running long enough to scroll.

**Try it:** Show your name in your favorite color. Then slow down the speed until it’s easy to read.

---

### 2) Set specific pixels (coordinate system + colors)
**Idea:** The LED matrix is 8 columns by 8 rows. Coordinates start at the **top‑left**.  
- `x`: 0..7 (left→right)  
- `y`: 0..7 (top→bottom)

```python
from sense_hat import SenseHat
sense = SenseHat()

red   = (255, 0, 0)
green = (0, 255, 0)
blue  = (0, 0, 255)

sense.clear()
sense.set_pixel(0, 0, red)      # top-left
sense.set_pixel(7, 7, green)    # bottom-right
sense.set_pixel(3, 4, blue)     # somewhere in the middle
```

**Drawing many pixels at once (`set_pixels`)**
Create a list of **64 color tuples** in row‑major order (row 0, then row 1, …).

```python
X = (255, 0, 0)   # red
_ = (0, 0, 0)     # off (black)

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

**Helpful utilities**
```python
def clamp(c):
    # keep each color 0..255
    return max(0, min(255, int(c)))

def color(r, g, b):
    return (clamp(r), clamp(g), clamp(b))
```

**Common mistakes**
- Coordinates outside 0..7 cause an error. Validate x/y before drawing.
- Don’t forget parentheses for tuples `(r, g, b)`.

---

### 3) Read environmental sensors (units, accuracy, smoothing)
**Idea:** Sense HAT measures temperature (°C), humidity (%), and pressure (millibars / hPa).  
**Note:** Temperature can read high because the Pi’s CPU warms the board.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while True:
    # Different estimation methods—try both:
    t_h = sense.get_temperature_from_humidity()
    t_p = sense.get_temperature_from_pressure()
    h = sense.get_humidity()
    p = sense.get_pressure()
    print(f"T(H)={t_h:.1f}°C  T(P)={t_p:.1f}°C  H={h:.1f}%  P={p:.1f} hPa")
    sleep(2)
```

**Calibrating temperature (simple offset)**
```python
CPU_OFFSET = -3.0  # adjust to your setup after comparing with a real thermometer
temp = sense.get_temperature_from_humidity() + CPU_OFFSET
```

**Smoothing readings (moving average)**
```python
from collections import deque

window = deque(maxlen=5)

while True:
    t = sense.get_temperature_from_humidity()
    window.append(t)
    avg = sum(window) / len(window)
    print(f"avg temp={avg:.1f}°C")
    sleep(1)
```

**Pitfalls & tips**
- Readings are **floats**; round only when you print.  
- Always label **units** (°C, %, hPa).  
- Read less frequently to avoid heating the board (every 1–3 seconds is fine).

---

### 4) Handle joystick input (events and actions)
**Idea:** The mini‑stick is a 5‑way joystick: up/down/left/right/middle. You get events with `direction` and `action`.

```python
from sense_hat import SenseHat
from signal import pause

sense = SenseHat()

def on_any(event):
    # event.direction: 'up','down','left','right','middle'
    # event.action: 'pressed','held','released'
    print(f"{event.direction} - {event.action}")

sense.stick.direction_any = on_any
pause()  # keep the program alive
```

**Polling instead of callbacks**
```python
events = sense.stick.get_events()
for e in events:
    if e.action == "pressed" and e.direction == "left":
        print("Left!")
```

**Mini demo: move a pixel with the joystick**
```python
sense.clear()
x, y = 3, 3

def draw():
    sense.clear()
    sense.set_pixel(x, y, (255, 255, 255))

def on_any(e):
    global x, y
    if e.action != "pressed":
        return
    if e.direction == "up":    y = max(0, y-1)
    if e.direction == "down":  y = min(7, y+1)
    if e.direction == "left":  x = max(0, x-1)
    if e.direction == "right": x = min(7, x+1)
    draw()

draw()
sense.stick.direction_any = on_any
from signal import pause; pause()
```

**Pitfalls**
- If your program exits, you won’t see events. Keep it running with a loop or `pause()`.
- Handle only `pressed` to avoid repeated moves while held.

---

### 5) Read basic motion (accelerometer/gyroscope/orientation)
**Idea:** The IMU reports motion and orientation. You can get raw acceleration or fused orientation angles.

```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

# Enable sensors you care about (optional; all True by default)
sense.set_imu_config(compass=True, gyroscope=True, accelerometer=True)

while True:
    # Raw acceleration (in g’s)
    accel = sense.get_accelerometer_raw()
    x, y, z = accel["x"], accel["y"], accel["z"]

    # Orientation (degrees 0..360): pitch, roll, yaw
    o = sense.get_orientation()
    pitch, roll, yaw = o["pitch"], o["roll"], o["yaw"]

    print(f"accel x={x:.2f} y={y:.2f} z={z:.2f} | pitch={pitch:.1f} roll={roll:.1f} yaw={yaw:.1f}")
    sleep(0.2)
```

**Tilt‑to‑rotate text (orientation aware)**
```python
# Rotate display so text stays upright when you rotate the Pi
angle = 0
o = sense.get_orientation()
roll = o["roll"]
if roll > 315 or roll <= 45:   angle = 0
elif 45 < roll <= 135:         angle = 270
elif 135 < roll <= 225:        angle = 180
else:                           angle = 90
sense.set_rotation(angle)
sense.show_message("Aligned!")
```

**Pitfalls**
- Motion values can be noisy—consider smoothing.  
- Orientation depends on calibration; keep the HAT away from magnets/metal when using compass/yaw.

---

## Vocabulary
- LED matrix: 8×8 grid of colored LEDs you can set pixel-by-pixel.
- IMU: Inertial Measurement Unit; reports acceleration, rotation, orientation.
- Joystick: 5-way mini stick on the Sense HAT (up, down, left, right, press).
- Humidity sensor: Measures relative humidity (%RH).
- Pressure sensor: Measures air pressure (hPa or mbar).
- Orientation: Pitch/roll/yaw angles derived from the IMU.

## Check your understanding
1. Where is `(0,0)` on the LED grid, and what happens if you draw at `(8,8)`?  
2. Why might temperature read higher than room temperature, and how could you correct it?  
3. What two fields do joystick events have, and what do they represent?  
4. What’s the difference between `get_accelerometer_raw()` and `get_orientation()`?

---

## Try it: Mini‑projects

### A) Weather Badge
- Every 3 seconds, read temperature & humidity.  
- If `temp > 28°C`, flash a red “!” for 1 second, else show a green “✓”.  
- Stretch: Map humidity to LED brightness.

### B) Tilt‑Etch‑A‑Sketch
- Use accelerometer X/Y to move a “pen.”  
- Press the middle joystick to **clear**.

### C) Reaction Timer
- Show a random color. When it turns **green**, press joystick **middle** as fast as you can.  
- Print reaction time in milliseconds.

---

## Troubleshooting
- **`ModuleNotFoundError: No module named 'sense_hat'`** → Install with `sudo apt install sense-hat` and ensure you’re on Raspberry Pi OS.  
- **No LED output** → Reseat the HAT, try `sense.clear()`, check power.  
- **Joystick events not printing** → Keep the script running (`while True:` or `signal.pause()`); ensure you’re handling `pressed`.  
- **High temperature readings** → Use `_from_humidity/_from_pressure` and apply an offset; avoid reading too fast.  
- **Weird colors/too dim** → Bright colors can bloom; try lower values like `(120,0,0)` instead of `(255,0,0)`.

---

## Next up
Do the matching lab: **[02 – Sense HAT Basics](../Labs/02-sense-hat-basics.md)**

