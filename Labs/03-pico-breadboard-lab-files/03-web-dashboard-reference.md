# 03 — web_dashboard.py Reference

> ### Quick Summary  
> **Level:** 03 • **Time:** 10–15 min  
> **Prereqs:** WiFi connected on Pico 2 W  
> **Hardware:** HC-SR04P (3.3V), RGB LED, optional SSD1306 OLED  
> **You’ll practice:** simple web server, JSON endpoint, polling, state toggles

# What This File Does
`web_dashboard.py` runs a tiny web server on the Pico and provides:

- `/` — a dashboard web page (HTML + JavaScript)
- `/data` — live JSON data (distance, button, capture state, RGB)
- `/capture/toggle` — flips **Capture** between ACTIVE and INACTIVE

The dashboard page polls `/data` automatically, so your readings update live.

# Capture State
Capture is a single shared state that controls whether the ultrasonic sensor is read:

## Capture INACTIVE
- Ultrasonic sensor is **not read**
- RGB LED is **OFF**
- OLED shows `Distance=PAUSED` (if OLED installed)

## Capture ACTIVE
- Ultrasonic sensor is read on a steady interval
- RGB LED color updates based on distance
- OLED shows `Distance=12.3cm`

You can toggle Capture from:
- The **web** button (**Toggle Capture**)
- The physical Pico **button on GPIO 13** (debounced)

# RGB Distance Colors (Part A Thresholds)
This matches the Lab Part A ranges:

- **RED:** distance **< 20 cm**
- **YELLOW:** distance **20–40 cm**
- **GREEN:** distance **> 40 cm**

The web page also shows RGB as **0–255** values.

# Settings You Can Tune (top of the file)
- `CLOSE_CM` and `MEDIUM_MAX_CM` — distance thresholds
- `_SENSOR_UPDATE_MS` — how often the Pico updates distance/RGB/OLED while ACTIVE
- `poll_ms` passed into `run_server(ip, poll_ms=500)` — how often the browser updates
- `RGB_COMMON_ANODE` — set `True` if your RGB LED is common-anode (colors look inverted)

# Troubleshooting
- **Web loads but distance never changes**
  - Make sure you opened the Pico’s IP from the OLED.
  - Make sure the browser is on the same WiFi network.
- **OLED stuck on `Distance=PAUSED`**
  - Confirm your `oled_status.py` includes `show_distance()`.
- **RGB colors wrong**
  - Double-check RGB pins (R=17, G=18, B=19).
  - Try `RGB_COMMON_ANODE = True`.
