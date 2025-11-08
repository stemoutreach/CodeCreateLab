# STUDENT_START — 03 Pico Breadboard Lab

**Use this only if you're stuck for 5–7 minutes.**
Minimal starter with TODOs — no full solution.

```python
from picozero import Button, LED, RGBLED, Speaker
from time import sleep

BTN_PIN = 15
LED_PIN = 14
RGB_PINS = (13, 12, 11)  # R,G,B
BUZZER_PIN = 10  # optional

button = Button(BTN_PIN)
led = LED(LED_PIN)
rgb = RGBLED(*RGB_PINS)

try:
    buzzer = Speaker(BUZZER_PIN)
except Exception:
    buzzer = None

prev = False

def read_button():
    return button.is_pressed

def show_led(on):
    led.on() if on else led.off()

def show_rgb(pressed):
    # TODO: choose your own colors
    if pressed:
        rgb.color = (0,1,0)
    else:
        rgb.color = (0,0,1)

def beep_once(ms=80):
    if buzzer:
        buzzer.on()
        sleep(ms/1000)
        buzzer.off()

def main():
    global prev
    print("Pico Breadboard Lab")
    while True:
        try:
            pressed = read_button()
            # Mirror LED
            show_led(pressed)
            # RGB feedback
            show_rgb(pressed)
            # Optional: rising-edge beep
            if pressed and not prev:
                # TODO: uncomment to enable
                # beep_once(100)
                pass
            prev = pressed
            sleep(0.02)  # debounce
        except KeyboardInterrupt:
            break
    # cleanup
    show_led(False)
    rgb.color = (0,0,0)
    if buzzer:
        buzzer.off()
    print("Goodbye!")

if __name__ == "__main__":
    main()
```
