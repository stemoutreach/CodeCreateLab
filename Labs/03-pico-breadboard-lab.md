
---
title: Pico Breadboard Lab — Button, LED, and (Optional) RGB/Ultrasonic
level: 03
estimated_time: 45–75 min
difficulty: Beginner
prereqs:
  - Guide: [03 – Raspberry Pi Pico Breadboarding](../Guides/03-pico-breadboarding.md)
rubric:
  - ✅ Must: Wire a **pushbutton** (input) and a **single LED** (output) and control the LED with the button
  - ✅ Must: Use **functions** (e.g., `normalize_input()`, `read_button()`, `show_status()`)
  - ✅ Must: Include basic **debounce** and clean exit on Ctrl‑C
  - ⭐ Stretch: Add an **RGB LED** (picozero.RGBLED), or read **HC‑SR04** distance and change color/behavior
---

# Goal
Build a small interactive circuit on a breadboard. Pressing the **button** should control an **LED**.  
Add at least **one** extension (RGB LED or ultrasonic distance sensor) if time permits.

## Materials
- Raspberry Pi Pico (or Pico W) + micro‑USB cable
- Breadboard, jumper wires
- **1× LED** and **1× 220–330Ω resistor**
- **1× pushbutton**
- *(Optional)* RGB LED (common cathode recommended) or **HC‑SR04** ultrasonic sensor

## Wiring (reference)
| Part | Pico GPIO | Notes |
|------|-----------|-------|
| LED anode (long leg) | **GP14** | LED cathode → resistor → **GND** |
| Pushbutton | **GP15** | Other side → **GND** (library will pull‑up) |
| RGB LED (optional) | **R=GP13, G=GP12, B=GP11** | Use `picozero.RGBLED(13,12,11)`; common‑cathode to GND |
| HC‑SR04 (optional) | **TRIG=GP10, ECHO=GP9** | ECHO must go to a **3V3‑safe** input |

> If your RGB LED is **common anode**, set `active_high=False` in `RGBLED(...)` or invert values.

## Steps
1) **Plan** — Sketch your wiring and pin choices; confirm resistor on LED.  
2) **Build** — Place parts and make connections; double‑check polarity and pins.  
3) **Code** — Start from the starter file below; run and verify button→LED behavior.  
4) **Test** — Try holding, tapping, and rapid presses to see debounce effects.  
5) **Iterate** — Add one extension (RGB LED color changes or distance‑based logic).

## Starter snippet (see full starter file below)
```python
from picozero import Button, LED
from time import sleep

button = Button(15)  # internal pull-up handled by library
led = LED(14)

def read_button():
    return button.is_pressed

def show_status(pressed: bool):
    led.on() if pressed else led.off()

try:
    while True:
        pressed = read_button()
        show_status(pressed)
        sleep(0.02)  # simple debounce
except KeyboardInterrupt:
    led.off()
    print("\nGoodbye!")
```

## Submission / Demo checklist
- [ ] Button **press** turns the LED **on**, release turns it **off** (or toggles—your choice, but be consistent).  
- [ ] Code uses **functions** and includes a **small debounce** delay.  
- [ ] Program exits cleanly on Ctrl‑C.

## Extensions (choose one or more)
- **RGB LED mode:** Use `RGBLED(13,12,11)` and set colors (e.g., green when pressed, fade when released).  
- **Distance mode:** Add HC‑SR04 and map distance to color (red=near, blue=mid, green=far).  
- **Buzzer:** Add a tone when pressed (use a PWM‑capable pin).  
- **Game:** Make a reaction‑time game; print milliseconds to beat.

## Troubleshooting
- **LED stays off** → Check LED orientation (long leg to GPIO), resistor to GND, and correct pin number.  
- **Button always “pressed”** → Make sure you’re using **opposite** legs of the switch; one side must go to **GND**.  
- **ImportError** on `picozero` → Ensure you’re running on the **Pico** with MicroPython/Thonny, not your PC Python.  
- **Nothing runs** → In Thonny, set Interpreter to **MicroPython (Raspberry Pi Pico)**.

## Reflection
In 2–3 sentences, describe how you’d modularize this code further (e.g., a `Device` class or config dict for pins).

## Next up
Continue to **[04 – PicoBot Maze Explorer](../Labs/04-picobot-maze-explorer.md)** if you’re building the robot.
