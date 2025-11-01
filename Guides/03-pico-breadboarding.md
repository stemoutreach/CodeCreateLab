# Raspberry Pi Pico Breadboarding

> ### Quick Summary
> **Level:** 03 • **Time:** 60–90 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi Pico + micro‑USB cable; Breadboard, jumper wires, LEDs, pushbutton, resistors  
> **You’ll practice:**
> - setting up MicroPython/Thonny
> - understanding breadboard internals
> - using `picozero` for LEDs & buttons
> - safe wiring with resistors
> - debouncing
> - and adapting recipes

# Why This Matters
Breadboards let you prototype **electronics without soldering**. Pairing the **Raspberry Pi Pico** with MicroPython gives you instant results: blink LEDs, read buttons, and build mini‑games. Mastering these basics prepares you for sensors, buzzers, motors, and bigger projects.

---

## What you’ll learn
- Breadboard anatomy (power rails, rows, the “gap”)
- Resistors: why you need them for LEDs + a quick Ohm’s Law check
- GPIO basics: inputs vs outputs, pin numbering, and safety
- MicroPython on Pico with **Thonny** + the **picozero** library
- Blink the onboard LED, then an external LED
- Read a pushbutton reliably (debouncing concepts)
- Where to find & adapt PicoZero recipes (RGB LED, ultrasonic, buzzer)

## Materials
- Raspberry Pi Pico (W or non‑W)
- Breadboard, jumper wires
- **LED(s)** and **220–330Ω** resistors (one resistor **in series** with each LED)
- One **pushbutton** (tact switch)
- (Optional) RGB LED, buzzer, ultrasonic sensor (HC‑SR04)

---

## Breadboard & GPIO — The Big Picture

### Inside the breadboard
A breadboard is a grid of spring clips hidden under plastic. Certain holes are internally connected:

```
 Power rails (usually colored)          Main area (rows)
 ┌───────────┐  ┌───────────┐           Columns a b c d e  |  f g h i j
 │ +  +  +  +│  │ -  -  -  -│           Rows connect like this:
 │ +  +  +  +│  │ -  -  -  -│           a–e are connected together per row
 └───────────┘  └───────────┘           f–j are connected together per row
                                          a b c d e   gap   f g h i j
                                          ─────────   ---   ─────────
```

**Key rules**
- The long **power rails** run top‑to‑bottom (often split in the middle on some boards). Use them for **3V3** and **GND**.
- The **main rows** connect **horizontally** (five holes on each side of the **center gap**). The gap separates the left/right sides.
- Always double‑check that your LED & resistor are in **series** (in one continuous path from GPIO → LED → resistor → GND).

### Why a resistor for an LED?
LEDs need limited current. Without a resistor, too much current can flow and damage the LED or the Pico’s pin.

**Quick check (Ohm’s Law):**
- Pico GPIO is ~3.3 V
- Typical LED forward voltage ≈ 2.0 V (red) → Voltage across resistor ≈ 1.3 V
- Target current 5–10 mA → **R ≈ V / I** → 1.3 V / 0.01 A ≈ **130 Ω**
- Choose a common value **220–330 Ω** to be safe and bright enough.

### GPIO basics (Pico)
- **Output**: the Pico **drives** the pin high (3.3 V) or low (0 V) → good for LEDs (with resistor).
- **Input**: the Pico **reads** the pin as pressed/not pressed, on/off, etc. → good for buttons and sensors.
- **Safety**: Avoid short circuits (never connect a GPIO directly to GND and drive it HIGH). Keep LED current modest.

---

## Setup (MicroPython + Thonny)
1. Connect the **Pico** to your computer via **micro‑USB**.
2. Open **Thonny** → **Tools ▸ Options ▸ Interpreter**.
   - Interpreter: **MicroPython (Raspberry Pi Pico)**
   - Port: **Automatic**
3. The Thonny **Shell** should show `>>>` (MicroPython REPL).  
   If not, re‑select the interpreter or reconnect the cable.

> Tip: Save your scripts on the **Pico** (not your computer) so they can run without Thonny later.

---

## Walkthrough — Step by Step (with explanations)

### 1) Blink the onboard LED
**Why start here?** No wiring required—just verify code + interpreter.

```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```
- `pico_led` is a ready‑made object for the tiny LED on the Pico board.  
- `sleep(0.5)` pauses for half a second.
- Press **Stop** in Thonny to end the loop.

**Try this:** Replace `0.5` with `0.1` (faster) or `1.0` (slower).

---

### 2) Blink an external LED (with a resistor)
**Wiring (series path)**
- **GPIO 14** → **LED long leg (anode)**  
- **LED short leg (cathode)** → **resistor** → **GND**

```
GPIO14 ──► ( +| LED |− ) ──► resistor ──► GND
```

**Code**
```python
from picozero import LED
from time import sleep

led = LED(14)     # the GPIO number

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

**Check yourself**
- LED still dark? Flip it: the **long leg** should face the GPIO (through the series path).
- Confirm the resistor is **in series**, not in a different row by accident.
- Try `led.blink()` for a quick test (built‑in helper).

**Why GPIO 14?** Any digital GPIO works; 14 is just an example. If you change the wiring, update the number in code.

---

### 3) Read a pushbutton (and avoid false presses)
**Goal:** Light the LED only when the button is pressed.

**Wiring**
- One button leg → **GPIO 15**
- The opposite leg → **GND**  
(Place the button so the legs you use are on **opposite sides**—tact switches connect across the gap.)

**Code**
```python
from picozero import Button, LED
from time import sleep

button = Button(15)   # picozero handles the internal pull-up
led = LED(14)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
    sleep(0.02)  # small delay reduces switch bounce noise
```

**What’s “debouncing”?** Real buttons can “chatter” (rapid on/off) when pressed.  
- A tiny delay (`sleep(0.02)`) smooths this.  
- For more control, use `button.when_pressed = handler` callbacks or track time between presses.

**Common pitfalls**
- Button wired on the **same side** instead of across the gap → it does nothing.
- Floating input: `picozero.Button` enables a pull‑up for you; if you use low‑level APIs later, you must set pull‑ups/downs yourself.

---

### 4) Optional: Compare with low-level `machine.Pin`
`picozero` is beginner‑friendly. For advanced control, MicroPython’s `machine` gives you the raw pins.

```python
from machine import Pin
from time import sleep

led = Pin(14, Pin.OUT)
button = Pin(15, Pin.IN, Pin.PULL_UP)  # enable internal pull-up

while True:
    led.value(0 if button.value() else 1)  # pressed = 0 (to GND)
    sleep(0.02)
```
- Here, pressed means the input reads **0** (because it’s pulled to GND).  
- This mirrors what `picozero` configures automatically for you.

---

### 5) Mini‑exercise — Reaction Game (two players)
**Rules:** After a random wait, the LED turns on. First player to press wins.

**Wiring**
- **LED** on GPIO **14** (with resistor to GND)
- **Button 1** on GPIO **15** to GND
- **Button 2** on GPIO **17** to GND

**Code**
```python
from picozero import Button, LED
from time import sleep
import random

led = LED(14)
p1 = Button(15)
p2 = Button(17)

print("Get ready...")
sleep(random.uniform(2, 5))
led.on()

while True:
    if p1.is_pressed:
        print("Player 1 wins!")
        break
    if p2.is_pressed:
        print("Player 2 wins!")
        break

led.off()
```

**Extensions**
- Add a **too‑soon** penalty: if a button is pressed **before** the LED turns on, that player loses the round.
- Keep **best‑of‑3** scores.
- Use `time.ticks_ms()` to print reaction time in milliseconds.

---

## Check your understanding
1. On a breadboard, which holes are connected together in a row? What does the center **gap** do?  
2. Why must an LED have a resistor, and where should it go in the circuit?  
3. What’s the difference between **GPIO input** and **output**? Give one example of each.  
4. What is **debouncing**, and why might your button appear to press multiple times?

---

## Troubleshooting
- **LED never lights:**  
  - Flip the LED (long leg toward the GPIO path).  
  - Ensure the resistor is **in series** and not placed across the same row.  
  - Confirm pin number in code matches the GPIO you used.
- **Button always “pressed” or never pressed:**  
  - Make sure the button connects across the **gap** and one side goes to **GND**.  
  - If using low‑level pins, enable a **pull‑up** or **pull‑down**.
- **No `picozero` found / code runs on the computer instead of Pico:**  
  - In Thonny, set interpreter to **MicroPython (Raspberry Pi Pico)** and see `>>>` in the Shell.  
  - Save/run the file on the Pico.
- **Random resets / hot components:**  
  - Check for accidental **shorts** (e.g., GPIO driven HIGH directly to GND).  
  - Use one LED + resistor per GPIO; don’t draw too much current from a single pin.

---

## Explore PicoZero recipes (pick 1–2 to try next)
- **RGB LED:** set colors with `(r, g, b)` values  
- **Buzzer:** play simple tones for game feedback  
- **Ultrasonic sensor (HC‑SR04):** measure distance in cm and trigger lights/sounds

> Tip: Start from a recipe, then adapt **pin numbers** to match your wiring and tweak delays/thresholds.

---

## Next up
Do the matching lab: **[03 – Pico Breadboard Lab](../Labs/03-pico-breadboard-lab.md)**
