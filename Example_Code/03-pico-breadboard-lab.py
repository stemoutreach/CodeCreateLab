
"""
Pico Breadboard Lab — Starter
Button + LED (required) and optional RGB/Ultrasonic
"""
from picozero import Button, LED, RGBLED
from time import sleep
from typing import Tuple

# --- Pins (adjust to your wiring) ---
PIN_LED = 14
PIN_BUTTON = 15
PIN_RGB = (13, 12, 11)  # (R, G, B)

# Optional ultrasonic pins (uncomment if using)
# PIN_TRIG = 10
# PIN_ECHO = 9

# --- Devices ---
led = LED(PIN_LED)
button = Button(PIN_BUTTON)      # library uses internal pull-up
try:
    rgb = RGBLED(*PIN_RGB)       # comment out if not installed
    HAS_RGB = True
except Exception:
    HAS_RGB = False
    rgb = None  # type: ignore

# --- Helpers ---
def read_button() -> bool:
    return button.is_pressed

def show_status(pressed: bool) -> None:
    """Required behavior: button controls LED."""
    if pressed:
        led.on()
    else:
        led.off()

def set_rgb_color(rgb_led: RGBLED, color: Tuple[float, float, float]) -> None:
    """Set RGB using floats 0.0–1.0 (picozero format)."""
    rgb_led.color = color

# --- Optional Ultrasonic (HC-SR04) ---
# If you enable this, you'll need machine.Pin and time_pulse_us:
# from machine import Pin, time_pulse_us
# TRIG = Pin(PIN_TRIG, Pin.OUT); ECHO = Pin(PIN_ECHO, Pin.IN)
# def read_distance_cm(timeout_us: int = 25000):
#     TRIG.low(); sleep(0.002)
#     TRIG.high(); sleep(0.00001); TRIG.low()
#     dur = time_pulse_us(ECHO, 1, timeout_us)
#     if dur < 0:
#         return None
#     return (dur * 0.0343) / 2.0

# --- Main ---
try:
    print("Pico Breadboard Lab — Button + LED" + (" + RGB" if HAS_RGB else ""))
    while True:
        pressed = read_button()
        show_status(pressed)

        # Optional: RGB feedback
        if HAS_RGB:
            set_rgb_color(rgb, (0.0, 1.0, 0.0) if pressed else (0.0, 0.0, 0.0))

        sleep(0.02)  # debounce / loop pace
except KeyboardInterrupt:
    led.off()
    if HAS_RGB:
        set_rgb_color(rgb, (0.0, 0.0, 0.0))
    print("\nGoodbye!")
