# Setup
- **Classroom default:** **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**
- Connect the **Pico** via micro‑USB
- Thonny → **Tools ▸ Options ▸ Interpreter** → **MicroPython (Raspberry Pi Pico)**; flash MicroPython if prompted
- Create `pico_breadboard_lab.py` in `~/Documents/CodeCreate/`, then **Run ▶** and watch the **Shell**

---


> ### Quick Summary
> **Level:** 03 • **Time:** 45–75 min  
> **Prereqs:** [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> **Hardware:** Raspberry Pi 500 + **Pico** + breadboard + components  
> **You’ll practice:** Buttons (input), LED & RGB (output), buzzer (PWM), ultrasonic distance

# Why This Matters

> **Learn → Try → Do**
> - **Learn** in the Guide
> - **Try** quick practice in the Guide
> - **Do** this Lab project
This lab turns basic I/O into an interactive gadget. You'll wire inputs and outputs and write small functions to keep your code tidy.

# What You’ll Build
A breadboarded gadget that reacts to a **button** and shows state with an **LED** or **RGB LED**, with optional **buzzer** tones and **ultrasonic** distance feedback.

# Outcomes
By the end you can:
- Read a **button** and debounce it
- Drive an **LED** and **RGB LED**
- Play a **buzzer** tone with PWM (optional)
- Measure distance with **HC‑SR04** (optional)
- Organize logic into small **functions** and exit cleanly

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

# Steps


> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/03-pico-breadboard-lab/STUDENT_START.md)**.

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/03-pico-breadboard-lab/STUDENT_START.md)**.

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


# Skeleton Starter
Use this **single** starter. Fill each **TODO**. No full solutions here.

```python
from picozero import Button, LED, RGBLED, Speaker
from time import sleep

# Pins
BTN_PIN = 15
LED_PIN = 14
RGB_PINS = (13, 12, 11)  # R,G,B

button = Button(BTN_PIN)
led = LED(LED_PIN)
rgb = RGBLED(*RGB_PINS)
# Optional buzzer (active speaker): if using a simple piezo, use PWM and set duty/frequency
try:
    buzzer = Speaker(10)  # optional; comment out if not present
except Exception:
    buzzer = None

# Optional HC-SR04 support (user to implement if available)
# TRIG=GP10, ECHO=GP9
# TODO: implement distance_cm() using machine.Pin + time_pulse_us or a helper library

def read_button() -> bool:
    """Return True if pressed (debounced via tiny sleep in loop)."""
    return button.is_pressed

def set_led(on: bool):
    led.on() if on else led.off()

def set_rgb(r: float, g: float, b: float):
    """Set RGBLED with 0..1 floats."""
    rgb.color = (r, g, b)

def beep(ms=100):
    if buzzer:
        try:
            buzzer.on()
            sleep(ms/1000)
            buzzer.off()
        except Exception:
            pass

def main():
    print("Pico Breadboard Lab — Button/LED/RGB (buzzer/ultrasonic optional)")
    while True:
        try:
            pressed = read_button()
            # TODO: Toggle or mirror LED state based on pressed
            # Example mirror:
            set_led(pressed)

            # TODO: If pressed: show green; else blue (or any scheme)
            set_rgb(0, 1, 0) if pressed else set_rgb(0, 0, 1)

            # TODO (optional): short beep when pressed transitions from False->True
            # Hint: track prev state

            # TODO (optional): if you implemented distance_cm(), map distance to a color

            sleep(0.02)  # simple debounce
        except KeyboardInterrupt:
            break
    # cleanup
    set_led(False); set_rgb(0,0,0)
    if buzzer: buzzer.off()
    print("Goodbye!")

if __name__ == "__main__":
    main()
```


# Demo / Submission Checklist
- [ ] Button → LED behavior works consistently (mirror or toggle; state explained)
- [ ] Code uses **functions** for I/O and includes a small **debounce**
- [ ] **RGB LED** changes color based on state (or a mode you designed)
- [ ] *(Optional)* **Buzzer** beeps on press transition (no stuck tone)
- [ ] *(Optional)* **Ultrasonic** reading affects color/printout
- [ ] Clean exit on **Ctrl‑C** (LEDs off)
