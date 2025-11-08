# STUDENT_START — 04 PicoBot Drive Basics (No Sensors)

No-spoilers starter that mirrors the lab. Copy only what you need.

```python
from machine import Pin, PWM
from time import sleep_ms

# EDIT to match your wiring
ENA = 2; IN1 = 3; IN2 = 4
ENB = 5; IN3 = 6; IN4 = 7

BASE_DUTY = 0.6
LEFT_TRIM = 0.00
RIGHT_TRIM = 0.00

pwm_left = PWM(Pin(ENA)); pwm_right = PWM(Pin(ENB))
pwm_left.freq(1000); pwm_right.freq(1000)

in1 = Pin(IN1, Pin.OUT); in2 = Pin(IN2, Pin.OUT)
in3 = Pin(IN3, Pin.OUT); in4 = Pin(IN4, Pin.OUT)

def duty_to_u16(frac): return int(max(0.0, min(1.0, float(frac))) * 65535)

def stop():
    in1.value(0); in2.value(0); in3.value(0); in4.value(0)
    pwm_left.duty_u16(0); pwm_right.duty_u16(0)

def set_left(direction, duty): pass   # TODO
def set_right(direction, duty): pass  # TODO
def forward(duty=BASE_DUTY): pass     # TODO
def turn_left(duty=BASE_DUTY): pass   # TODO
def turn_right(duty=BASE_DUTY): pass  # TODO
def drive_square(side_ms=1200, turn_ms=700, duty=BASE_DUTY): pass  # TODO

def main():
    print("PicoBot Drive Basics — wheels OFF table for first run!")
    try:
        stop()
        # TODO: quick spin test (wheels up)
        # TODO: drive_square()
    finally:
        stop()
        print("Stopped.")

if __name__ == "__main__":
    main()
```
