
# Lab 2 – Raspberry Pi Pico Breadboarding (Solution)

## Overview  
This solution demonstrates how to implement a simple interactive distance detection system using a Raspberry Pi Pico, ultrasonic sensor, and RGB LED. The code reads distance in inches and updates the RGB LED color based on how close an object is.

---

## Solution Code

```python
from machine import Pin, PWM, time_pulse_us
import time

# --- Pin setup ---
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)
BUTTON = Pin(15, Pin.IN, Pin.PULL_DOWN)

RGB = (PWM(Pin(18)), PWM(Pin(19)), PWM(Pin(20)))  # R, G, B channels
for channel in RGB:
    channel.freq(1000)  # 1 kHz PWM for smooth colour control

# --- Constants ---
SPEED_CM_PER_US = 0.0343 / 2     # speed of sound (cm/us) /2 for round-trip
MIN_INCH = 8                     # < 8"  -> RED
MID_INCH = 16                    # < 16" -> BLUE

# --- Helper functions ---
def set_rgb(r: int, g: int, b: int) -> None:
    """Set RGB LED colour (0–255 each)."""
    for pwm, val in zip(RGB, (r, g, b)):
        pwm.duty_u16(int(val * 65535 / 255))

def read_distance_inches() -> float:
    """Return distance in inches measured by HC-SR04."""
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    duration = time_pulse_us(ECHO, 1, 30_000)
    distance_cm = duration * SPEED_CM_PER_US
    return distance_cm / 2.54

def colour_for_distance(dist_in: float) -> tuple[int, int, int]:
    if dist_in < MIN_INCH:
        return (255, 0, 0)        # red
    elif dist_in < MID_INCH:
        return (0, 0, 255)        # blue
    else:
        return (0, 255, 0)        # green

# --- Main loop ---
try:
    while True:
        if BUTTON.value():
            distance = read_distance_inches()
            print(f"Distance: {distance:.2f} inches")
            r, g, b = colour_for_distance(distance)
            set_rgb(r, g, b)
            time.sleep(0.3)
        else:
            set_rgb(20, 20, 20)
            time.sleep(0.1)
            set_rgb(0, 0, 0)
            time.sleep(0.9)

except KeyboardInterrupt:
    set_rgb(0, 0, 0)
```

---

## Notes
- RGB LED changes color based on distance range.
- Button triggers ultrasonic reading.
- Code includes heartbeat LED to indicate script is running.
- Students may customize this with optional components such as buzzers or traffic light indicators.
