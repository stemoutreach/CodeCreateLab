
# 02.5 — Sense HAT Mission Dashboard (Advanced)

> ### Quick Summary
> **Level:** 02.5 • **Time:** 45–75 min  
> **Prereqs:** [Guide: 02 — Sense HAT Basics](../Guides/02-sense-hat.updated.md), [Lab: 02 — Sense HAT Basics](./02-sense-hat-basics.md)  
> **Hardware:** Raspberry Pi 500 (or Pi 4/5) with Sense HAT  
> **You’ll practice:** joystick events, multi-screen UI, sensor polling loop, icons, thresholds, tiny dashboard patterns

# Why This Matters
You’ll turn basic sensor reads into a tiny dashboard experience—switch screens with the joystick, show icons, and balance refresh rates so your UI stays responsive. These are the same patterns you’ll use later for more complex UIs.

---
## What you’ll learn
- Read and debounce **joystick** events to change modes/screens
- Poll **temperature**, **humidity**, and **pressure** without freezing the UI
- Draw simple **icons** and **bar indicators** on the 8×8 LED matrix
- Implement **threshold colors** and **units** consistently
- Make a responsive **main loop** with a target refresh rate (~5–10 Hz)

## Setup
> **Classroom default:** Raspberry Pi 500 + **Thonny**  
> Use the regular **Python 3 (Local)** interpreter for Sense HAT work.

1. Verify Sense HAT orientation and I²C is enabled.  
2. Open a new Python file for this lab (you can name it `mission_dashboard.py`).

---
# Steps
> 🆘 **Need a hint?** Start from your previous lab and add the **Joystick + Modes** pieces shown in the skeleton below.

## 1) Define dashboard modes & icons
- Create `MODES = ["Temp", "Humidity", "Pressure"]`.  
- For each mode, design a tiny 8×8 icon (e.g., thermometer, water drop, barometer).

**Discovery (pseudo-steps):**
- Draw a simple *one-color* icon first.  
- Add color logic (e.g., green/yellow/red) based on thresholds.

## 2) Read sensors and compute display values
- Temperature in °C (round to 1 decimal).  
- Humidity in % (round to whole number).  
- Pressure in hPa (round to nearest 1).

## 3) Joystick navigation
- Left/Right: previous/next mode  
- Press: toggle “number overlay” (show live value as a small text overlay or on a single row).

## 4) Main loop & refresh rate
- Target ~5–10 FPS.  
- Keep the loop responsive (don’t `sleep` for too long).  
- Use a simple state machine: **mode**, **show_overlay**, **last_read_time**.

## 5) Stretch goals (optional)
- Add a **mini bar** along the bottom that scales with value.  
- Create a **4th mode** for “All” that cycles Temp → Humidity → Pressure automatically.

---
## Skeleton Starter
```python
# Sense HAT Mission Dashboard (Advanced)
# Run with: Python 3 (Local) on Raspberry Pi OS

from sense_hat import SenseHat
from time import time, sleep

sense = SenseHat()
sense.low_light = True

# === MODES ===
MODES = ["Temp", "Humidity", "Pressure"]
mode_idx = 0
show_overlay = True

# === ICON COLORS ===
R = (255, 0, 0); Y = (255, 170, 0); G = (0, 180, 0); B = (0, 0, 200)
K = (0, 0, 0)

def temp_icon(color):
    """TODO: return 64-length list of pixels for a thermometer."""
    # Hint: start with all K, draw a red column, bulb, and tick marks
    return [K]*64

def humidity_icon(color):
    """TODO: water drop icon in 'color'."""
    return [K]*64

def pressure_icon(color):
    """TODO: barometer icon in 'color'."""
    return [K]*64

def thresholds_for(mode, value):
    """Return a color for the icon based on thresholds."""
    if mode == "Temp":
        # Example thresholds (°C)
        if value < 18: return B
        if value <= 27: return G
        return R
    if mode == "Humidity":
        # Example thresholds (%)
        if value < 30: return Y
        if value <= 60: return G
        return R
    if mode == "Pressure":
        # Example thresholds (hPa)
        if value < 990: return Y
        if value <= 1020: return G
        return R
    return G

def read_values():
    t = round(sense.get_temperature(), 1)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())
    return t, h, p

def render(mode, value, color, overlay):
    # TODO: choose proper icon per mode and draw it
    # TODO: if overlay, briefly show numeric value using show_message or a row
    sense.set_pixels(temp_icon(color))  # placeholder

def on_joystick_event(event):
    global mode_idx, show_overlay
    if event.action != "pressed":
        return
    if event.direction == "right":
        mode_idx = (mode_idx + 1) % len(MODES)
    elif event.direction == "left":
        mode_idx = (mode_idx - 1) % len(MODES)
    elif event.direction == "middle":
        show_overlay = not show_overlay

def main():
    sense.stick.direction_any = on_joystick_event

    target_fps = 8
    target_dt = 1.0 / target_fps
    last = 0.0

    try:
        while True:
            now = time()
            if now - last >= target_dt:
                last = now
                t, h, p = read_values()
                mode = MODES[mode_idx]
                value = t if mode == "Temp" else h if mode == "Humidity" else p
                color = thresholds_for(mode, value)
                render(mode, value, color, show_overlay)
            sleep(0.01)  # keep loop responsive
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

if __name__ == "__main__":
    main()
```

---
## Testing & troubleshooting
- **Laggy UI:** reduce icon recompute, limit `show_message` usage.  
- **Colors too bright:** set `sense.low_light = True`.  
- **Wrong values:** confirm environment warm-up (temp spikes right after boot).

## Submission checklist
- [ ] Three modes with working joystick navigation  
- [ ] Icons + threshold colors for each mode  
- [ ] Live numeric overlay toggle  
- [ ] Smooth updates (~5–10 FPS), no freezing  
- [ ] Clean exit (KeyboardInterrupt) and `sense.clear()`

## Rubric
- **Must:** 3 modes, sensor reads, joystick navigation, stable loop  
- **Should:** threshold coloring + overlay  
- **Stretch:** bar indicator or auto-cycle “All” mode
