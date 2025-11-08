
# Coach Solution — PicoBot Drive Basics

> **Coach-only** reference solution matching the student `main.py` scaffold.

```python
from machine import Pin, PWM
from time import sleep_ms

ENA_PIN = 2; ENB_PIN = 3
IN1_PIN = 4; IN2_PIN = 5; IN3_PIN = 6; IN4_PIN = 7

PWM_FREQ = 1000
PWM_DUTY = 65000
TRIM_LEFT = 1.00
TRIM_RIGHT = 1.00

ena = PWM(Pin(ENA_PIN)); enb = PWM(Pin(ENB_PIN))
ena.freq(PWM_FREQ); enb.freq(PWM_FREQ)

in1 = Pin(IN1_PIN, Pin.OUT); in2 = Pin(IN2_PIN, Pin.OUT)
in3 = Pin(IN3_PIN, Pin.OUT); in4 = Pin(IN4_PIN, Pin.OUT)

def set_trim(left: float, right: float):
    global TRIM_LEFT, TRIM_RIGHT
    TRIM_LEFT = max(0.0, min(1.2, left))
    TRIM_RIGHT = max(0.0, min(1.2, right))

def _drive_raw(left_duty: int, right_duty: int):
    if left_duty > 0: in1.value(1); in2.value(0)
    elif left_duty < 0: in1.value(0); in2.value(1)
    else: in1.value(0); in2.value(0)

    if right_duty > 0: in3.value(1); in4.value(0)
    elif right_duty < 0: in3.value(0); in4.value(1)
    else: in3.value(0); in4.value(0)

    ld = int(abs(left_duty) * TRIM_LEFT)
    rd = int(abs(right_duty) * TRIM_RIGHT)
    ena.duty_u16(min(65535, ld))
    enb.duty_u16(min(65535, rd))

def stop():
    _drive_raw(0, 0)

def forward(ms: int):
    _drive_raw(PWM_DUTY, PWM_DUTY)
    sleep_ms(ms); stop()

def turn_left(ms: int):
    _drive_raw(-PWM_DUTY, PWM_DUTY)
    sleep_ms(ms); stop()

def turn_right(ms: int):
    _drive_raw(PWM_DUTY, -PWM_DUTY)
    sleep_ms(ms); stop()

def demo_square(side_ms=1000, turn_ms=500):
    for _ in range(4):
        forward(side_ms); sleep_ms(250)
        turn_right(turn_ms); sleep_ms(250)

def main():
    try:
        # Example trim
        # set_trim(1.00, 0.95)
        demo_square()
    except KeyboardInterrupt:
        pass
    finally:
        stop()

if __name__ == "__main__":
    main()
```
