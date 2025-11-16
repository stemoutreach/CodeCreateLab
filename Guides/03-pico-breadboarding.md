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

> **Learn → Try**: Learn concepts here with tiny examples, then Try a quick practice before you Do the matching Lab.

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
- Find & adapt PicoZero [recipes](https://picozero.readthedocs.io/en/latest/recipes.html) (RGB LED, ultrasonic, buzzer)

## Materials
- Raspberry Pi Pico (W or non‑W)
- Breadboard, jumper wires
- **LED(s)** and **220–330Ω** resistors (one resistor **in series** with each LED)
- One **pushbutton** (tact switch)
- (Optional) RGB LED, buzzer, ultrasonic sensor (HC‑SR04)

---
## Meet the Raspberry Pi Pico (RP2040) — What it is & how code runs

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/5544-02.jpg" width="400" >

**What is it?**  
The **Raspberry Pi Pico** is a tiny microcontroller board built around the **RP2040** chip.  
- Runs **MicroPython** or **C/C++** directly on the chip (no operating system).  
- **3.3V logic** only (never feed 5V into a GPIO pin).  
- ~**26 usable GPIO pins** for digital input/output; 3 pins support **analog input (ADC)**.  
- USB for **power** and **programming**.
- [Getting started with Raspberry Pi Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)

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

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/picodiagram.jpg" width="400" >

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

  <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/PicoBreadboard.png" width="184" >    |    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Insidebread.jpg" width="195" > 

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

## Setup

_Classroom default: **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny**._

1. Connect the **Pico** via **micro‑USB**.
2. Open **Thonny** → **Tools ▸ Options ▸ Interpreter**.
   - Interpreter: **MicroPython (Raspberry Pi Pico)**
   - Port: **Automatic**
   - If prompted, let Thonny **install/flash MicroPython (UF2)** to the Pico.
3. **Save** your script on the Pico (or in `~/Documents/CodeCreate/`) and press **Run ▶**.

> Tip: Files named **`main.py`** on the Pico auto‑run on power‑up.

## Table of Contents (Walkthrough 1–8)

- [1) Blink the onboard LED](#1-blink-the-onboard-led)
- [2) Blink an external LED (with a resistor)](#2-blink-an-external-led-with-a-resistor)
- [3) Read a pushbutton (and avoid false presses)](#3-read-a-pushbutton-and-avoid-false-presses)
- [4) Mini-exercise Reaction Game (two players)](#4-mini-exercise-reaction-game-two-players)
- [4) Mini-exercise — Reaction Game (two players)](#4-mini-exercise--reaction-game-two-players)
- [5) RGB LED Blink (three pins + common pin)](#5-rgb-led-blink-three-pins--common-pin)
- [6) Ultrasonic Distance Sensor (HC-SR04) with picozero](#6-ultrasonic-distance-sensor-hc-sr04-with-picozero)
- [7) Speaker (buzzer) & Play a Tune](#7-speaker-buzzer--play-a-tune)




## Walkthrough — Step by Step (with explanations)
- `pico_led` is a ready‑made object for the tiny LED on the Pico board.  
- `sleep(0.5)` pauses for half a second.
- Press **Stop** in Thonny to end the loop.


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

**Try this:** Replace `0.5` with `0.1` (faster) or `1.0` (slower).

---


### Deploy to Pico (main.py)
> **Make it auto‑run:** Save your final script **to the Pico** as `main.py`. Unplug/replug USB or power the Pico — it runs automatically.
1. In **Thonny**: File → **Save as…** → **Raspberry Pi Pico**.
2. Name it **`main.py`** (this special name auto‑runs at boot).
3. Unplug/replug the Pico or power it from a battery/USB — your program starts by itself.

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
  <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/BlinkLED1.jpeg" width="380" >    |    <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/BlinkLED2.jpeg" width="400" > 


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
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReadpushbuttonON.jpeg" width="400" >

**What’s “debouncing”?** Real buttons can “chatter” (rapid on/off) when pressed.  
- A tiny delay (`sleep(0.02)`) smooths this.  
- For more control, use `button.when_pressed = handler` callbacks or track time between presses.

**Common pitfalls**
- Button wired on the **same side** instead of across the gap → it does nothing.
- Floating input: `picozero.Button` enables a pull‑up for you; if you use low‑level APIs later, you must set pull‑ups/downs yourself.

---

## Optional: Compare with low-level `machine.Pin`
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

### 4) Mini‑exercise Reaction Game (two players)
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


### 5) RGB LED Blink (three pins + common pin)

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
led = RGBLED(red=15, green=14, blue=13)

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

 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/RGBLED.jpeg" width="400" >

 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/RGBDiagram.JPG" width="400" >
 
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

### 6) Ultrasonic Distance Sensor (HC-SR04) with picozero

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
- **TRIG** → **GPIO 3**  
- **ECHO** → **voltage divider → GPIO 2** (see note above)

**Code (based on picozero recipe: Ultrasonic distance sensor)**
```python
from picozero import DistanceSensor
from time import sleep

# echo pin first, then trigger (picozero signature: DistanceSensor(echo, trigger))
sensor = DistanceSensor(echo=2, trigger=3)

while True:
    # distance is in meters
    d_m = sensor.distance
    d_cm = d_m * 100
    print(f"{d_cm:.1f} cm")
    sleep(0.2)
```
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Ultrasonic.jpeg" width="400" >


**Pitfalls & tips**
- Point the sensor **straight** at the target; soft or angled surfaces reflect poorly.  
- Minimum range is ~2–3 cm; maximum ~3–4 m for typical modules.  
- Avoid very fast polling; ~5–10 readings/second is plenty.  
- If readings seem random, check **ground common** between Pico and sensor, and verify the **ECHO** line is **3.3V-safe**.

### 7) Speaker (buzzer) & Play a Tune

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
from time import sleep
from picozero import Buzzer

buzzer = Buzzer(14)

buzzer.on()
sleep(1)
buzzer.off()
sleep(1)

buzzer.beep()
sleep(4)
buzzer.off()
```
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Speaker.jpeg" width="400" >

**Control a passive buzzer or speaker that can play different tones or frequencies:**
```python
from picozero import Speaker
from time import sleep

speaker = Speaker(14)

def tada():
    c_note = 523
    speaker.play(c_note, 0.1)
    sleep(0.1)
    speaker.play(c_note, 0.9)

def chirp():
    global speaker
    for _ in range(5):
        for i in range(5000, 2999, -100):
          speaker.play(i, 0.01)
        sleep(0.2)


try: 
    tada()
    sleep(1)
    chirp()
    
finally: # Turn the speaker off if interrupted
    speaker.off()
```

**Play a tune of note names and durations in beats:**
```python
from picozero import Speaker

speaker = Speaker(14)

BEAT = 0.25 # 240 BPM

liten_mus = [ ['d5', BEAT / 2], ['d#5', BEAT / 2], ['f5', BEAT], ['d6', BEAT], ['a#5', BEAT], ['d5', BEAT],  
              ['f5', BEAT], ['d#5', BEAT], ['d#5', BEAT], ['c5', BEAT / 2],['d5', BEAT / 2], ['d#5', BEAT], 
              ['c6', BEAT], ['a5', BEAT], ['d5', BEAT], ['g5', BEAT], ['f5', BEAT], ['f5', BEAT], ['d5', BEAT / 2],
              ['d#5', BEAT / 2], ['f5', BEAT], ['g5', BEAT], ['a5', BEAT], ['a#5', BEAT], ['a5', BEAT], ['g5', BEAT],
              ['g5', BEAT], ['', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT / 2], ['d6', BEAT / 2], ['c6', BEAT / 2],
              ['a#5', BEAT / 2], ['a5', BEAT / 2], ['g5', BEAT / 2], ['a5', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT],
              ['f5', BEAT], ['f5', BEAT], ['f5', BEAT / 2], ['d#5', BEAT / 2], ['d5', BEAT], ['f5', BEAT], ['d6', BEAT],
              ['d6', BEAT / 2], ['c6', BEAT / 2], ['b5', BEAT], ['g5', BEAT], ['g5', BEAT], ['c6', BEAT / 2],
              ['a#5', BEAT / 2], ['a5', BEAT], ['f5', BEAT], ['d6', BEAT], ['a5', BEAT], ['a#5', BEAT * 1.5]]

try:
    speaker.play(liten_mus)
       
finally: # Turn speaker off if interrupted
    speaker.off()
```
**Play individual notes and control the timing or perform another action:**
```python
from picozero import Speaker
from time import sleep

speaker = Speaker(14)

BEAT = 0.4

liten_mus = [ ['d5', BEAT / 2], ['d#5', BEAT / 2], ['f5', BEAT], ['d6', BEAT], ['a#5', BEAT], ['d5', BEAT],  
              ['f5', BEAT], ['d#5', BEAT], ['d#5', BEAT], ['c5', BEAT / 2],['d5', BEAT / 2], ['d#5', BEAT], 
              ['c6', BEAT], ['a5', BEAT], ['d5', BEAT], ['g5', BEAT], ['f5', BEAT], ['f5', BEAT], ['d5', BEAT / 2],
              ['d#5', BEAT / 2], ['f5', BEAT], ['g5', BEAT], ['a5', BEAT], ['a#5', BEAT], ['a5', BEAT], ['g5', BEAT],
              ['g5', BEAT], ['', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT / 2], ['d6', BEAT / 2], ['c6', BEAT / 2],
              ['a#5', BEAT / 2], ['a5', BEAT / 2], ['g5', BEAT / 2], ['a5', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT],
              ['f5', BEAT], ['f5', BEAT], ['f5', BEAT / 2], ['d#5', BEAT / 2], ['d5', BEAT], ['f5', BEAT], ['d6', BEAT],
              ['d6', BEAT / 2], ['c6', BEAT / 2], ['b5', BEAT], ['g5', BEAT], ['g5', BEAT], ['c6', BEAT / 2],
              ['a#5', BEAT / 2], ['a5', BEAT], ['f5', BEAT], ['d6', BEAT], ['a5', BEAT], ['a#5', BEAT * 1.5]]

try:
    for note in liten_mus:
        speaker.play(note)
        sleep(0.1) # leave a gap between notes
       
finally: # Turn speaker off if interrupted
    speaker.off()
```


**Tips & pitfalls**
- If it sounds quiet, try a different piezo or a **shorter wire run**. Passive piezos are not loud.  
- If you only get one constant tone regardless of `play()`/`play_tone()`, you probably have an **active** buzzer—use `sp.beep()` or swap for a passive piezo.  
- Keep melodies simple and short to avoid blocking your main loop (or move playback to its own loop/function).

## Vocabulary
- MicroPython: A lightweight Python for microcontrollers like the Pico.
- picozero: Beginner-friendly Python library for Pico GPIO (LEDs, buttons, etc.).
- GPIO: General-Purpose Input/Output pins used to read sensors or drive outputs.
- Pull-up / Pull-down: Resistor configuration that sets a default HIGH/LOW level.
- Breadboard rails: Long power strips along the sides (watch for split rails).
- Series resistor: Limits current through an LED to protect it and the Pico.

## Check your understanding
1. On a breadboard, which holes are connected together in a row? What does the center **gap** do?  
2. Why must an LED have a resistor, and where should it go in the circuit?  
3. What’s the difference between **GPIO input** and **output**? Give one example of each.  
4. What is **debouncing**, and why might your button appear to press multiple times?

---

## Try it: Mini-exercises
- Blink SOS (…) using `LED.on()`/`off()` and `sleep()`.
- Turn the LED on only while the button is held (no bouncing).
- Challenge: Add a second LED on a different pin and alternate them.

**Stretch**
- Use `Button.is_pressed` to count presses and show the count over serial.
- Add a “hold to exit” safety (e.g., hold the button 2 sec to stop a loop).

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

## Explore PicoZero  (pick 1–2 to try next)
- **RGB LED:** set colors with `(r, g, b)` values  
- **Buzzer:** play simple tones for game feedback  
- **Ultrasonic sensor (HC‑SR04):** measure distance in cm and trigger lights/sounds
- Find & adapt additional PicoZero [recipes](https://picozero.readthedocs.io/en/latest/recipes.html) 

> Tip: Start from a recipe, then adapt **pin numbers** to match your wiring and tweak delays/thresholds.

---

## Next up
Do the matching lab: **[03 – Pico Breadboard](../Labs/03-pico-breadboard.md)**
