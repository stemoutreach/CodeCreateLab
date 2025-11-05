# 03 — Pico Breadboarding

> ### Quick Summary
> **Level:** 03 • **Time:** 60–90 min  
> **Prereqs:** [00 — Python Basics](./00-python-basics.md), [01 — Functions](./01-python-functions.md)  
> **Hardware:** Raspberry Pi Pico (W ok), breadboard, jumper wires, LEDs, resistors, pushbutton, optional buzzer/speaker  
> **You’ll practice:** breadboard power rails, GPIO as input/output, pull-ups, debouncing, PWM for brightness/tone

# Why This Matters
Breadboarding lets you prototype quickly. You’ll wire LEDs and a button to the Pico, practice safe 3.3V wiring, and write MicroPython to control GPIO. These skills power every future robot build.

---
## What you’ll learn
- Identify breadboard rows, columns, and power rails
- Map Pico pins to GPIO numbers and 3.3V/VSYS/GND safely
- Drive an LED with a series resistor
- Read a pushbutton with an internal pull-up
- Use PWM to fade an LED and beep a buzzer/speaker
- Prevent common wiring mistakes (shorts, reversed polarity)

## Setup
This setup uses **MicroPython** on a Raspberry Pi Pico with **Thonny**. Flash the MicroPython UF2 once, then use **Run current script** in Thonny.

## Materials  (ONLY include if hardware is involved)
- Raspberry Pi Pico / Pico W (Micro-USB cable)
- Breadboard + jumper wires
- 1× LED (any color) + 1× 220–330 Ω resistor (series)
- 1× Momentary pushbutton
- Optional: Passive buzzer *or* small 8 Ω speaker

---
## Walkthrough — Step by Step (with explanations)

### 1) Power and a first LED
**Idea:** Light an LED using a GPIO pin and a resistor.
```python
from machine import Pin
import time

led = Pin(15, Pin.OUT)  # pick a GPIO you actually wired
while True:
    led.toggle()
    time.sleep(0.5)
```
**Anatomy:**
- Use a **series resistor** (220–330 Ω) to limit LED current.
- Long LED leg → GPIO (through resistor); short leg → GND.
**Common mistakes:**
- Skipping the resistor → overheated LED or pin.

### 2) Read a pushbutton (pull-up)
**Idea:** Use the Pico’s internal pull-up to read pressed/not pressed.
```python
from machine import Pin
button = Pin(14, Pin.IN, Pin.PULL_UP)  # pressed = 0, released = 1
print(button.value())
```
**Notes & pitfalls:**
- Wire one side of button to **GND**, the other to the GPIO.
- Logic is inverted with pull-up: pressed reads **0**.

### 3) Debounce and control an LED
**Idea:** Toggle LED only once per press.
```python
from machine import Pin
import time

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)

last = 1
while True:
    cur = button.value()
    if last == 1 and cur == 0:   # just pressed
        led.toggle()
        time.sleep(0.02)         # debounce
    last = cur
    time.sleep(0.005)
```
**Notes & pitfalls:**
- Mechanical switches bounce; add a short delay.

### 4) PWM: fade LED / play tone
**Idea:** Pulse‑width modulation controls brightness or sound.
```python
from machine import Pin, PWM
import time

pwm = PWM(Pin(13))  # choose the pin you wired
pwm.freq(1000)
for duty in range(0, 65535, 4096):
    pwm.duty_u16(duty)
    time.sleep(0.05)
pwm.deinit()
```
**Notes & pitfalls:**
- For a **passive buzzer/speaker**, set `pwm.freq(440)` to play A4.
- **Active buzzer** ignores frequency; it just beeps when powered.

---
## Vocabulary
- **Breadboard**: A prototyping board with connected rows/rails.
- **GPIO**: General‑purpose input/output pin on the Pico.
- **Pull‑up**: Resistor to 3.3V that makes the default state “1”.
- **PWM**: Rapid on/off to simulate analog control (brightness/tone).
- **Debounce**: Ignore rapid state changes from a mechanical switch.

---
## Check your understanding
1) Why must an LED have a series resistor?  
2) How do you wire a button for pull‑up reading?  
3) Why does a pressed pull‑up button read `0`?  
4) What does PWM control for LEDs and for speakers?  
5) What problem does debouncing solve?

---
## Try it: Mini-exercises
Build a **traffic light**: cycle Red → Yellow → Green with timing, and add a button to switch to **blinking yellow** mode.  
**Stretch goals:**
- Use PWM to fade between colors on an RGB LED.
- Play a short melody using a passive buzzer with different `freq()` values.

---
## Troubleshooting
- **Nothing lights** → Verify GND connection and resistor orientation; try another GPIO.  
- **Button always 1** → Wrong wiring: connect other leg to GND, or remove an external pull‑down that fights the pull‑up.  
- **No sound** → Passive buzzer needs a frequency; active buzzers just need power.

---
## Next up
**[03 – Pico Breadboarding](../Labs/03-pico-breadboarding.md)**
