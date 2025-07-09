# Lab 2 – Raspberry Pi Pico Breadboarding

## Overview
Interface a push‑button, an ultrasonic distance sensor (HC‑SR04), a single‑colour LED, and an RGB LED.  
Press the button to trigger a distance reading; LEDs provide immediate visual feedback.

## Learning objectives
- Wire digital input (button with pull‑down)
- Drive digital output (LED)
- Use PWM for RGB LED colour mixing
- Measure distance with `machine.Pin` and `machine.time_pulse_us`
- Structure MicroPython code with functions and modules

## Prerequisites
Follow **Guides/Pico_Breadboard_Guide.md** to verify your Thonny setup.

## Circuit
See `Assets/Pico_Breadboard_Schematic.png`.

## Starter code

```python
# pico_distance_alert.py
from machine import Pin, PWM
import time

TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)
BUTTON = Pin(15, Pin.IN, Pin.PULL_DOWN)
LED  = Pin(13, Pin.OUT)
RGB  = (PWM(Pin(18)), PWM(Pin(19)), PWM(Pin(20)))  # R, G, B pins

SPEED_CM_PER_US = 0.0343 / 2

def set_rgb(r, g, b):
    for pwm, val in zip(RGB, (r, g, b)):
        pwm.freq(1000)
        pwm.duty_u16(int(val * 65535 / 255))

def read_distance_cm():
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    us = time_pulse_us(ECHO, 1, 30000)
    return us * SPEED_CM_PER_US

while True:
    if BUTTON.value():
        dist = read_distance_cm()
        print(f"Distance: {dist:.1f} cm")

        if dist < 20:
            LED.high()
            set_rgb(255, 0, 0)        # red
        else:
            LED.low()
            set_rgb(0, 255, 0)        # green

        time.sleep(0.3)

    # TODO: maybe add a heartbeat LED blink here
```

## Stretch goals
- Cycle RGB colours proportionally to distance.
- Display distance on an I²C OLED (see Guide).
