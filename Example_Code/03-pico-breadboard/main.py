
# Pico Breadboard Lab — Starter
# Interpreter: MicroPython (Raspberry Pi Pico). Save as main.py on the Pico.

from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms

LED_PIN = 15
BTN_PIN = 14
DEBOUNCE_MS = 30

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)  # For PULL_UP wiring, change to Pin.PULL_UP

last_state = btn.value()
last_change = ticks_ms()

def set_led(on: bool):
    led.value(1 if on else 0)

def blink(times=3, on_ms=200, off_ms=200):
    for _ in range(times):
        set_led(True); sleep_ms(on_ms)
        set_led(False); sleep_ms(off_ms)

def read_button_debounced():
    global last_state, last_change
    now = ticks_ms()
    raw = btn.value()
    if raw != last_state and ticks_diff(now, last_change) > DEBOUNCE_MS:
        last_state = raw
        last_change = now
        return raw  # edge: 1=pressed, 0=released (with PULL_DOWN wiring)
    return None

def main():
    try:
        while True:
            edge = read_button_debounced()
            if edge is None:
                sleep_ms(5)
                continue
            if edge == 1:  # pressed
                # TODO: fast blink while held (or simply LED on while held)
                set_led(True)
            else:          # released
                # TODO: slow blink three times on release
                set_led(False)
                blink(times=3, on_ms=120, off_ms=120)
    except KeyboardInterrupt:
        pass
    finally:
        set_led(False)

if __name__ == "__main__":
    main()
