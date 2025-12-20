# Raspberry Pi Pico Breadboarding Guide

> ### Quick Summary
> **Level:** 03 • **Time:** 60–90 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi Pico + micro-USB cable; breadboard, jumper wires, LEDs, pushbuttons, RGB LED, ultrasonic sensor (HC-SR04P), passive buzzer/small speaker, 0.96\" I2C OLED. *(Pico W / Pico 2 W needed for Sections 7–8.)*  
> **You’ll practice:** blink LEDs, read buttons with debouncing, mix RGB colors, measure distance with ultrasonic, play tones, draw text on an I2C OLED, connect to WiFi, host a tiny web page

> **Learn → Try:** Learn concepts here with tiny examples, then try mini-exercises before you do the matching Lab.

# Why This Matters
Breadboards let you prototype **electronics without soldering**. Pairing the **Raspberry Pi Pico** with MicroPython gives you instant feedback: blink LEDs, read buttons, measure distance, make sounds, and show messages on a tiny screen. Mastering these basics prepares you for sensors, motors, and bigger robot projects.

---

## What you’ll learn
- Breadboard anatomy (power rails, rows, and the center “gap”)
- GPIO basics: inputs vs outputs, pin numbering, and **3.3 V safety**
- Using MicroPython with **Thonny** and the **picozero** library
- Onboard + external LEDs, plus RGB color mixing
- Reading pushbuttons reliably and understanding **debouncing**
- Measuring distance with an **HC-SR04P** ultrasonic sensor
- Making beeps and tones on a passive buzzer/speaker
- Displaying text on a **0.96\" SSD1306 I2C OLED**
- *(Pico W / Pico 2 W only)* Joining WiFi and finding the Pico’s IP address
- *(Pico W / Pico 2 W only)* Hosting a tiny web page with **ON/OFF** buttons

## Table of Contents (Walkthrough 1–8)
- [1) Blink LEDs (onboard and external)](#1-blink-leds-onboard-and-external)
- [2) Read pushbuttons](#2-read-pushbuttons)
- [3) RGB LED color mixing](#3-rgb-led-color-mixing)
- [4) Ultrasonic Distance Sensor](#4-ultrasonic-distance-sensor)
- [5) Speaker](#5-speaker)
- [6) OLED Display](#6-oled-display)
- [7) WiFi Config and Connect](#7-wifi-config-and-connect)
- [8) Simple Web Button](#8-simple-web-button)

---

## Setup
_Classroom default: **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**._

1. Connect the **Pico** via **micro-USB** to the Raspberry Pi 500.
2. Open **Thonny** → **Tools ▸ Options ▸ Interpreter**:
   - Interpreter: **MicroPython (Raspberry Pi Pico)**
   - Port: **Automatic**
   - If prompted, let Thonny **install/flash MicroPython (UF2)** to the Pico.
3. Save your script either:
   - On your computer (good for experiments), or
   - Directly on the Pico (File → Save as… → **Raspberry Pi Pico**).
4. Press **Run ▶** to execute your code.

> Tip: A file named **`main.py`** saved on the Pico will **auto-run** whenever the Pico powers up.

---

## Materials (hardware)
- **Raspberry Pi Pico** (W recommended)
- **Breadboard** and jumper wires
- **2× pushbutton** (tact switches)
- **1× single-color LED** *(with resistor, or a pre-resisted LED from a kit)*
- **1× common cathode RGB LED**
- **HC-SR04P** ultrasonic distance sensor *(3.3–5 V version recommended)*
- **Passive piezo buzzer or small speaker**
- **0.96\" I2C OLED display** (SSD1306, 128×64, 4-pin VCC/GND/SCL/SDA)
- **Optional (recommended if your ultrasonic ECHO is 5V):** two resistors for a voltage divider (ex: 1 kΩ + 2 kΩ)

> ⚠️ **Safety note:** Pico GPIO pins are **3.3 V only**. Never feed 5 V into a GPIO. Always share a common **GND** between Pico and sensors.

---

## Walkthrough — Step by Step (with explanations)

### Standard pin map used in this guide
Use this **standard map** so the Lab and Guide match:

```python
# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN  = 13        # main pushbutton
BUTTON2_PIN = 15        # second button (reaction game)
LED_PIN     = 14        # external LED
RGB_R_PIN   = 17
RGB_G_PIN   = 18
RGB_B_PIN   = 19
SPEAKER_PIN = 20        # passive buzzer / speaker

# OLED Display (0.96" I2C 128x64, SSD1306)
OLED_SDA_PIN = 0        # I2C0 SDA
OLED_SCL_PIN = 1        # I2C0 SCL
```

---

### Meet the Pico, GPIO, and breadboard (fast version)

- The **Pico** is a microcontroller. It runs your MicroPython code directly (no full operating system).
- **GPIO pins** can be **outputs** (LEDs, buzzers) or **inputs** (buttons, sensors).
- Breadboards connect:
  - **Rows of 5 holes** together (on each side of the center gap)
  - **Power rails** along the side for 3V3 and GND
  - The **center gap** separates left/right sides (prevents shorts)

> If something doesn’t work, it’s usually a wire in the wrong **row**, wrong **side of the gap**, or a missing **GND** connection.

---

## 1) Blink LEDs (onboard and external)

### Onboard LED blink
Use `picozero.pico_led` so your code works on both Pico and Pico W.

```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```

### External LED blink (GPIO 14)
**Wiring**
- Pico **GPIO 14** → LED long leg (anode) *(through resistor if needed)*
- LED short leg (cathode) → **GND**

```python
from picozero import LED
from time import sleep

led = LED(LED_PIN)  # LED_PIN = 14

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

**Quick fixes**
- If it never lights, flip the LED.
- Confirm the GPIO number in code matches your wiring.
- Press **Stop** in Thonny to end the loop.

---

## 2) Read pushbuttons

**Wiring**
- One button leg → **GPIO 13**
- Opposite leg → **GND**
- Make sure the button straddles the breadboard **center gap**.

```python
from picozero import Button, LED
from time import sleep

button = Button(BUTTON_PIN)   # BUTTON_PIN = 13
led = LED(LED_PIN)            # LED_PIN = 14

while True:
    led.value = button.is_pressed
    sleep(0.02)               # small delay helps with debouncing
```

### Mini reaction game (two players)
After a random wait, the LED turns on. First button press wins.

```python
from picozero import Button, LED
from time import sleep
import random

led = LED(LED_PIN)
p1 = Button(BUTTON_PIN)
p2 = Button(BUTTON2_PIN)

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

---

## 3) RGB LED color mixing

**Wiring (common cathode RGB LED)**
- Common cathode (usually longest leg) → **GND**
- Red leg → **GPIO 17**
- Green leg → **GPIO 18**
- Blue leg → **GPIO 19**

```python
from picozero import RGBLED
from time import sleep

rgb = RGBLED(red=RGB_R_PIN, green=RGB_G_PIN, blue=RGB_B_PIN)

while True:
    rgb.color = (1, 0, 0)   # red
    sleep(0.5)
    rgb.color = (0, 1, 0)   # green
    sleep(0.5)
    rgb.color = (0, 0, 1)   # blue
    sleep(0.5)
    rgb.color = (1, 1, 0)   # yellow
    sleep(0.5)
    rgb.off()
    sleep(0.5)
```

> If your LED is **common anode**, set `RGBLED(..., active_high=False)` and connect the common pin to **3V3**.

---

## 4) Ultrasonic Distance Sensor

**Goal:** Measure distance by timing an echo.

### Important voltage note (read this)
Many HC-SR04-style sensors output a **5V ECHO** signal. Pico inputs must stay at **3.3V max**.

- If your sensor’s ECHO is 5V, use a **voltage divider** on ECHO (example: 2 kΩ from ECHO to Pico, 1 kΩ from Pico to GND).
- If you have an **HC-SR04P** (3.3–5 V), it’s typically safer, but still treat ECHO carefully.

### Wiring (typical)
- VCC → 5V (or 3V3 if your module supports it)
- GND → GND
- TRIG → GPIO 10
- ECHO → (through divider if needed) → GPIO 11

### Code
```python
from picozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)

while True:
    d_cm = sensor.distance * 100   # distance is meters
    print(f"{d_cm:.1f} cm")
    sleep(0.2)
```

**Tips**
- Aim at a flat surface.
- Don’t spam readings; 5–10 per second is plenty.

---

## 5) Speaker

**Goal:** Make simple beeps and tones.

### Passive buzzer / small speaker wiring
- GPIO 20 → + buzzer
- GND → – buzzer

### Simple beeps (works with most buzzers)
```python
from picozero import Buzzer
from time import sleep

buzzer = Buzzer(SPEAKER_PIN)

buzzer.on()
sleep(0.2)
buzzer.off()
sleep(0.2)
buzzer.beep(on_time=0.1, off_time=0.1, n=5)
```

### Tones (requires a passive buzzer/speaker)
```python
from picozero import Speaker
from time import sleep

sp = Speaker(SPEAKER_PIN)

sp.play(440, 0.2)   # A4
sleep(0.1)
sp.play(523, 0.2)   # C5
sleep(0.1)
sp.play(659, 0.2)   # E5
sp.off()
```

> If your buzzer only ever makes one fixed tone, it’s probably an **active buzzer** (great for beeps, not for melodies).

---

## 6) OLED Display

**Goal:** Show text on a 0.96\" I2C SSD1306 OLED.

### Wiring (I2C0)
- OLED VCC → Pico 3V3(OUT)
- OLED GND → Pico GND
- OLED SDA → Pico GP0
- OLED SCL → Pico GP1

### Driver file
This requires **`ssd1306.py`** on the Pico.
- If it’s missing, open `ssd1306.py` in Thonny and **Save as… → Raspberry Pi Pico**.

### Hello World
```python
from machine import Pin, I2C
import ssd1306
from time import sleep

i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.text("Hello, world!", 0, 0)
oled.text("Pico OLED OK", 0, 16)
oled.show()

while True:
    sleep(1)
```

> If nothing shows: check SDA/SCL aren’t swapped, confirm the address (some boards use `0x3D`).

---

## 7) WiFi Config and Connect

WiFi only works on **Pico W / Pico 2 W**. If you have a non‑W Pico, skip this section.

**Goal:** Connect to WiFi and print the Pico’s IP address in Thonny.

### Quick rules
- Use a **2.4 GHz** network (5 GHz won’t work on many microcontrollers).
- Captive portals (hotel/school “sign-in” pages) usually **won’t work**.
- If stuck, try a **phone hotspot**.

### Single-script WiFi connect (no extra files yet)
```python
import network
import time

SSID = "CHANGE_ME_WIFI_NAME"
PASSWORD = "CHANGE_ME_PASSWORD"

def connect_wifi(timeout_s=15):
    wlan = network.WLAN(network.STA_IF)   # join an existing WiFi network
    wlan.active(True)

    if wlan.isconnected():
        return wlan.ifconfig()[0]

    print("Connecting to WiFi", end="")
    wlan.connect(SSID, PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout_s:
            raise RuntimeError("WiFi failed (SSID/PASSWORD, 2.4GHz, captive portal).")
        print(".", end="")
        time.sleep(1)

    ip = wlan.ifconfig()[0]
    print("\nConnected! IP:", ip)
    return ip

ip = connect_wifi()
```

---

## 8) Simple Web Button

Now we’ll host a tiny web page on the Pico. Your browser will show **ON** and **OFF** buttons to control the **onboard LED**.

### Single-script web server (onboard LED)
```python
import network
import socket
import time
from machine import Pin

SSID = "CHANGE_ME_WIFI_NAME"
PASSWORD = "CHANGE_ME_PASSWORD"

pico_led = Pin("LED", Pin.OUT)  # Pico W / Pico 2 W

def connect_wifi(timeout_s=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        return wlan.ifconfig()[0]

    print("Connecting to WiFi", end="")
    wlan.connect(SSID, PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout_s:
            raise RuntimeError("WiFi failed (SSID/PASSWORD, 2.4GHz, captive portal).")
        print(".", end="")
        time.sleep(1)

    ip = wlan.ifconfig()[0]
    print("\nConnected! IP:", ip)
    return ip

def page(state: str) -> str:
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pico Web Button</title>
  <style>
    body {{ font-family: sans-serif; margin: 1rem; }}
    button {{ padding: 0.8rem 1.2rem; margin-right: 0.5rem; }}
  </style>
</head>
<body>
  <h1>Pico Web Button</h1>
  <p><strong>Onboard LED:</strong> {state}</p>
  <p>
    <a href="/on"><button>ON</button></a>
    <a href="/off"><button>OFF</button></a>
  </p>
</body>
</html>
"""

def run_server(port=80):
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    led_on = False
    pico_led.off()

    print(f"Web server ready: http://{ip}:{port}/")

    while True:
        cl, _ = s.accept()
        try:
            req = cl.recv(1024).decode("utf-8")
            path = req.split(" ")[1] if req else "/"

            if path.startswith("/on"):
                pico_led.on()
                led_on = True
            elif path.startswith("/off"):
                pico_led.off()
                led_on = False

            cl.send(page("ON" if led_on else "OFF"))
        finally:
            cl.close()

ip = connect_wifi()
run_server(port=80)
```

### Use it
1. Run the script.
2. Copy the printed IP (example `192.168.1.42`).
3. On a device on the **same WiFi**, open: `http://<ip>/`
4. Click **ON** / **OFF** and watch the onboard LED.

**Stop the server:** click Thonny **Stop** or press `Ctrl+C`.

> If port **80** is blocked on your network, change `port=80` to `port=8080`, then open `http://<ip>:8080/`.

---

## Vocabulary
- **MicroPython:** A lightweight version of Python that runs on microcontrollers like the Pico
- **GPIO:** Pins used for input (read) or output (control)
- **Debouncing:** Smoothing out rapid on/off “chatter” from a physical button press
- **I2C:** Two-wire device bus (SDA + SCL) used for OLEDs and sensors
- **STA mode:** “Station” mode (the Pico joins an existing WiFi network)
- **Socket:** A basic network connection used to send/receive data (like a tiny web server)
- **HTTP:** The simple request/response protocol your browser uses

---

## Check your understanding
1. Why is the Pico’s GPIO limit **3.3 V**, and what can happen if you feed a GPIO **5 V**?
2. On a breadboard, what does the **center gap** do?
3. What is **debouncing**, and why do we add a small delay in a button loop?
4. Why do Sections 7–8 require a **Pico W / Pico 2 W**?
5. In the web server, what URL path turns the LED on?

---

## Try it: Mini-exercises
1. **SOS blink:** Blink Morse code SOS (`... --- ...`) with the external LED.
2. **Toggle press:** Each button press toggles the LED on/off (use a `state` variable).
3. **Traffic light:** RGB LED cycles red → green → yellow.
4. **Distance warning:** Turn the LED on when distance is < **20 cm**.
5. **OLED dashboard:** Show distance on the OLED and update it 5×/second.
6. *(WiFi)* Print the Pico’s IP, then show it on the OLED (extra challenge).
7. *(Web)* Add a third button: **BLINK** (blink onboard LED 3 times).

---

## Troubleshooting (quick hits)

- **LED never lights**
  - Flip the LED, verify GPIO number, check GND.

- **Button always pressed / never pressed**
  - Button must straddle the breadboard gap, one side to GND.

- **Ultrasonic readings random**
  - Confirm shared GND, check TRIG/ECHO pins, and protect ECHO voltage.

- **OLED blank**
  - Swap SDA/SCL if needed, ensure `ssd1306.py` is on the Pico, try `addr=0x3D`.

- **WiFi won’t connect**
  - Check SSID/PASSWORD, use **2.4 GHz**, avoid captive portals, try a phone hotspot.

- **Web page won’t load**
  - Ensure your phone/laptop is on the same WiFi, try `:8080` if port 80 is blocked.

---

## Next up
Do the matching lab: **[03 – Pico Breadboard](../Labs/03-pico-breadboard.md)**
