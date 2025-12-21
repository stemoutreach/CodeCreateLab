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

- `03A_distance_station.py` (recommended while testing)

Starter code (fill in TODOs as you go):

```python
from picozero import LED, Button, RGBLED, DistanceSensor, Speaker
from time import sleep

# 03 — Pico Smart Distance Station
# Completed reference solution for coaches/teachers.
# Students should work from the lab Skeleton Starter and STUDENT_START.md.

# --- Pin setup (matches the lab instructions) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 13
RGB_RED_PIN = 17
RGB_GREEN_PIN = 18
RGB_BLUE_PIN = 19
ULTRASONIC_ECHO_PIN = 11
ULTRASONIC_TRIG_PIN = 10
SPEAKER_PIN = 20

# --- Distance thresholds (in cm) ---
CLOSE_CM = 20.0
MEDIUM_CM = 40.0

# --- Objects ---
status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
rgb = RGBLED(red=RGB_RED_PIN, green=RGB_GREEN_PIN, blue=RGB_BLUE_PIN)
sensor = DistanceSensor(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)

# Simple mode variable: "idle" or "active"
mode = "idle"

# Track previous button state for edge detection
prev_pressed = False


def read_distance_cm():
    """Return the distance in centimeters (float)."""
    d_m = sensor.distance        # distance in meters
    d_cm = d_m * 100
    return d_cm


def update_lights(distance_cm):
    """
    Set status_led and rgb color based on:
      - mode (idle vs active)
      - distance_cm (far / medium / close)
    """
    global mode

    if mode == "idle":
        status_led.off()
        rgb.off()
        return

    # mode == "active"
    status_led.on()

    if distance_cm is None:
        # If we somehow get here without a distance, just turn RGB off
        rgb.off()
        return

    # Choose colors for distance ranges
    if distance_cm < CLOSE_CM:
        # Too close: red
        rgb.color = (1.0, 0.0, 0.0)
    elif distance_cm < MEDIUM_CM:
        # Medium range: yellow (red + green)
        rgb.color = (1.0, 1.0, 0.0)
    else:
        # Far: green
        rgb.color = (0.0, 1.0, 0.0)


def update_sound(distance_cm, loop_count):
    """
    Decide when/how the speaker should beep.

    Pattern:
      - idle: speaker.off()
      - far:  silent
      - medium: short beep every few loops
      - close: faster short beep each loop
    """
    global mode

    if mode == "idle" or distance_cm is None:
        speaker.off()
        return

    # Far: silent
    if distance_cm >= MEDIUM_CM:
        speaker.off()
        return

    # Medium: occasional beep (every 5th loop)
    if CLOSE_CM <= distance_cm < MEDIUM_CM:
        if loop_count % 5 == 0:
            speaker.beep(on_time=0.05, off_time=0.05, n=1)
        else:
            speaker.off()
        return

    # Close: frequent beeps (every loop)
    if distance_cm < CLOSE_CM:
        speaker.beep(on_time=0.05, off_time=0.05, n=1)
        return


def handle_button():
    """
    Flip mode when the button is pressed (edge-triggered).

    We toggle when the state changes from "not pressed" to "pressed".
    """
    global mode, prev_pressed

    pressed_now = button.is_pressed

    # Detect transition: not pressed -> pressed
    if (not prev_pressed) and pressed_now:
        mode = "active" if mode == "idle" else "idle"
        print("Mode changed to:", mode)

    prev_pressed = pressed_now


def main():
    print("Pico Smart Distance Station starting...")
    print("Press the button to toggle between IDLE and ACTIVE.")
    print("Move your hand in front of the sensor to test.")

    loop_count = 0

    try:
        while True:
            loop_count += 1
            handle_button()

            if mode == "active":
                distance_cm = read_distance_cm()
                print(f"Distance: {distance_cm:.1f} cm")
            else:
                distance_cm = None  # no reading in idle

            update_lights(distance_cm)
            update_sound(distance_cm, loop_count)

            sleep(0.1)  # small delay to avoid spamming the sensor
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        status_led.off()
        rgb.off()
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
    """
    Draw the top 3 lines (title + browse-to + IP).
    The 4th line (y=48) is reserved for live status like distance.
    """
    oled.fill(0)
    oled.text("Pico 2 W Online", 0, 0)
    oled.text("Browse to:", 0, 16)
    oled.text(ip_str[:16], 0, 32)
    oled.show()

def show_status_line(line):
    """
    Update ONLY the bottom (4th) line.
    """
    oled.fill_rect(0, 48, 128, 16, 0)
    oled.text(line[:16], 0, 48)
    oled.show()

def show_distance(distance_cm, active: bool = True):
    """
    Show distance on the 4th line in a compact format.

    Examples (<=16 chars):
      Distance=123.4cm
      Distance=PAUSED
      Distance=---
    """
    if not active:
        show_status_line("Distance=PAUSED")
        return

    if distance_cm is None:
        show_status_line("Distance=---")
        return

    # "Distance=" (9) + "123.4" (5) + "cm"(2) = 16 chars
    try:
        txt = "Distance=%0.1fcm" % float(distance_cm)
    except Exception:
        txt = "Distance=---"

    show_status_line(txt)

```

### `web_dashboard.py` (simple HTTP server)

This keeps things intentionally simple:

- `/` shows a page with live values  
- `/led/on` turns the LED on  
- `/led/off` turns the LED off

```python
# web_dashboard.py
"""
Pico WiFi Dashboard (Live + Capture Toggle + Part A RGB + OLED Distance)

Why your OLED stayed on "PAUSED":
- Your current oled_status.py only has show_status_line().
- The live dashboard tries to call show_distance() for updates.
- If show_distance() doesn't exist, the dashboard can’t update the OLED.

This version:
- Updates OLED live using show_distance() if available,
  OR falls back to show_status_line("Distance=...") if not.
- Matches Part A thresholds:
    close < 20 cm  -> RGB RED
    20–40 cm       -> RGB YELLOW
    > 40 cm        -> RGB GREEN
"""

import gc
import socket
import ujson
import utime
from machine import Pin
from picozero import LED, Button, DistanceSensor, RGBLED

# --- Pins (Lab Standard Map) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 13
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11
RGB_R_PIN = 17
RGB_G_PIN = 18
RGB_B_PIN = 19

# --- Part A thresholds (cm) ---
CLOSE_CM = 20.0
MEDIUM_MAX_CM = 40.0

RGB_COMMON_ANODE = False
_DEBOUNCE_MS = 250
_SENSOR_UPDATE_MS = 500

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
rgb = RGBLED(red=RGB_R_PIN, green=RGB_G_PIN, blue=RGB_B_PIN)
onboard_led = Pin("LED", Pin.OUT)

# OLED support (show_distance preferred, show_status_line fallback)
try:
    import oled_status
except Exception:
    oled_status = None

sensor_active = False
_last_distance_cm = None
_last_rgb_name = "OFF"
_last_rgb_f = (0.0, 0.0, 0.0)
_last_sensor_update_ms = 0


def _set_active(active: bool) -> bool:
    global sensor_active, _last_distance_cm, _last_rgb_name, _last_rgb_f
    sensor_active = bool(active)

    if sensor_active:
        status_led.on()
        onboard_led.on()
    else:
        status_led.off()
        onboard_led.off()
        _last_distance_cm = None
        _last_rgb_name = "OFF"
        _last_rgb_f = (0.0, 0.0, 0.0)
        _rgb_off()
        _oled_distance(None, active=False)

    return sensor_active


def _toggle_active() -> bool:
    return _set_active(not sensor_active)


def _safe_distance_cm():
    try:
        d_m = sensor.distance
        d_cm = float(d_m) * 100.0
        if d_cm < 0:
            return None
        return d_cm
    except Exception:
        return None


def _rgb_apply(r: float, g: float, b: float):
    if RGB_COMMON_ANODE:
        r, g, b = (1.0 - r), (1.0 - g), (1.0 - b)
    rgb.color = (r, g, b)


def _rgb_off():
    _rgb_apply(0.0, 0.0, 0.0)


def _rgb_to_255(r: float, g: float, b: float):
    return int(r * 255), int(g * 255), int(b * 255)


def _color_from_distance(distance_cm):
    if distance_cm is None:
        return "NO READ", (0.0, 0.0, 1.0)  # BLUE = read error while active

    if distance_cm < CLOSE_CM:
        return "RED", (1.0, 0.0, 0.0)
    elif distance_cm <= MEDIUM_MAX_CM:
        return "YELLOW", (1.0, 1.0, 0.0)
    else:
        return "GREEN", (0.0, 1.0, 0.0)


def _oled_distance(distance_cm, active: bool):
    """
    Update OLED bottom line:
    - Prefer oled_status.show_distance(distance_cm, active=...)
    - Fallback: oled_status.show_status_line("Distance=...")
    """
    if oled_status is None:
        return

    try:
        if hasattr(oled_status, "show_distance"):
            oled_status.show_distance(distance_cm, active=active)
            return

        # Fallback to show_status_line only
        if not active:
            oled_status.show_status_line("Distance=PAUSED")
            return

        if distance_cm is None:
            oled_status.show_status_line("Distance=---")
            return

        # "Distance=123.4cm" fits 16 chars
        oled_status.show_status_line("Distance=%0.1fcm" % float(distance_cm))
    except Exception as e:
        # Don't hard-crash if OLED isn't present; just print once in a while if you want
        # print("OLED update error:", e)
        pass


def _maybe_update_sensor(force: bool = False):
    global _last_distance_cm, _last_rgb_name, _last_rgb_f, _last_sensor_update_ms

    if not sensor_active:
        return

    now = utime.ticks_ms()
    if (not force) and utime.ticks_diff(now, _last_sensor_update_ms) < _SENSOR_UPDATE_MS:
        return
    _last_sensor_update_ms = now

    d_cm = _safe_distance_cm()
    rgb_name, (r, g, b) = _color_from_distance(d_cm)

    _last_distance_cm = d_cm
    _last_rgb_name = rgb_name
    _last_rgb_f = (r, g, b)

    _rgb_apply(r, g, b)
    _oled_distance(d_cm, active=True)


def _http_response(body: bytes, content_type: str = "text/plain", status: str = "200 OK") -> bytes:
    headers = (
        "HTTP/1.1 " + status + "\r\n"
        "Content-Type: " + content_type + "\r\n"
        "Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n"
        "Pragma: no-cache\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body


def _page_html(ip: str, poll_ms: int = 500) -> bytes:
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Pico WiFi Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; margin: 1rem; }}
    .box {{ border: 1px solid #ccc; padding: 0.75rem; border-radius: 10px; margin: 0.75rem 0; }}
    button {{ padding: 0.75rem 1.1rem; margin-right: 0.5rem; border-radius: 10px; border: 1px solid #999; }}
    .value {{ font-weight: 700; }}
    .small {{ opacity: 0.8; font-size: 0.95rem; }}
    code {{ background: #eee; padding: 0.1rem 0.25rem; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Pico WiFi Dashboard</h1>
  <p class="small"><strong>IP:</strong> {ip}</p>

  <div class="box">
    <h2>Ultrasonic Capture</h2>
    <p>
      <button onclick="toggleActive()">Toggle Capture</button>
      <span class="small">Tip: Pico button (GPIO 13) toggles too.</span>
    </p>
    <p><strong>Capture:</strong> <span id="active" class="value">--</span></p>
  </div>

  <div class="box">
    <h2>Live Readings</h2>
    <p><strong>Distance:</strong> <span id="dist" class="value">--</span> <span class="small">cm</span></p>
    <p><strong>Button:</strong> <span id="btn" class="value">--</span></p>
    <p><strong>Status LED:</strong> <span id="led" class="value">--</span></p>

    <p><strong>RGB Color:</strong> <span id="rgbName" class="value">--</span></p>
    <p class="small"><strong>RGB (0–255):</strong> <code id="rgb255">--</code></p>

    <p class="small">Updates every {poll_ms} ms</p>
  </div>

<script>
async function toggleActive() {{
  try {{
    await fetch('/capture/toggle', {{ cache: 'no-store' }});
    await tick();
  }} catch (e) {{}}
}}

async function tick() {{
  try {{
    const r = await fetch('/data', {{ cache: 'no-store' }});
    const j = await r.json();

    document.getElementById('btn').textContent = j.button_pressed ? 'Pressed' : 'Released';
    document.getElementById('led').textContent = j.led_on ? 'ON' : 'OFF';
    document.getElementById('active').textContent = j.sensor_active ? 'ACTIVE' : 'INACTIVE';

    document.getElementById('rgbName').textContent = j.rgb_name;
    document.getElementById('rgb255').textContent = `(${{j.rgb_255[0]}}, ${{j.rgb_255[1]}}, ${{j.rgb_255[2]}})`;

    if (!j.sensor_active) {{
      document.getElementById('dist').textContent = 'PAUSED';
    }} else {{
      document.getElementById('dist').textContent = (j.distance_cm === null) ? '---' : j.distance_cm.toFixed(1);
    }}
  }} catch (e) {{
    document.getElementById('dist').textContent = '---';
  }}
}}

tick();
setInterval(tick, {poll_ms});
</script>
</body>
</html>
"""
    return html.encode("utf-8")


def _parse_path(request_text: str) -> str:
    try:
        first_line = request_text.split("\r\n", 1)[0]
        parts = first_line.split(" ")
        if len(parts) >= 2:
            return parts[1]
    except Exception:
        pass
    return "/"


def run_server(ip: str, poll_ms: int = 500):
    _set_active(False)
    _oled_distance(None, active=False)

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.settimeout(0.1)
    s.bind(addr)
    s.listen(1)

    print("Listening on", addr)
    print("Open: http://%s/" % ip)

    last_pressed = False
    last_toggle_ms = utime.ticks_ms()

    while True:
        pressed = bool(button.is_pressed)
        if pressed and (not last_pressed):
            now = utime.ticks_ms()
            if utime.ticks_diff(now, last_toggle_ms) >= _DEBOUNCE_MS:
                _toggle_active()
                if sensor_active:
                    _maybe_update_sensor(force=True)
                last_toggle_ms = now
        last_pressed = pressed

        _maybe_update_sensor(force=False)

        try:
            cl, _ = s.accept()
        except OSError:
            gc.collect()
            continue

        try:
            cl.settimeout(2)
            req = cl.recv(1024)
            if not req:
                cl.close()
                continue

            path = _parse_path(req.decode("utf-8", "ignore"))

            if path.startswith("/capture/toggle"):
                new_state = _toggle_active()
                if new_state:
                    _maybe_update_sensor(force=True)
                body = ujson.dumps({"sensor_active": bool(new_state)}).encode()
                cl.sendall(_http_response(body, "application/json"))
                continue

            if path.startswith("/data"):
                _maybe_update_sensor(force=False)

                if sensor_active:
                    d_cm = _last_distance_cm
                    rgb_name = _last_rgb_name
                    r, g, b = _last_rgb_f
                else:
                    d_cm = None
                    rgb_name = "OFF"
                    r, g, b = (0.0, 0.0, 0.0)

                payload = {
                    "distance_cm": d_cm,
                    "sensor_active": bool(sensor_active),
                    "button_pressed": bool(button.is_pressed),
                    "led_on": bool(status_led.value),
                    "rgb_name": rgb_name,
                    "rgb_255": _rgb_to_255(r, g, b),
                    "ms": utime.ticks_ms(),
                }
                cl.sendall(_http_response(ujson.dumps(payload).encode(), "application/json"))
                continue

            cl.sendall(_http_response(_page_html(ip, poll_ms=poll_ms), "text/html"))

        except Exception as e:
            try:
                cl.sendall(_http_response(("Error: %s" % e).encode(), "text/plain", status="500 Internal Server Error"))
            except Exception:
                pass
            print("Client error:", e)
        finally:
            try:
                cl.close()
            except Exception:
                pass
            gc.collect()

```

### `main.py` (glue it together)

```python
# main.py
from wifi import connect_wifi
from oled_status import show_wifi_ip, show_distance
from web_dashboard import run_server

def main():
    ip = connect_wifi()
    if not ip:
        return

    show_wifi_ip(ip)
    # Replace "Waiting for web..." with a distance placeholder immediately
    show_distance(None, active=False)

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
