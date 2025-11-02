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
## Meet the Raspberry Pi Pico (RP2040) — What it is & how code runs

**What is it?**  
The **Raspberry Pi Pico** is a tiny microcontroller board built around the **RP2040** chip.  
- Runs **MicroPython** or **C/C++** directly on the chip (no operating system).  
- **3.3V logic** only (never feed 5V into a GPIO pin).  
- ~**26 usable GPIO pins** for digital input/output; 3 pins support **analog input (ADC)**.  
- USB for **power** and **programming**.

**How code is loaded (two common ways):**  
1) **With Thonny (recommended for students)**  
   - In Thonny: *Tools → Options → Interpreter* → choose **MicroPython (Raspberry Pi Pico)**.  
   - Click **Save** and pick **“MicroPython device”** to place your file on the Pico.  
   - Files named **`main.py`** (and optionally `boot.py`) will **auto‑run** when the Pico powers up.

2) **USB “drag‑and‑drop” (UF2 bootloader)**  
   - **Hold** the **BOOTSEL** button on the Pico, then **plug in** USB.  
   - A drive called **RPI‑RP2** appears. Drag a **.uf2** firmware file to install MicroPython (done once).  
   - After MicroPython is installed, use Thonny to save your Python code as **`main.py`** on the Pico.

**What runs at power‑on?**  
- If a file named **`main.py`** is on the Pico, it runs automatically when you plug in power.  
- If there’s no `main.py`, connect Thonny and run your script from the editor.  
- To stop a stuck program, reconnect with Thonny and click **Stop**, or re‑enter BOOTSEL mode to manage files.

> **Pico vs Pico W:** On **Pico (non‑W)** the onboard LED is **GP25**. On **Pico W**, the LED is controlled by the Wi‑Fi chip; use `picozero.pico_led` so your code works on both.

---

## GPIO Map (numbering & special pins)

> **Quick view (not to scale).** Use this to learn **names and roles**; always check an official pinout when wiring new parts.

```
   USB connector
      ┌──────────────────────────────────────────────┐
Left  │ GP0 GP1  GND  GP2  GP3  GP4  GP5  GND  GP6  │  Right │ VBUS VSYS GND 3V3_EN 3V3  ADC_REF
side  │ GP7 GP8  GP9  GND  GP10 GP11 GP12 GP13 GP14 │  side  │ GP28 (ADC2)  GND  ADC_VREF 3V3  GP27 (ADC1)
      │ GP15 GP16 GP17 GP18 GP19 GP20 GP21 GP22 GP26│        │ GP26 (ADC0)  GND   RUN     GP24  GP25 (LED on Pico)
      └──────────────────────────────────────────────┘
```
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Insidebread.jpg" width="600" >
 
**Key points**
- **Digital GPIO:** `GP0`–`GP22` (most common for LEDs, buttons, drivers).  
- **Analog inputs (ADC):** `GP26`, `GP27`, `GP28`.  
- **Power & control:** multiple **GND** pins, **3V3**, **VBUS/VSYS**, **RUN**, `3V3_EN`.  
- **Onboard LED:** **GP25** (Pico only). Use `picozero.pico_led` to be portable across Pico and Pico W.

**Safety rules**
- GPIO pins are **3.3V max**. Use level shifting if a sensor outputs **5V**.  
- For LEDs: **series resistor** (220–330 Ω) between GPIO and GND path.  
- Never tie a driven GPIO directly to **3V3** or **GND**.

### GPIO basics (Pico)
- **Output**: the Pico **drives** the pin high (3.3 V) or low (0 V) → good for LEDs (with resistor).
- **Input**: the Pico **reads** the pin as pressed/not pressed, on/off, etc. → good for buttons and sensors.
- **Safety**: Avoid short circuits (never connect a GPIO directly to GND and drive it HIGH). Keep LED current modest.

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
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Insidebread.jpg" width="600" >

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
- **GPIO 14** → **resistor** → **LED long leg (anode)**  
- **LED short leg (cathode)**  → **GND**

```
GPIO14 ──► resistor ──► ( +| LED |− )  ──► GND
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
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/BlinkLED1.jpeg" width="600" >

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
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReadpushbuttonON.jpeg" width="600" >

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

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReactionGame.jpeg" width="600" >

**Extensions**
- Add a **too‑soon** penalty: if a button is pressed **before** the LED turns on, that player loses the round.
- Keep **best‑of‑3** scores.
- Use `time.ticks_ms()` to print reaction time in milliseconds.

---


### 6) RGB LED Blink (three pins + common pin)

**Goal:** Control an RGB LED by blinking colors and mixing red/green/blue.

**Parts & wiring**
- Use a **common cathode RGB LED** (recommended for beginners).  
- **Common cathode** → **GND** through a **single shared resistor** *or* one resistor **per color** (best practice).  
- Connect the three color pins to **three GPIOs** via resistors (e.g., 220–330 Ω each).

**Example wiring (per-color resistors)**
- **GPIO 16** → resistor → **R pin**  
- **GPIO 17** → resistor → **G pin**  
- **GPIO 18** → resistor → **B pin**  
- **Common cathode** → **GND**

> If your LED is **common anode**, connect the common pin to **3V3** and set `active_high=False` in `RGBLED(...)` (so the logic is inverted). RGBLED(red=16, green=17, blue=18, active_high=False)

**Code (based on picozero recipe: Blink)**
```python
from picozero import RGBLED
from time import sleep

# Common cathode: active_high=True (default)
led = RGBLED(red=16, green=17, blue=18)

# Simple blink through a few colors
while True:
    led.color = (1, 0, 0)   # red (1=on, 0=off) for each channel
    sleep(0.5)
    led.color = (0, 1, 0)   # green
    sleep(0.5)
    led.color = (0, 0, 1)   # blue
    sleep(0.5)
    led.off()
    sleep(0.5)
```

**Mix your own colors**
- Use **floats 0..1** for each channel: `(r, g, b)`  
- Example: purple ≈ `(1, 0, 0.4)`, cyan ≈ `(0, 1, 1)`, yellow ≈ `(1, 1, 0)`

```python
# Fade red up and down
for i in range(0, 11):
    led.color = (i/10, 0, 0)  # 0.0 → 1.0
    sleep(0.05)
for i in range(10, -1, -1):
    led.color = (i/10, 0, 0)
    sleep(0.05)
```

**Pitfalls & tips**
- RGB LEDs have **four legs**; the **longest** is usually the **common**. Check the datasheet or trial-and-error.  
- Use **one resistor per color** so brightness is consistent.  
- If colors look “inverted,” you likely have a **common anode** LED—set `active_high=False`.  
- Brightness varies by color (green/blue often look brighter); you can lower those channels slightly, e.g. `(1, 0.7, 0.6)`.

---

### 7) Ultrasonic Distance Sensor (HC-SR04) with picozero

**Goal:** Measure distance to an object using sound. The sensor sends a ping and measures the echo time.

**Safety & voltage note (important)**
- Many **HC-SR04** modules run on **5V** and return a **5V echo** signal, which can **damage** the Pico (3.3V max on inputs).  
- Solutions:
  1) Use a **voltage divider** on the **ECHO** line (e.g., **1 kΩ** to Pico + **2 kΩ** to GND, from the sensor’s echo output).  
  2) Use a **3.3V-safe module** (e.g., HC-SR04P) or a proper **level shifter**.  
  3) Some modules *may* work on 3.3V Vcc but are unreliable—prefer 5V with a **stepped-down echo**.

**Wiring (typical HC-SR04)**
- **VCC** → **5V** (or 3V3 if your module supports it)  
- **GND** → **GND**  
- **TRIG** → **GPIO 19**  
- **ECHO** → **voltage divider → GPIO 20** (see note above)

**Code (based on picozero recipe: Ultrasonic distance sensor)**
```python
from picozero import DistanceSensor
from time import sleep

# echo pin first, then trigger (picozero signature: DistanceSensor(echo, trigger))
sensor = DistanceSensor(echo=20, trigger=19)

while True:
    # distance is in meters
    d_m = sensor.distance
    d_cm = d_m * 100
    print(f"{d_cm:.1f} cm")
    sleep(0.2)
```

**Make it interactive (LED indicator)**
```python
from picozero import DistanceSensor, LED
from time import sleep

near_led = LED(14)  # reuse your LED circuit
sensor = DistanceSensor(echo=20, trigger=19)

THRESH_CM = 20

while True:
    if sensor.distance * 100 < THRESH_CM:
        near_led.on()
    else:
        near_led.off()
    sleep(0.05)
```

**Pitfalls & tips**
- Point the sensor **straight** at the target; soft or angled surfaces reflect poorly.  
- Minimum range is ~2–3 cm; maximum ~3–4 m for typical modules.  
- Avoid very fast polling; ~5–10 readings/second is plenty.  
- If readings seem random, check **ground common** between Pico and sensor, and verify the **ECHO** line is **3.3V-safe**.

### 8) Speaker (buzzer) & Play a Tune

**Goal:** Make sound for alerts and simple melodies.

**Which part do I need?**
- Prefer a **passive piezo buzzer** (works with tones of different frequencies).  
- An **active buzzer** has a built‑in oscillator—it only makes one fixed tone when powered. Use it for simple beeps.

**Basic wiring (passive piezo)**
- **GPIO 12** → **+** buzzer pin  
- **GND** → **–** buzzer pin  
> Passive piezos draw very little current and can be driven directly from a GPIO. For bigger speakers, use a driver (transistor).

**Code — quick beeps (picozero Speaker)**
```python
from picozero import Speaker
from time import sleep

sp = Speaker(14)

# Three short beeps
sp.beep(on_time=0.2, off_time=0.2, n=3)

# One long beep
sp.on()
sleep(0.5)
sp.off()
```

**Play a note by name or frequency**
```python
# Musical note (middle C in the 4th octave)
sp.play("C4", 0.4)     # note name, duration seconds

# Or play by frequency in Hz (A4 = 440 Hz)
sp.play_tone(440, 0.4)
```

**Play a short tune (list of notes)**
```python
from time import sleep

tune = [
    ("C4", 0.30), ("D4", 0.30), ("E4", 0.30), ("C4", 0.45),
    ("C4", 0.30), ("D4", 0.30), ("E4", 0.30), ("C4", 0.45),
    ("E4", 0.30), ("F4", 0.30), ("G4", 0.60),
]

for note, dur in tune:
    sp.play(note, dur)
    sleep(0.05)  # tiny gap between notes
```

**Tips & pitfalls**
- If it sounds quiet, try a different piezo or a **shorter wire run**. Passive piezos are not loud.  
- If you only get one constant tone regardless of `play()`/`play_tone()`, you probably have an **active** buzzer—use `sp.beep()` or swap for a passive piezo.  
- Keep melodies simple and short to avoid blocking your main loop (or move playback to its own loop/function).

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
