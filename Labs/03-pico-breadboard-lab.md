# 03 — Pico Smart Distance Station + WiFi Dashboard (Lab)

> ### Quick Summary  
> **Level:** 03 • **Time:** 90–120 min  
> **Prereqs:**  
> - [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> - [Guide: 01 — Python Functions](../Guides/01-python-functions.md)  
> - [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> **Hardware:**  
> - Raspberry Pi **Pico** (Part A) *or* **Pico 2 W** (Part A + Part B) + micro-USB cable  
> - Breadboard + jumper wires  
> - 1 × single-color LED (status LED)  
> - 1 × pushbutton  
> - 1 × RGB LED *(optional, Part A extension)*  
> - 1 × Ultrasonic sensor (HC-SR04 or 3.3V-safe variant)  
> - 1 × passive piezo speaker/buzzer *(optional but recommended)*  
> - 1 × 0.96" I2C SSD1306 OLED display (128×64, 4-pin I2C) *(Part B)*  
> **You’ll practice:** GPIO input/output, distance sensing, mapping sensor values, WiFi connect (STA), showing IP on OLED, serving a simple web page, HTTP routes

---

# Why This Matters

Real projects combine **multiple inputs and outputs** *and* a way to **control/monitor** them.  
In Part A you’ll build a smart station that measures distance and responds with lights and sound.  
In Part B you’ll reuse what you already learned about **WiFi + a simple web app with buttons**, and turn your Pico 2 W into a tiny **dashboard** you can open on any phone/laptop on the same network.

This is the same pattern used by robots, smart home devices, and “monitor + control” dashboards in the real world.

---

# What You’ll Build

## Part A — Smart Distance Station (local)

- Ultrasonic sensor measures distance.  
- Status LED shows whether the station is “armed” and measuring.
- Structure a simple state machine (idle vs active) driven by a pushbutton. 
- RGB LED acts like a traffic light (far/medium/close).  
- Speaker beeps faster as you get closer.

## Part B — WiFi Dashboard (browser)

- Pico 2 W joins WiFi (STA mode).  
- OLED shows the Pico’s IP address.  
- A simple web page:
  - Shows **distance** and **button** state.
  - Lets you turn the **status LED** on/off from the browser.

---

# Outcomes

By the end you can:

- Wire and use multiple parts on one breadboard (LED, button, ultrasonic, speaker).  
- Read distance and convert it to **cm**.  
- Write clean code using small functions (instead of one giant loop).
- Map distance ranges to RGB colors, a status LED, and speaker beeps.
- Structure a simple state machine (idle vs active) driven by a pushbutton.
- Connect a Pico 2 W to WiFi and find its **IP address**.  
- Run a tiny HTTP server and create “routes” like `/led/on` and `/led/off`.  

---

# Setup

- **Environment:** Classroom default is **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**.  
- **Interpreter:** Thonny → **Tools → Options → Interpreter → MicroPython (Raspberry Pi Pico)**.  
- **Project folder (PC):** `~/Documents/CodeCreate/` (or your class folder).  
- **Saving to Pico:** In Thonny, you can save files to:
  - **This computer** (good for backups), and/or  
  - **Raspberry Pi Pico** (required for Part B file layout).

---

# Part A — Build the Smart Distance Station

> If you’re already comfortable wiring these parts, you can move faster here.  
> The key is: **get stable distance readings first**, then add outputs.

## A1) Standard pin map used in this guide

Use this **standard map** so the Lab and Guide match:

```python
# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN  = 13        # main pushbutton
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
**Double-check**
- All grounds are shared (Pico GND, sensor GND, LED GND, speaker GND).  
- TRIG/ECHO are not swapped.  
- Your ECHO pin is protected (3.3V-safe).

## A2) Code it (10–15 min)

Create a new file (on your computer or the Pico) called:

- `03_distance_station.py` (recommended while testing)

Starter code (fill in TODOs as you go):

```python
from picozero import LED, Button, DistanceSensor, Speaker
from time import sleep, ticks_ms

# --- Pin setup (matches the lab instructions) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 13
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11
SPEAKER_PIN = 20

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)

mode = "idle"  # "idle" or "active"
_prev_pressed = False

# Distance thresholds (cm) — tune these later
CLOSE_CM = 20
MEDIUM_CM = 40

# Simple beep timing
_last_beep_ms = 0


def read_distance_cm() -> float:
    d_m = sensor.distance
    return d_m * 100.0


def handle_button():
    global mode, _prev_pressed
    pressed = button.is_pressed

    # Toggle only on a new press (rising edge)
    if pressed and not _prev_pressed:
        mode = "active" if mode == "idle" else "idle"
        print("Mode ->", mode)

    _prev_pressed = pressed


def update_outputs(distance_cm: float):
    global _last_beep_ms

    if mode == "idle":
        status_led.off()
        speaker.off()
        return

    status_led.on()

    # --- Sound mapping (simple + not too annoying) ---
    now = ticks_ms()

    # Far: silent
    if distance_cm > MEDIUM_CM:
        speaker.off()
        return

    # Medium: slow beep
    if distance_cm > CLOSE_CM:
        if now - _last_beep_ms > 900:
            speaker.play(880, 0.05)
            _last_beep_ms = now
        return

    # Close: fast beep
    if now - _last_beep_ms > 250:
        speaker.play(988, 0.05)
        _last_beep_ms = now


def main():
    print("Smart Distance Station starting...")
    print("Press the button to toggle IDLE/ACTIVE.")

    try:
        while True:
            handle_button()

            if mode == "active":
                d = read_distance_cm()
                print(f"Distance: {d:.1f} cm")
                update_outputs(d)
            else:
                update_outputs(0)

            sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        status_led.off()
        speaker.off()


if __name__ == "__main__":
    main()
```

## A3) Test it (3–5 min)

1. Press the button: status LED should toggle on/off with the mode.  
2. In ACTIVE mode, move your hand toward the sensor:
   - Far: no beep  
   - Medium: slow beep  
   - Close: fast beep  

If distance values look glitchy, slow the loop a bit:

- Change `sleep(0.1)` → `sleep(0.2)`.

---

# Part B — Add the WiFi Dashboard (Pico 2 W)

> Part B requires a **Pico 2 W**.  
> You already learned the basics (connect WiFi, simple button routes). Here you’ll **reuse that knowledge** and connect it to your breadboard station.

## B1) Add the OLED (3–5 min)

Use I2C0 so we avoid common motor pins later:

- OLED **VCC** → **3V3**  
- OLED **GND** → **GND**  
- OLED **SDA** → **GP0**  
- OLED **SCL** → **GP1**

## B2) File layout on the Pico (5 min)

Save these files to **Raspberry Pi Pico** storage (`/flash`):

```text
/flash
  main.py             # Entry point: connect WiFi, show IP, start web dashboard
  wifi_config.py      # WiFi name + password only (students edit this)
  wifi.py             # WiFi helper (connect_wifi)
  oled_status.py      # OLED setup + show_wifi_ip
  web_dashboard.py    # HTTP server + LED/sensor routes
  ssd1306.py          # SSD1306 driver (copied once, no edits)
```

### Why we use separate files (modules)

Instead of one huge script, we split the project into **small files that each do one job**:

```text
main.py             # Entry point: connect WiFi, show IP, start web dashboard
wifi_config.py      # WiFi name + password only (students edit this)
wifi.py             # WiFi helper (connect_wifi)
oled_status.py      # OLED setup + show_wifi_ip
web_dashboard.py    # HTTP server + LED/sensor routes
```

**Benefits:**
- **Easier debugging:** if WiFi isn’t working, you know to check `wifi_config.py` + `wifi.py`.
- **Easier teamwork:** one person can work on the web page while another works on the OLED.
- **Reuse:** you can reuse `wifi.py` and `oled_status.py` in later labs/projects.

**Rule of thumb:** students should usually only edit **`wifi_config.py`** (SSID + password).  
Everything else is “project code.”

> Note: You’ll also copy `ssd1306.py` onto the Pico one time as the OLED driver file (no edits).


> If `main.py` exists on the Pico, it will auto-run on boot.

## B3) Copy the SSD1306 driver (1–2 min)

You need a standard MicroPython driver file called **`ssd1306.py`** saved to the Pico.
(Your instructor may provide it, or you may have already used it in earlier activities.)

## B4) Create the WiFi + OLED + Dashboard code (10–15 min)

### `wifi_config.py` (students edit this)

```python
# wifi_config.py
# Put your local WiFi settings here.
# Do NOT commit this file to GitHub.

SSID = "CHANGE_ME_WIFI_NAME"
PASSWORD = "CHANGE_ME_PASSWORD"
```

### `wifi.py` (connect helper)

```python
# wifi.py
import network
import time
from wifi_config import SSID, PASSWORD

def connect_wifi():
    """Connect Pico 2 W to WiFi (station/client mode). Return IP string or None."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)

        max_wait = 15
        while max_wait > 0 and not wlan.isconnected():
            print("  waiting...", max_wait)
            max_wait -= 1
            time.sleep(1)

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print("Connected! IP:", ip)
        return ip

    print("WiFi connection failed.")
    return None
```

### `oled_status.py` (show IP)

```python
# oled_status.py
from machine import Pin, I2C
import ssd1306

# I2C0 on GP0 (SDA) and GP1 (SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def show_wifi_ip(ip_str):
    oled.fill(0)
    oled.text("Pico 2 W Online", 0, 0)
    oled.text("Browse to:", 0, 16)
    oled.text(ip_str, 0, 32)
    oled.show()

def show_status_line(line):
    oled.fill_rect(0, 48, 128, 16, 0)
    oled.text(line[:16], 0, 48)  # keep it short
    oled.show()
```

### `web_dashboard.py` (simple HTTP server)

This keeps things intentionally simple:

- `/` shows a page with live values  
- `/led/on` turns the LED on  
- `/led/off` turns the LED off

```python
# web_dashboard.py
import socket
from machine import Pin
from picozero import LED, Button, DistanceSensor

# Reuse Part A pins
STATUS_LED_PIN = 14
BUTTON_PIN = 13
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)

onboard_led = Pin("LED", Pin.OUT)  # Pico's built-in LED

def read_distance_cm():
    d_m = sensor.distance
    return d_m * 100.0

def build_page(ip, distance_cm, button_pressed, led_on):
    button_text = "Pressed" if button_pressed else "Released"
    led_text = "ON" if led_on else "OFF"

    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
  <title>Pico WiFi Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; margin: 1rem; }}
    button {{ padding: 0.5rem 1rem; margin: 0.25rem; }}
    .box {{ border: 1px solid #ccc; padding: 0.5rem; margin-top: 1rem; }}
  </style>
</head>
<body>
  <h1>Pico WiFi Dashboard</h1>
  <p><strong>IP:</strong> {ip}</p>

  <div class="box">
    <h2>LED Control</h2>
    <p>
      <a href="/led/on"><button>LED ON</button></a>
      <a href="/led/off"><button>LED OFF</button></a>
    </p>
  </div>

  <div class="box">
    <h2>Live Readings</h2>
    <p><strong>Distance:</strong> {distance_cm:.1f} cm</p>
    <p><strong>Button:</strong> {button_text}</p>
    <p><strong>Status LED:</strong> {led_text}</p>
  </div>
</body>
</html>
"""

def run_server(ip):
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)

    while True:
        cl, remote_addr = s.accept()
        print("Client connected from:", remote_addr)

        try:
            request = cl.recv(1024).decode("utf-8")
            if not request:
                cl.close()
                continue

            first_line = request.split("\r\n")[0]
            parts = first_line.split(" ")
            path = parts[1] if len(parts) > 1 else "/"
            print("Request path:", path)

            # --- Routes ---
            if "/led/on" in path:
                status_led.on()
                onboard_led.on()
            elif "/led/off" in path:
                status_led.off()
                onboard_led.off()

            # Always read sensors before responding
            distance_cm = read_distance_cm()
            button_pressed = button.is_pressed
            led_on = bool(status_led.value)

            cl.send(build_page(ip, distance_cm, button_pressed, led_on))
        except Exception as e:
            print("Error:", e)
        finally:
            cl.close()
```

### `main.py` (glue it together)

```python
# main.py
from wifi import connect_wifi
from oled_status import show_wifi_ip, show_status_line
from web_dashboard import run_server

def main():
    ip = connect_wifi()
    if not ip:
        return

    show_wifi_ip(ip)
    show_status_line("Waiting for web...")

    run_server(ip)

if __name__ == "__main__":
    main()
```

## B5) Run it (3–5 min)

1. Save all files to **Raspberry Pi Pico**.  
2. Edit `wifi_config.py` with the correct WiFi name/password.  
3. Run `main.py` (or just reset the Pico if `main.py` is already on the Pico).

You should see:

- Thonny Shell prints: “Connected! IP: …” and “Listening on …”  
- OLED shows the IP address.

On a phone/laptop on the **same WiFi**, open:

```text
http://<ip-address>/
```

Click **LED ON/OFF** and watch the LED change.  
Refresh the page and watch **Distance** and **Button** values update.

---

# Submission / Demo Checklist

**Part A**
- [ ] Button toggles idle/active in your local test script.  
- [ ] Distance readings print and make sense when you move your hand.  
- [ ] Speaker changes behavior based on distance (at least 2 patterns).

**Part B**
- [ ] Pico 2 W connects to WiFi and OLED shows the IP address.  
- [ ] Dashboard loads from a browser on the same network.  
- [ ] `/led/on` and `/led/off` reliably control the LED.  
- [ ] Dashboard shows distance and button state.

---

# Extensions (choose one)

- **Extension A — Add a `/beep` route:**  
  Add a new button on the web page that calls `/beep`, and play a quick tone on the speaker.

- **Extension B — Add “armed” mode from the web:**  
  Add routes like `/mode/active` and `/mode/idle`. Display the current mode on the page.

- **Extension C — RGB indicator:**  
  If you wired an RGB LED, update its color in `run_server()` before building the page:
  - far = green, medium = yellow, close = red.

- **Extension D — Auto-refresh page:**  
  Add `<meta http-equiv="refresh" content="1">` so the dashboard refreshes every second.

---

# Troubleshooting

- **WiFi connects but the page won’t load**
  - Make sure your phone/laptop is on the **same WiFi** as the Pico.
  - Some networks block device-to-device connections (ask your mentor/instructor).
  - Try refreshing, or try `http://<ip>/led/on` directly.

- **OLED stays blank**
  - Check SDA → GP0 and SCL → GP1.
  - Confirm you copied `ssd1306.py` onto the Pico.

- **Distance is always 0.0 cm**
  - TRIG/ECHO swapped, missing GND, or ECHO not 3.3V-safe.
  - Slow the sensor reads (add a small delay or refresh less often).

- **Button toggles many times per press**
  - Use the “edge detect” pattern from Part A (`_prev_pressed`).

---

# Reflection (1–2 sentences)

- What was the biggest “integration moment” for you: wiring, reading sensors, or connecting it to the web dashboard?  
- If you had another hour, what would you add to make this feel like a “real product”?
