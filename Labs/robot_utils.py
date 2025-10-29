
"""
robot_utils.py — PicoBot helpers (MicroPython)
Pins assume the wiring from the PicoBot guide.
Adjust GPIOs if your wiring differs.
"""
from machine import Pin, time_pulse_us
import time
from typing import Optional

# --- Motor GPIO mapping (L298N) ---
In1 = Pin(6, Pin.OUT)   # Motor A IN1
In2 = Pin(7, Pin.OUT)   # Motor A IN2
EN_A = Pin(8, Pin.OUT)  # Motor A ENA (used as ON/OFF; change to PWM for speed)

In3 = Pin(4, Pin.OUT)   # Motor B IN3
In4 = Pin(3, Pin.OUT)   # Motor B IN4
EN_B = Pin(2, Pin.OUT)  # Motor B ENB

# Enable motors (full power). To add speed control, switch EN_* to PWM.
EN_A.high()
EN_B.high()

# --- Ultrasonic pins ---
TRIG = Pin(14, Pin.OUT)
ECHO = Pin(15, Pin.IN)

# --- Tunables ---
TURN_DURATION = 0.40   # seconds; tune for your surface
BACKUP_DURATION = 0.30 # seconds; used before turns (optional)
SAFE_DISTANCE = 12.0   # cm; treat closer as blocked

# --- Motor primitives ---
def stop_motors() -> None:
    In1.low(); In2.low()
    In3.low(); In4.low()

def move_forward() -> None:
    In1.high(); In2.low()
    In3.high(); In4.low()

def move_backward() -> None:
    In1.low();  In2.high()
    In3.low();  In4.high()

def turn_left(duration: float = TURN_DURATION) -> None:
    # Left wheel backward, right wheel forward
    In1.low();  In2.high()
    In3.high(); In4.low()
    time.sleep(duration)
    stop_motors()

def turn_right(duration: float = TURN_DURATION) -> None:
    # Left wheel forward, right wheel backward
    In1.high(); In2.low()
    In3.low();  In4.high()
    time.sleep(duration)
    stop_motors()

# --- Distance ---
def read_distance_cm(timeout_us: int = 25000) -> Optional[float]:
    """Return distance in cm, or None on timeout."""
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    dur = time_pulse_us(ECHO, 1, timeout_us)
    if dur < 0:
        return None
    # Speed of sound 0.0343 cm/us; divide by 2 (out & back)
    return (dur * 0.0343) / 2.0
