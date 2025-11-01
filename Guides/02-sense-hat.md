# Sense HAT

> ### Quick info
> **Level:** 02 • **Time:** 45–75 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)   
> **Hardware:** Raspberry Pi + Sense HAT   
> **You’ll practice:**
> - Install and import the Sense HAT Python library
> - Control the 8×8 LED matrix (text and pixels)
> - Read temperature, humidity, and pressure
> - Handle joystick input events
> - Use IMU readings (accelerometer/gyroscope) at a basic level

# Why This Matters
The Sense HAT adds real-world sensors and an 8×8 LED display to your Raspberry Pi. In this guide you’ll learn to display messages, read environment data, and react to joystick/IMU input—skills you’ll use in the matching lab, **Sense HAT Basics**.

## What you’ll learn
- Installing and importing `sense_hat`
- Showing text and pixels on the LED matrix
- Reading environmental sensors (temperature, humidity, pressure)
- Reading joystick events
- Basics of motion sensing (accelerometer/gyroscope)

## Setup
1. **Attach the Sense HAT** to the Raspberry Pi GPIO header.
2. **Install the library** (Raspberry Pi OS):
   ```bash
   sudo apt update
   sudo apt install -y sense-hat
   ```
3. **Quick test** (Python REPL):
   ```python
   from sense_hat import SenseHat
   sense = SenseHat()
   sense.show_message("Hi!")
   ```
   If you see scrolling text, you’re good to go.

## Walkthrough

### 1) Display text on the LED matrix
```python
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()
sense.show_message("Hello!", scroll_speed=0.08)  # lower = faster scroll
```

### 2) Set specific pixels (RGB tuples 0–255)
```python
from sense_hat import SenseHat
sense = SenseHat()

red = (255, 0, 0)
green = (0, 255, 0)

# Coordinates are x=0..7, y=0..7
sense.set_pixel(0, 0, red)
sense.set_pixel(7, 7, green)
```

### 3) Read environmental sensors
```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while True:
    t = sense.get_temperature()
    h = sense.get_humidity()
    p = sense.get_pressure()
    print(f"T={t:.1f}°C  H={h:.1f}%  P={p:.1f} mbar")
    sleep(2)
```

> Note: Temperature can read a bit high due to CPU heat. For better accuracy, consider offsets or moving the sensor away from the CPU.

### 4) Handle joystick input
```python
from sense_hat import SenseHat
from signal import pause

sense = SenseHat()

def on_any(event):
    print(f"{event.direction} - {event.action}")
    # event.direction: up/down/left/right/middle
    # event.action: pressed/held/released

sense.stick.direction_any = on_any
pause()  # keep the program running to receive events
```

### 5) Read basic motion (accelerometer)
```python
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while True:
    accel = sense.get_accelerometer_raw()
    x, y, z = accel["x"], accel["y"], accel["z"]
    print(f"x={x:.2f}  y={y:.2f}  z={z:.2f}")
    sleep(0.2)
```

## Check your understanding
1. What does `set_pixel(x, y, (r,g,b))` do if `x` or `y` is outside 0–7?
2. Why might the reported temperature be higher than the room temperature?
3. What two fields does a joystick event provide and what do they represent?

## Try it: Mini‑exercise
Build a **Weather Blinker**:
- Every 2 seconds, read temperature and humidity.
- If `temp > 28°C` show a red “!” for one second; otherwise show a green “✓”.
- Use `show_message()` or a custom 8×8 pixel pattern function.

> Stretch: Map humidity to LED brightness or color (drier = dim/blue, humid = bright/cyan).

## Troubleshooting
- **`ModuleNotFoundError: No module named 'sense_hat'`** → Recheck install (`sudo apt install sense-hat`), and that you’re on Raspberry Pi OS.
- **No LED output** → Verify HAT is seated correctly; try `sense.clear()` first. Check power supply.
- **Joystick events not printing** → Ensure your program keeps running (e.g., `while True:` or `signal.pause()`), not exiting immediately.
- **High temperature readings** → Apply a calibration offset or add a short idle before reading to reduce CPU heat influence.

## Next up
Do the matching lab: **[02 – Sense HAT Basics](../Labs/02-sense-hat-basics.md)**

