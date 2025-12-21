# 03 — oled_status.py Reference

> ### Quick Summary  
> **Level:** 03 • **Time:** 5–10 min  
> **Prereqs:** SSD1306 OLED wired to I2C0  
> **Hardware:** 0.96" SSD1306 OLED (128x64), Pico 2 W  
> **You’ll practice:** I2C display updates, keeping text within 16 characters

# What This File Does
`oled_status.py` owns the OLED and provides small helper functions:

- `show_wifi_ip(ip_str)`  
  Draws the top 3 lines:
  1. `Pico 2 W Online`
  2. `Browse to:`
  3. the IP address

- `show_status_line(text)`  
  Updates only the bottom line (the 4th line).

- `show_distance(distance_cm, active=True)`  
  Used by `web_dashboard.py` to show distance in a consistent format:
  - `active=False` → `Distance=PAUSED`
  - `distance_cm is None` → `Distance=---`
  - else → `Distance=12.3cm`

# Why the Text Looks “Short”
With the default SSD1306 font, you get about **16 characters per line**.
`Distance=12.3cm` is designed to fit.

# Common Problems
- **Blank screen**
  - Check power (3V3 + GND) and I2C wiring.
  - Confirm SDA=GP0 and SCL=GP1 for I2C0.
- **Text doesn’t change**
  - Make sure you call `oled.show()` after writing (these helpers do).
