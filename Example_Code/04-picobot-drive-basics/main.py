
# PicoBot — Drive Basics (L298N, no sensors)
# Save as: main.py (on Pico) to auto-run on boot

from machine import Pin, PWM
from time import sleep_ms

# === CONFIGURE YOUR PINS HERE ===
# Adjust these to match your wiring (see Guide 04).
ENA_PIN = 2   # PWM enable for left motor
ENB_PIN = 3   # PWM enable for right motor
IN1_PIN = 4   # Left motor IN1
IN2_PIN = 5   # Left motor IN2
IN3_PIN = 6   # Right motor IN3
IN4_PIN = 7   # Right motor IN4

PWM_FREQ = 1000          # 1 kHz is fine for DC motors
PWM_DUTY = 65000         # Base duty (0..65535). Start around 55-70% of 65535.
TRIM_LEFT = 1.00         # Adjust to balance motors (e.g., 0.95 means 5% slower)
TRIM_RIGHT = 1.00

# === SETUP ===
ena = PWM(Pin(ENA_PIN))
enb = PWM(Pin(ENB_PIN))
ena.freq(PWM_FREQ)
enb.freq(PWM_FREQ)

in1 = Pin(IN1_PIN, Pin.OUT)
in2 = Pin(IN2_PIN, Pin.OUT)
in3 = Pin(IN3_PIN, Pin.OUT)
in4 = Pin(IN4_PIN, Pin.OUT)

def set_trim(left: float, right: float):
    """Set per-side speed multipliers to keep the bot driving straight."""
    global TRIM_LEFT, TRIM_RIGHT
    TRIM_LEFT = max(0.0, min(1.2, left))
    TRIM_RIGHT = max(0.0, min(1.2, right))

def _drive_raw(left_duty: int, right_duty: int):
    """Low-level: set directions and PWM for each side (+ forward, - reverse, 0 stop)."""
    # Left
    if left_duty > 0:
        in1.value(1); in2.value(0)
    elif left_duty < 0:
        in1.value(0); in2.value(1)
    else:
        in1.value(0); in2.value(0)
    # Right
    if right_duty > 0:
        in3.value(1); in4.value(0)
    elif right_duty < 0:
        in3.value(0); in4.value(1)
    else:
        in3.value(0); in4.value(0)

    # Apply PWM (abs value), include trim
    ld = int(abs(left_duty) * TRIM_LEFT)
    rd = int(abs(right_duty) * TRIM_RIGHT)
    ena.duty_u16(min(65535, ld))
    enb.duty_u16(min(65535, rd))

def stop():
    """Immediately stop both motors."""
    _drive_raw(0, 0)

def forward(ms: int):
    """Drive forward for ms milliseconds."""
    # TODO: set both sides forward using PWM_DUTY and sleep for ms
    _drive_raw(PWM_DUTY, PWM_DUTY)
    sleep_ms(ms)
    stop()

def turn_left(ms: int):
    """Pivot left for ms milliseconds (left back, right forward)."""
    # TODO: implement a pivot (e.g., left negative, right positive)
    _drive_raw(-PWM_DUTY, PWM_DUTY)
    sleep_ms(ms)
    stop()

def turn_right(ms: int):
    """Pivot right for ms milliseconds (left forward, right back)."""
    # TODO: mirror of turn_left
    _drive_raw(PWM_DUTY, -PWM_DUTY)
    sleep_ms(ms)
    stop()

def demo_square(side_ms=1000, turn_ms=500):
    """Drive a simple timed square."""
    for _ in range(4):
        forward(side_ms)
        sleep_ms(250)
        turn_right(turn_ms)
        sleep_ms(250)

def main():
    try:
        # Example: slight trim if your bot veers right
        # set_trim(1.00, 0.95)
        demo_square()
    except KeyboardInterrupt:
        pass
    finally:
        stop()

if __name__ == "__main__":
    main()
