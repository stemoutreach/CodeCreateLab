# Raspberry Pi Pico Breadboarding

> ### Quick Summary  
> **Level:** 03 • **Time:** 60–90 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi Pico + micro-USB cable; breadboard, jumper wires, LEDs, pushbuttons, RGB LED, ultrasonic sensor (HC-SR04P), passive buzzer or small speaker, 0.96" I2C OLED  
> **You’ll practice:** blink LEDs, read buttons with debouncing, mix RGB colors, measure distance with ultrasonic, play tones on a buzzer, draw text on an I2C OLED display  

> **Learn → Try:** Learn concepts here with tiny examples, then try mini-exercises before you do the matching Lab.

# Why This Matters
Breadboards let you prototype **electronics without soldering**. Pairing the **Raspberry Pi Pico** with MicroPython gives you instant feedback: blink LEDs, read buttons, measure distance, make sounds, and show messages on a tiny screen. Mastering these basics prepares you for sensors, buzzers, motors, and bigger robot projects.

---

## What you’ll learn
- Breadboard anatomy (power rails, rows, and the center “gap”).  
- GPIO basics: inputs vs outputs, pin numbering, and 3.3 V safety.  
- Using MicroPython with **Thonny** and the **picozero** library.  
- Controlling onboard and external LEDs, including RGB color mixing.  
- Reading pushbuttons reliably and understanding **debouncing**.  
- Measuring distance with an **HC-SR04P** ultrasonic sensor.  
- Playing beeps and tones on a passive buzzer or small speaker.  
- Displaying text and simple graphics on a **0.96" SSD1306 I2C OLED**.

## Table of Contents (Walkthrough 1–8)

- [1) Blink LEDs (onboard and external)](#1-blink-leds-onboard-and-external)
- [3) Read pushbuttons](#2-read-pushbuttons)
- [3) RGB LED color mixing](#3-rgb-led-color-mixing)
- [4) Ultrasonic Distance Sensor](#4-ultrasonic-distance-sensor)
- [5) Speaker](#5-speaker)
- [6) OLED Display](#6-oled-display)



## Setup
_Classroom default: **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**._

1. Connect the **Pico** via **micro-USB** to the Raspberry Pi 500.  
2. Open **Thonny** → **Tools ▸ Options ▸ Interpreter**:  
   - Interpreter: **MicroPython (Raspberry Pi Pico)**  
   - Port: **Automatic**  
   - If prompted, let Thonny **install/flash MicroPython (UF2)** to the Pico.  
3. In Thonny, create a folder like `~/Documents/CodeCreate/`.  
4. Save your script there **or** directly on the Pico (File → Save as… → **Raspberry Pi Pico**).  
5. Press **Run ▶** to execute your code.  

> Tip: A file named **`main.py`** saved on the Pico will **auto-run** whenever the Pico powers up.

## Materials  (hardware)
- **Raspberry Pi Pico** (W or non-W)  
- **Breadboard** and jumper wires  
- **2× pushbutton** (tact switch), plus optional **second button**  
- **1× single-color LED** (+ resistor if needed; many kits include pre-resisted LEDs)  
- **1× common cathode RGB LED**  
- **HC-SR04P** ultrasonic distance sensor (3.3–5 V version)  
- **Passive piezo buzzer or small speaker**  
- **0.96" I2C OLED display** (SSD1306, 128×64, 4-pin VCC/GND/SCL/SDA)  

> ⚠️ **Safety note:** Pico GPIO pins are **3.3 V only**. Never feed 5 V into a GPIO. Always share a common **GND** between Pico and sensors.

---

## Walkthrough — Step by Step (with explanations)

We’ll build up features in small steps:

1. Meet the Pico, GPIO, and breadboard.  
2. Blink LEDs (onboard + external).  
3. Read pushbuttons and build a reaction game.  
4. Use an RGB LED for color mixing.  
5. Measure distance and add simple sound feedback.  
6. Show “Hello, world!” on a 0.96" I2C OLED.

### Standard pin map used in this guide

We’ll use this **standard map** so the Lab and Guide match:

```python
# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN = 13        # main pushbutton
BUTTON2_PIN = 15       # second button for reaction game
RGB_R_PIN = 17
RGB_G_PIN = 18
RGB_B_PIN = 19
SPEAKER_PIN = 20       # passive buzzer / speaker

# OLED Display (0.96" I2C 128x64, SSD1306)
OLED_SDA_PIN = 0       # I2C0 SDA
OLED_SCL_PIN = 1       # I2C0 SCL
```

You can copy this at the top of your program and use the names instead of raw pin numbers.

---

### Meet the Pico, GPIO, and breadboard

**Idea:** Before wiring anything, understand what the Pico is, what GPIO pins do, and how the breadboard’s hidden connections work.

#### The Raspberry Pi Pico (RP2040) — what it is & how code runs

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/5544-02.jpg" width="400" alt="Raspberry Pi Pico microcontroller board top view" >

- The **Raspberry Pi Pico** is a tiny microcontroller board based on the **RP2040** chip.  
- It runs **MicroPython** or **C/C++** directly on the chip (no full operating system).  
- Uses **3.3 V logic only** (never feed 5 V into a GPIO pin).  
- ~**26 usable GPIO pins** for digital I/O; 3 pins support **analog input (ADC)**.  
- Its **USB port** is used for both **power** and **programming**.

**How code is loaded (Thonny way):**

- Thonny connects to the Pico and runs code line by line or from a saved file.  
- If you save your program as **`main.py`** on the Pico, it will **run automatically** when powered.

> **Pico vs Pico W:** On Pico (non-W) the onboard LED is **GP25**. On Pico W, the LED is controlled by the Wi-Fi chip. Use `picozero.pico_led` so your code works on both.

#### GPIO map (numbering & special pins)

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/picodiagram.jpg" width="200" alt="Raspberry Pi Pico pinout diagram" >

Key facts:

- **Digital GPIO:** `GP0`–`GP22` are used for LEDs, buttons, sensors, etc.  
- **Analog inputs (ADC):** `GP26`, `GP27`, `GP28`.  
- **Power & control:** multiple **GND** pins, **3V3(OUT)**, **VBUS/VSYS**, **RUN**, `3V3_EN`.  
- **Onboard LED:** typically **GP25** (use `picozero.pico_led` to hide the difference between Pico and Pico W).

**Safety rules**

- GPIO pins are **3.3 V max**. If a sensor outputs 5 V, you must use a **level shifter** (or pick a 3.3-V-safe version like HC-SR04P).  
- Never tie a driven GPIO directly to **3V3** or **GND**; that can short the pin.  
- Always share a **common ground** (GND) between the Pico and all connected parts.

#### Inside the breadboard

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/PicoBreadboard.png" width="184" alt="Raspberry Pi Pico plugged into a breadboard" > <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Insidebread.jpg" width="195" alt="Diagram showing how breadboard rows and columns connect internally" >

- Long **power rails** run along the edges (often marked **+** and **–**).  
- **Rows of 5 holes** are connected **horizontally** on each side of the **center gap**.  
- The **gap** in the middle separates left and right sides—perfect for placing ICs or the Pico so pins don’t short together.

**Notes & pitfalls**

- Some breadboards have power rails that are **split in the middle**—check continuity or the printed marks.  
- If something doesn’t work, it’s often just a wire in the wrong **row** or **side of the gap**.

---

### 1) Blink LEDs (onboard and external)

**Idea:** First, prove your setup works with the **onboard LED**. Then move that idea to an **external LED** on the breadboard.

#### Onboard LED blink

```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```

- `pico_led` is a ready-made object connected to the on-board LED.  
- `sleep(0.5)` pauses the program for half a second.

**Try this:** Change `0.5` to `0.1` (faster) or `1.0` (slower).

#### External LED blink

**Wiring (series path)**

- Pico **GPIO 14** → **LED long leg (anode)**  
- LED **short leg (cathode)** → **GND**  

```text
GPIO14 ──► ( +| LED |− ) ──► GND
```

**Code**

```python
from picozero import LED
from time import sleep

led = LED(14)     # GPIO number for the external LED

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/LEDPico.jpeg" width="380" alt="External LED wired to a breadboard and Pico" >  


**Notes & pitfalls**

- If the LED never lights, flip it: the **long leg** should face the GPIO (through a resistor or pre-resisted LED).  
- Double-check that **GPIO number in code** matches your wiring.  
- Press **Stop** in Thonny to break out of the infinite loop.

---

### 2) Read pushbuttons

**Idea:** Use a pushbutton as **input** to control an LED. Learn how to avoid “noisy” reads (debouncing).

**Wiring**

- One button leg → **GPIO 13** 
- Opposite leg → **GND**  

Make sure the two legs you use are on **opposite sides of the switch**, across the breadboard gap.

**Code**

```python
from picozero import Button, LED
from time import sleep

button = Button(13)  
led = LED(14)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
    sleep(0.02)       # small delay reduces switch bounce noise
```

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/button.JPG" width="400" alt="Pushbutton and LED wired on a breadboard to the Pico" >

**What’s debouncing?**

When you press a real button, the contacts **“chatter”** for a few milliseconds, causing multiple quick on/off transitions.

- A short delay like `sleep(0.02)` smooths this out.  
- For more advanced control you can use `button.when_pressed = handler` or track timestamps.

#### Optional: compare with low-level `machine.Pin`

```python
from machine import Pin
from time import sleep

led = Pin(14, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    # button.value() is 0 when pressed, 1 when released
    led.value(0 if button.value() else 1)
    sleep(0.02)
```

`picozero` hides some of this complexity for you, but later you might want the full power of `machine.Pin`.

---

#### Mini reaction game (two players)

**Goal:** After a random wait, the LED turns on. The **first** player to press their button wins.

**Extra wiring**

- **Button 1** on GPIO **13** to GND.  
- **Button 2** on GPIO **15** to GND.

**Code**

```python
from picozero import Button, LED
from time import sleep
import random

led = LED(14)
p1 = Button(13)   # player 1
p2 = Button(15)   # player 2

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
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/game.JPG" width="380" >  


**Notes & pitfalls**

- If a button “does nothing”, it might be wired **on the same side** of the switch instead of across the gap.  
- `picozero.Button` enables an internal **pull-up** for you; the input reads **HIGH** when not pressed and **LOW** when pressed (connected to GND).

### 3) RGB LED color mixing

**Idea:** Use three GPIO pins to control the red, green, and blue channels of an **RGB LED**, then mix your own colors.

**Parts & wiring**

- Use a **common cathode** RGB LED (recommended).  
- **Common cathode** → **GND**.  
- Connect the three color legs to three GPIO pins:

- **GPIO 17** → R pin 
- **GPIO 18** → G pin  
- **GPIO 19** → B pin  

> If your LED is **common anode**, connect the common pin to **3V3** and set `active_high=False` when creating the `RGBLED`.

**Code (blink through basic colors)**

```python
from picozero import RGBLED
from time import sleep

led = RGBLED(red=17, green=18, blue=19) 

while True:
    led.color = (1, 0, 0)   # red
    sleep(0.5)
    led.color = (0, 1, 0)   # green
    sleep(0.5)
    led.color = (0, 0, 1)   # blue
    sleep(0.5)
    led.off()
    sleep(0.5)
```

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/rgbled2.jpeg" width="400" alt="RGB LED connected to Pico on a breadboard" >  
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/RGBDiagram.JPG" width="400" alt="Diagram of RGB LED legs and common cathode connection" >

**Mix your own colors**

Use **floats from 0.0 to 1.0** for each channel:

```python
# Fade red up and down
for i in range(0, 11):
    led.color = (i / 10, 0, 0)
    sleep(0.05)

for i in range(10, -1, -1):
    led.color = (i / 10, 0, 0)
    sleep(0.05)
```

Examples: purple ≈ `(1, 0, 0.4)`, cyan ≈ `(0, 1, 1)`, yellow ≈ `(1, 1, 0)`.

**Notes & pitfalls**

- RGB LEDs have **four legs**; the **longest leg** is usually the common pin (GND for common cathode).  
- If colors look **inverted**, you probably have a **common anode** LED—use `active_high=False`.  
- Different colors may have different brightness; you can reduce green/blue a bit for a nicer balance.

---

### 4) Ultrasonic Distance Sensor

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
- **TRIG** → **GPIO 10**  
- **ECHO** → **voltage divider → GPIO 11** (see note above)

**Code (based on picozero recipe: Ultrasonic distance sensor)**
```python
from picozero import DistanceSensor
from time import sleep

# echo pin first, then trigger (picozero signature: DistanceSensor(echo, trigger))
sensor = DistanceSensor(echo=11, trigger=10)

while True:
    # distance is in meters
    d_m = sensor.distance
    d_cm = d_m * 100
    print(f"{d_cm:.1f} cm")
    sleep(0.2)
```
<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/distancepico.jpeg" width="400" >


**Pitfalls & tips**
- Point the sensor **straight** at the target; soft or angled surfaces reflect poorly.  
- Minimum range is ~2–3 cm; maximum ~3–4 m for typical modules.  
- Avoid very fast polling; ~5–10 readings/second is plenty.  
- If readings seem random, check **ground common** between Pico and sensor, and verify the **ECHO** line is **3.3V-safe**.

### 5) Speaker

**Goal:** Make sound for alerts and simple melodies.

**Which part do I need?**
- Prefer a **passive piezo buzzer** (works with tones of different frequencies).  
- An **active buzzer** has a built‑in oscillator—it only makes one fixed tone when powered. Use it for simple beeps.

**Basic wiring (passive piezo)**
- **GPIO 20** → **+** buzzer pin  
- **GND** → **–** buzzer pin  
> Passive piezos draw very little current and can be driven directly from a GPIO. For bigger speakers, use a driver (transistor).

**Code — quick beeps (picozero Speaker)**
```python
from time import sleep
from picozero import Buzzer

buzzer = Buzzer(20)

buzzer.on()
sleep(1)
buzzer.off()
sleep(1)

buzzer.beep()
sleep(4)
buzzer.off()
```
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/picospeaker.jpeg" width="400" >

**Control a passive buzzer or speaker that can play different tones or frequencies:**
```python
from picozero import Speaker
from time import sleep

speaker = Speaker(20)

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

speaker = Speaker(20)

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

speaker = Speaker(20)

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

---

### 6) OLED Display

**Idea:** Connect a small **I2C OLED display** and show a message. This is a great way to see sensor readings without a computer.

Most 0.96" OLED modules:

- Use the **SSD1306** controller.  
- Speak over **I2C** using just two data lines: **SDA** (data) and **SCL** (clock).  
- Have **4 pins**: VCC, GND, SCL, SDA.

We’ll use **I2C0** on `GP0` (SDA) and `GP1` (SCL).

#### Wiring

Use the same power rails you already set up for other parts:

- **OLED VCC** → **Pico 3V3(OUT)**  
- **OLED GND** → **Pico GND**  
- **OLED SCL** → **Pico GP1** 
- **OLED SDA** → **Pico GP0** 

```text
Pico 3V3(OUT)  ----->  VCC   (OLED)
Pico GND       ----->  GND   (OLED)
Pico GP1       ----->  SCL
Pico GP0       ----->  SDA
```

 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/Display.jpeg" width="400" >

> ✅ Most SSD1306 boards accept **3.3–5 V** on VCC. Always confirm before wiring.

#### Make sure you have the `ssd1306` driver

This example expects a file named **`ssd1306.py`** to be on the Pico.

- In class, your mentor may pre-load this file.  
- Otherwise, open `ssd1306.py` in Thonny, then **File → Save as… → Raspberry Pi Pico** and name it `ssd1306.py`.

You only need to do this **once** per Pico.

#### Hello World code

```python
from machine import Pin, I2C
import ssd1306
from time import sleep

# Match the standard map
OLED_SDA_PIN = 0
OLED_SCL_PIN = 1

# I2C0 on GP0 (SDA) and GP1 (SCL)
i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN))

# Most 0.96" OLEDs use 128x64 pixels and address 0x3C
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear the screen (fill with 0 = black)
oled.fill(0)

# Draw some text at (x=0, y=0)
oled.text("Hello, world!", 0, 0)

# You must call show() to update the display
oled.show()

# Keep program alive so display stays on
while True:
    sleep(1)
```

**What’s happening?**

- `I2C(0, scl=Pin(1), sda=Pin(0))` sets up the hardware I2C bus.  
- `SSD1306_I2C(128, 64, i2c, addr=0x3C)` knows the display size and I2C address.  
- `oled.fill(0)` clears the buffer; `oled.text()` writes into the buffer.  
- `oled.show()` transfers the buffer to the screen.

**Notes & pitfalls**

- Nothing shows? Check VCC, GND, and that SDA/SCL are not swapped.  
- If you get `ImportError: no module named 'ssd1306'`, the driver file is not on the Pico.  
- Some boards use address `0x3D` instead of `0x3C`—try changing the `addr` if needed.

---

## Vocabulary
- **MicroPython:** A lightweight version of Python that runs directly on microcontrollers like the Pico.  
- **picozero:** Beginner-friendly library that wraps common Pico hardware (LEDs, buttons, sensors) into simple Python objects.  
- **GPIO (General-Purpose Input/Output):** Pins you can use to send signals out (outputs) or read signals in (inputs).  
- **Breadboard rails:** Long strips of connected holes along the sides, usually used for 3V3 and GND.  
- **Debouncing:** Smoothing out the rapid on/off “chatter” when a real button is pressed or released.  
- **I2C:** A two-wire communication bus (SDA + SCL) used to talk to smart devices like displays and sensors.  
- **Ultrasonic sensor:** A device that sends high-frequency sound pulses and measures how long the echo takes to return to estimate distance.  
- **Buzzer / Speaker:** Output device that turns electrical signals into sound; passive buzzers can play different tones, active ones usually make one fixed beep.  
- **OLED (Organic LED) display:** A small, bright screen where each pixel lights up individually—great for text and simple graphics.  
- **Pull-up resistor:** Keeps an input pin at a stable HIGH level until a button or sensor pulls it down to LOW.

---

## Check your understanding

1. On a breadboard, which holes are connected together in a **row**, and what does the **center gap** do?  
2. Why is it important that Pico GPIO pins use **3.3 V logic**, and what can go wrong if you connect a 5 V signal directly to a GPIO pin?  
3. **Predict the output:** What will this code do?

    ```python
    from picozero import LED
    from time import sleep

    led = LED(14)

    for i in range(3):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

    print("Done")
    ```

4. **Debug this button code:** There is a bug that stops the LED from ever turning on. What is wrong, and how would you fix it?

    ```python
    from picozero import Button, LED

    button = Button(13)
    led = LED(14)

    while True:
        if button.is_pressed:
            led.on
        else:
            led.off()
    ```

5. What is the difference between using a **pushbutton** and using an **ultrasonic sensor** to detect objects? When might you choose one over the other in a project?  
6. Why might you choose to display information on the **OLED** instead of only printing to the **Thonny Shell**? Give one concrete example.

---

## Try it: Mini-exercises

Each of these should take about **3–8 minutes**. Start simple, then build up.

1. **SOS blink:** Use the external LED to blink the Morse code for SOS (`... --- ...`) in a loop.  
2. **Toggle button:** Make a program where **each button press toggles** the LED between ON and OFF (hint: use a `state` variable).  
3. **Traffic light:** Use the RGB LED to cycle through **red → green → yellow** like a traffic signal, with short delays between each color.  
4. **Distance warning light:** Combine the ultrasonic sensor and LED so the LED turns on only when an object is closer than **20 cm**.  
5. **Distance + beep:** Extend the previous exercise to play a **short beep** on the buzzer when something is too close, and stay silent otherwise.  
6. **OLED distance display:** Show the **current distance in cm** on the OLED and update it a few times per second.

### Stretch goals

Pick one or two if you finish early:

- **Best reaction time:** Modify the reaction game to print the **reaction time in milliseconds** for each player (use `time.ticks_ms()` or a similar approach).  
- **Multi-mode menu:** At startup, ask the user (via `input()` in the Thonny Shell) which mode to run:  
  - `1` = LED blink demo  
  - `2` = button + LED  
  - `3` = ultrasonic + buzzer  
  Loop until the user enters `q` to quit.  
- **OLED dashboard:** Design a simple “dashboard” screen that shows **distance**, a **status message** (“SAFE” / “TOO CLOSE”), and maybe a tiny border box around the edges of the screen.  
- **Color-coded distance:** Use the RGB LED to show **green** when far away, **yellow** in the middle, and **red** when very close based on the ultrasonic reading.

---

## Troubleshooting

- **LED never lights**  
  - Check the LED orientation (**long leg** should go toward the GPIO path).  
  - Confirm the GPIO number in your code matches the pin actually wired.  
  - Make sure you are powering the Pico and that Thonny is set to **MicroPython (Raspberry Pi Pico)**.

- **Button always “pressed” or never pressed**  
  - Verify the button is wired **across the center gap**, not on the same side.  
  - One side of the button must go to **GND**.  
  - If you use `machine.Pin` instead of `picozero.Button`, remember to set a **pull-up** or **pull-down**.

- **Ultrasonic distance readings are wrong or random**  
  - Confirm you have **HC-SR04P** (3.3–5 V) and not a 5-V-only version.  
  - Double-check VCC → **3V3(OUT)** and GND → **GND**.  
  - Make sure `echo` and `trigger` are not swapped in the code.  
  - Point the sensor at a flat, hard surface; soft or angled surfaces reflect poorly.

- **Buzzer is silent or always on**  
  - Ensure the positive buzzer pin goes to **GPIO 20** and the negative to **GND**.  
  - Check that you are calling `buzzer.on()` / `buzzer.off()` (with parentheses).  
  - If the buzzer only ever makes one fixed tone regardless of your code, it is probably an **active** buzzer—use it for simple beeps, not melodies.

- **OLED shows nothing**  
  - Check VCC and GND; do not mix them up.  
  - Make sure **SDA** is on GPIO 0 and **SCL** is on GPIO 1.  
  - Ensure the `ssd1306.py` file is saved on the **Pico**, not just your computer.  
  - Try switching `addr=0x3C` to `addr=0x3D` if your module uses a different I2C address.

- **Error: `ImportError: no module named 'ssd1306'`**  
  - The driver file is missing. Re-open `ssd1306.py` in Thonny and save it directly to the **Raspberry Pi Pico**.

- **Random resets or hot components**  
  - Look for accidental **shorts** (e.g., GPIO driven HIGH directly to GND).  
  - Make sure the Pico is powered from a good USB cable and port (not a loose power bank).

---

## Next up
Do the matching lab: **[03 – Pico Breadboard](../Labs/03-pico-breadboard.md)**
