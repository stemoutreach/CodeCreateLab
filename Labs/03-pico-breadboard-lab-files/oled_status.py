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
