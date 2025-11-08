
# 03 — Pico Circuit Challenges (Breadboard Lab)

> ### Quick Summary
> **Level:** 03 • **Time:** 40–70 min  
> **Prereqs:** [Guide: 03 — Pico + Breadboarding](../Guides/03-pico-breadboarding.updated.md)  
> **Hardware:** Raspberry Pi Pico, breadboard, LED + resistor, pushbutton + resistor, (optional) RGB LED or active buzzer  
> **You’ll practice:** GPIO input/output, pull-ups/pull-downs, debouncing, simple patterns

# Why This Matters
This lab cements the basics you’ll use in every Pico project: read inputs safely and drive outputs predictably. Mastering these patterns prepares you for robot control and sensors.

---
## What you’ll learn
- Wire an LED and pushbutton correctly (with resistors)
- Configure pins as **IN** with **pull-ups/downs** or external resistors
- Debounce a button in software
- Drive an LED (and optional RGB/buzzer) with clean functions
- Structure a simple main loop

## Setup
> **Classroom default:** Raspberry Pi 500 + **Thonny**  
> Choose **MicroPython (Raspberry Pi Pico)** and save your file on the Pico as **`main.py`**.

---
# Steps
> 🆘 **Need a hint?** See the skeleton below and the wiring diagram in the **03 Guide**.

## 1) Wire LED + button
- LED on `GP15` (through resistor to GND) — adjust if your board labeling differs.  
- Button on `GP14` to 3.3V with a 10kΩ pull-down to GND (or use internal pull-up and wire accordingly).

**Discovery (pseudo-steps):**
- Read `button.value()` repeatedly; print transitions only.  
- Light LED only when the button is pressed.

## 2) Debounce
- Implement a simple debounce: ignore changes for ~30 ms after an edge.  
- Print “pressed” and “released” once per action.

## 3) Patterns
- Add `blink(times, on_ms, off_ms)` using `sleep_ms`.  
- Optional: if you have an **active buzzer**, add `beep(ms)` in parallel with LED.

## 4) Mini challenge
- While the button is held: **blink fast**.  
- When released: **blink slow** three times, then turn off.

---
## Skeleton Starter
```python
from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms

LED_PIN = 15
BTN_PIN = 14
DEBOUNCE_MS = 30

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)  # or Pin.PULL_UP if you wire to GND

last_state = 0
last_change = 0

def set_led(on: bool):
    led.value(1 if on else 0)

def blink(times=3, on_ms=200, off_ms=200):
    for _ in range(times):
        set_led(True); sleep_ms(on_ms)
        set_led(False); sleep_ms(off_ms)

def read_button_debounced():
    global last_state, last_change
    now = ticks_ms()
    raw = btn.value()
    if raw != last_state and ticks_diff(now, last_change) > DEBOUNCE_MS:
        last_state = raw
        last_change = now
        return raw  # edge detected
    return None     # no change

def main():
    try:
        while True:
            edge = read_button_debounced()
            if edge is None:
                sleep_ms(5)
                continue

            if edge == 1:  # pressed
                # fast blink while held
                set_led(True)
            else:          # released
                set_led(False)
                blink(times=3, on_ms=120, off_ms=120)
    except KeyboardInterrupt:
        pass
    finally:
        set_led(False)

if __name__ == "__main__":
    main()
```

---
## Testing & troubleshooting
- **LED won’t light:** check polarity; long leg to Pico, short leg to GND via resistor.  
- **Button bounces:** increase `DEBOUNCE_MS` or use hardware RC filter.  
- **Inverted logic:** if using `PULL_UP`, pressed might read `0`—invert accordingly.

## Submission checklist
- [ ] Debounced button logic (single press/release events)  
- [ ] LED control with `set_led()` and `blink()`  
- [ ] Challenge behavior implemented  
- [ ] Clean exit and LED off in `finally:`

## Rubric
- **Must:** stable input reading + LED output control  
- **Should:** clean function structure and debounce  
- **Stretch:** optional RGB/buzzer patterns or a tiny state machine
