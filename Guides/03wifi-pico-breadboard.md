# 03wifi — Pico WiFi Breadboard Dashboard (Guide)

> ### Quick Summary  
> **Level:** 03+ • **Time:** 60–90 min  
> **Prereqs:**  
> - [Guide: 00 — Python Basics](../Guides/00-python-basics.md)  
> - [Guide: 01 — Python Functions](../Guides/01-python-functions.md)  
> - [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> - [Lab: 03 — Pico Smart Distance Station](../Labs/03-pico-breadboard.md)  
> **Hardware:**  
> - Raspberry Pi **Pico 2 W** (built-in WiFi) + micro-USB cable  
> - Breadboard + jumper wires  
> - 1 × single-color LED (re-use STATUS LED)  
> - 1 × pushbutton (re-use from Lab 03)  
> - 1 × Ultrasonic distance sensor (HC-SR04 or 3.3V-safe variant)  
> - 1 × passive piezo speaker/buzzer  
> - 1 × 0.96" I2C SSD1306 OLED display (128×64, 4-pin I2C)  
> **You’ll practice:** WiFi connect (STA mode), showing IP on an OLED, serving a simple web page, reading sensors/buttons, controlling LEDs from a browser

---

# Why This Matters

In Lab 03 you built a **Smart Distance Station**: the Pico read sensors and drove LEDs and a speaker directly.  
Now you’ll turn that same breadboard into a tiny **IoT dashboard**:

- The Pico 2 W joins your **WiFi network**.  
- It shows its **IP address** on the OLED so anyone can connect.  
- It runs a **web server** that:
  - Lets you turn LEDs on/off from a browser.
  - Shows live **distance** and **button** state on the page.

This is the pattern used by real robots, smart home devices, and monitoring dashboards.

---

# Big Picture

You’ll build three layers:

1. **WiFi Layer** – Connect the Pico 2 W to your existing WiFi (STA mode).  
2. **Status Display Layer** – Use an SSD1306 OLED to show the Pico’s IP (so you know what to type in the browser).  
3. **Web Dashboard Layer** – A tiny HTTP server that:
   - Handles URLs like `/led/on` and `/led/off`.  
   - Reads the **distance sensor** and **button**.  
   - Returns an HTML page showing the current readings.

You’ll keep your code organized with small modules (`wifi.py`, `oled_status.py`, `web_dashboard.py`) and a simple `main.py` that glues everything together.

---

# 1. Hardware & Pin Map

We will **reuse** the pin choices from *03 — Pico Smart Distance Station* where possible.

> 💡 Your Pico 2 W must be flashed with the **MicroPython** firmware.

### Reused from Lab 03

- **Status LED (single-color)**  
  - Long leg → **GPIO 14**  
  - Short leg → GND  

- **Pushbutton**  
  - One leg → **GPIO 13**  
  - Opposite leg → GND  

- **Ultrasonic sensor (HC-SR04)**  
  - VCC → 5V (or 3.3V *only* if your module supports it)  
  - GND → GND  
  - TRIG → **GPIO 10**  
  - ECHO → **GPIO 11** (through a 3.3 V-safe connection)  

- **Speaker (passive piezo)**  
  - `+` → **GPIO 20**  
  - `–` → GND  

> Ask your mentor if you’re unsure about the ultrasonic ECHO wiring. Protect the Pico’s 3.3 V pins.

### New: SSD1306 OLED (I2C)

Use I2C0 so we avoid motor pins later:

- **OLED VCC** → 3V3  
- **OLED GND** → GND  
- **OLED SDA** → **GP0**  
- **OLED SCL** → **GP1**

---

# 2. File Layout on the Pico

We’ll keep files small and focused:

```text
/flash           (Pico 2 W internal storage)

  main.py             # Entry point: connect WiFi, show IP, start web dashboard
  wifi_config.py      # WiFi name + password only (students edit this)
  wifi.py             # WiFi helper (connect_wifi)
  oled_status.py      # OLED setup + show_wifi_ip
  web_dashboard.py    # HTTP server + LED/sensor routes

  ssd1306.py          # SSD1306 driver (copied once, no edits)
```

> In Thonny, use **"Save to → Raspberry Pi Pico"** to put these files directly on the board.  
> If you name the main file `main.py`, it auto-runs when the Pico powers on.

---

# 3. Step 1 – WiFi Config & Connect

## 3.1 `wifi_config.py` – secrets only

Create a new file on the Pico called **`wifi_config.py`**:

```python
# wifi_config.py
# Put your local WiFi settings here.
# Do NOT commit this file to GitHub.

SSID = "CHANGE_ME_WIFI_NAME"
PASSWORD = "CHANGE_ME_PASSWORD"
```

Students only edit this file when they move between home/school/library networks.

---

## 3.2 `wifi.py` – reusable connect helper

Create **`wifi.py`** on the Pico:

```python
# wifi.py
import network
import time
from wifi_config import SSID, PASSWORD

def connect_wifi():
    """
    Connect Pico 2 W to WiFi in station (client) mode.
    Returns IP address string on success, or None on failure.
    """
    wlan = network.WLAN(network.STA_IF)   # station/client interface
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
    else:
        print("WiFi connection failed.")
        return None

# Optional: quick test
if __name__ == "__main__":
    connect_wifi()
```

**Key ideas:**

- `network.WLAN(network.STA_IF)` = Pico acts like a laptop joining an existing network.  
- `wlan.ifconfig()[0]` gives the **IP address** (e.g., `192.168.0.45`).

---

# 4. Step 2 – Show IP on the OLED

We’ll use the MicroPython SSD1306 driver. (Copy a standard `ssd1306.py` into the Pico once; no changes needed.)

## 4.1 `oled_status.py`

Create **`oled_status.py`** on the Pico:

```python
# oled_status.py
from machine import Pin, I2C
import ssd1306

# I2C0 on GP0 (SDA) and GP1 (SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def show_wifi_ip(ip_str):
    """
    Clear the screen and display the Pico's IP address.
    """
    oled.fill(0)  # clear
    oled.text("Pico 2 W Online", 0, 0)
    oled.text("Browse to:", 0, 16)
    oled.text(ip_str, 0, 32)
    oled.show()

def show_status_line(line):
    """
    Optional: show a short status line under the IP later.
    """
    oled.fill_rect(0, 48, 128, 16, 0)  # clear bottom area
    oled.text(line, 0, 48)
    oled.show()

# Quick test:
if __name__ == "__main__":
    show_wifi_ip("192.168.0.45")
```

Run this file once from Thonny to confirm the OLED wiring is correct.

---

# 5. Step 3 – Web Dashboard: Design

We want a **very simple web page** that works on phones and laptops:

- Shows:
  - Pico’s **IP address**  
  - Latest **distance** (in cm)  
  - **Button** state (Pressed/Released)  
  - **LED** state (On/Off)  
- Lets you:
  - Turn the status LED ON/OFF.

Example layout:

```text
Pico WiFi Dashboard
IP: 192.168.0.45

[ LED ON ]  [ LED OFF ]

Distance: 23.4 cm
Button: Released
LED: OFF
```

Every time you click a button or refresh, the Pico:

1. Reads the **current distance** and **button** state.  
2. Updates the LED if needed.  
3. Returns a fresh copy of the page.

---

# 6. Step 4 – Web Dashboard Code

## 6.1 `web_dashboard.py`

Create **`web_dashboard.py`**:

```python
# web_dashboard.py
import socket
from machine import Pin
from picozero import LED, Button, DistanceSensor

# Reuse Lab 03 pins
STATUS_LED_PIN = 14
BUTTON_PIN = 13
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)

onboard_led = Pin("LED", Pin.OUT)  # Pico's built-in LED

def read_distance_cm():
    """
    Use picozero DistanceSensor to get distance in centimeters.
    """
    d_m = sensor.distance        # meters (float)
    return d_m * 100.0

def build_page(ip, distance_cm, button_pressed, led_on):
    """
    Build a simple HTML page string with current readings.
    """
    button_text = "Pressed" if button_pressed else "Released"
    led_text = "ON" if led_on else "OFF"

    html = f"""HTTP/1.1 200 OK
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
    return html

def run_server(ip):
    """
    Start a simple HTTP server on port 80.
    """
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

            # Parse the first line: "GET /path HTTP/1.1"
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

            response = build_page(ip, distance_cm, button_pressed, led_on)
            cl.send(response)
        except Exception as e:
            print("Error:", e)
        finally:
            cl.close()
```

> This server is **very simple** on purpose. In later labs you can add more routes (e.g., `/beep`, `/mode/active`, `/mode/idle`).

---

# 7. Step 5 – Glue It Together with `main.py`

Create **`main.py`** so the Pico auto-connects and starts the dashboard:

```python
# main.py
from wifi import connect_wifi
from oled_status import show_wifi_ip, show_status_line
from web_dashboard import run_server

def main():
    ip = connect_wifi()
    if not ip:
        # Could show an error on the OLED here if you want
        return

    # Show IP on the OLED
    show_wifi_ip(ip)
    show_status_line("Waiting for web...")

    # Start the web dashboard (loop forever)
    run_server(ip)

if __name__ == "__main__":
    main()
```

### Run Steps (Thonny)

1. Confirm Thonny interpreter is set to **MicroPython (Raspberry Pi Pico)**.  
2. Save all the files (`wifi_config.py`, `wifi.py`, `oled_status.py`, `web_dashboard.py`, `ssd1306.py`, `main.py`) to **Raspberry Pi Pico**.  
3. Edit `wifi_config.py` with the correct WiFi.  
4. Click **Run ▶** on `main.py`.

You should see:

- In Thonny Shell: “Connected! IP: …” and “Listening on …”  
- On the OLED: “Pico 2 W Online” and your IP address.

On a phone or laptop on the **same WiFi**, open a browser and go to:

```text
http://<that-ip-address>/
```

You should see the dashboard page. Click **LED ON/OFF** and watch the status LED and onboard LED change.

---

# Vocabulary

- **WiFi STA mode (Station mode)** – The Pico joins an existing WiFi network like a laptop or phone.  
- **SSID** – The name of a WiFi network (what you see in the WiFi list).  
- **IP address** – A numeric address like `192.168.0.45` that identifies the Pico on the network.  
- **HTTP** – The protocol a browser uses to talk to web servers.  
- **Route / Path** – The part of the URL after the host, like `/led/on` or `/`.  
- **Dashboard** – A page that shows live data and controls in one place.

---

# Check Your Understanding

1. Why do we display the Pico’s **IP address** on the OLED instead of only printing it in Thonny?  
2. What happens inside `run_server` when you click **LED ON** in your browser?  
3. How does the Pico get the **latest distance and button state** for each page load?  
4. If the dashboard shows `Distance: 0.0 cm` all the time, what wiring or code problems could cause that?

---

# Next Steps & Extensions

Once your WiFi dashboard is working, try one of these:

- **Add sensor buttons:**  
  Add a `/beep` route that plays a short sound on the speaker, and a new button on the page to call it.

- **OLED status:**  
  Use `show_status_line("LED ON")` or `show_status_line("Button pressed")` inside your routes to mirror web actions on the OLED.

- **Color-coded distance:**  
  Use the RGB LED from Lab 03 and update its color in `web_dashboard.py` based on the latest distance reading, then display that color info on the page.

Later, you’ll combine this with **PicoBot drive functions**, turning the page into a full **web remote for a robot**.
