# 03 — Pico Smart Distance Station — STUDENT_START

This file is your **guided hint path** for the lab:

- Use it when you’re stuck for **5–7 minutes**, not right away.
- Work **top to bottom**, one part at a time.
- The **Full Starter** at the bottom matches the Lab’s Skeleton Starter (with TODOs).  
  Use it to compare structure with your own code.

---

## How to Use This File

1. Try the Lab steps on your own first.  
2. If you’re stuck on a specific part (sensor, LEDs, speaker, button):
   - Scroll to that section here.
   - Read the notes and **mini examples**.
3. When your design feels messy or you’re not sure about structure:
   - Scroll to **Full Starter**.
   - Compare the functions and main loop shape to yours.
   - Keep the TODOs for you to fill in.

---

## Part 1 — Ultrasonic Distance Sensor Sanity Check

Goal: get **just the distance sensor** working and printing numbers.

Create a tiny test file (separate from your main lab file) like `distance_test.py`.

### 1A. Minimal wiring check

Before coding, confirm:

- VCC → 5V (or 3.3V if your module is 3.3V-safe).
- GND → GND.
- TRIG → GPIO 3.
- ECHO → GPIO 2 (through a 3.3V-safe connection as covered in the Guide).

### 1B. Tiny distance test

```python
from picozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=2, trigger=3)

print("Distance sensor test starting...")

while True:
    d_m = sensor.distance      # distance in meters
    d_cm = d_m * 100
    print(f"{d_cm:.1f} cm")
    sleep(0.2)
```

**What to look for:**

- Move your hand closer and farther.
- Numbers should go **down** when you get closer, **up** when you move away.
- If you only see 0 or nonsense:
  - Check wiring.
  - Check echo pin safety.
  - Slow down the loop a bit (e.g., `sleep(0.3)`).

Once this works, **copy just the idea** (not the whole file) into your main lab program.

---

## Part 2 — Add a Status LED

Goal: show a clear **“system on”** or **“active mode”** indicator.

Make a small test file `status_led_test.py`:

```python
from picozero import LED
from time import sleep

status_led = LED(14)

print("Status LED test...")
while True:
    status_led.on()
    sleep(0.5)
    status_led.off()
    sleep(0.5)
```

If that works:

- In your main program, turn the LED **on** when the system is **active**.
- Turn it **off** when in **idle**.

You can use a global `mode` variable holding `"idle"` or `"active"` and let a function like `update_lights()` decide what to do.

---

## Part 3 — RGB LED Distance Bands

Goal: map distance to **colors** (traffic light style).

Test the RGB LED separately in `rgb_test.py`:

```python
from picozero import RGBLED
from time import sleep

rgb = RGBLED(red=16, green=17, blue=18)

print("RGB LED test...")
rgb.color = (1, 0, 0)   # red
sleep(1)
rgb.color = (0, 1, 0)   # green
sleep(1)
rgb.color = (0, 0, 1)   # blue
sleep(1)
rgb.off()
```

Once you see all three colors, bring the idea into your main file:

- Decide thresholds, for example:
  - `close` < 20 cm
  - `medium` 20–40 cm
  - `far` > 40 cm

Inside `update_lights(distance_cm)`:

- `far` → green  
- `medium` → yellow (e.g. `(1, 1, 0)` or `(0.5, 0.5, 0)`)  
- `close` → red  

Remember: when `mode == "idle"`, you might want RGB **off** or a neutral color.

---

## Part 4 — Speaker Patterns

Goal: turn distance into different **beeping patterns**.

First, make sure your speaker works at all in `speaker_test.py`:

```python
from picozero import Speaker
from time import sleep

speaker = Speaker(12)

print("Speaker test...")
speaker.play(440, 0.5)  # A4 for half a second
sleep(0.5)
speaker.play(660, 0.5)  # higher tone
sleep(0.5)
speaker.off()
print("Done.")
```

If you **hear something**, you’re good.

### Idea: simple patterns

In your lab’s `update_sound(distance_cm)`:

- When `mode == "idle"` → `speaker.off()`.
- When `far` → no beep (silent).
- When `medium` → occasional beep:
  - Example: every few loops, call `speaker.beep(on_time=0.05, off_time=0.05, n=1)`.
- When `close` → more urgent:
  - Use more frequent beeps or longer beep time.

**Important:** Don’t put long `sleep()` calls inside `update_sound`. Let your **main loop sleep** a little and keep `update_sound()` quick so the distance sensor still updates often.

---

## Part 5 — Button to Toggle Modes

Goal: use the pushbutton to switch between `"idle"` and `"active"` (or to mute/unmute).

Test in a tiny file `button_test.py`:

```python
from picozero import Button
from time import sleep

button = Button(15)

print("Button test. Press and release...")
while True:
    if button.is_pressed:
        print("Pressed")
    else:
        print("Not pressed")
    sleep(0.1)
```

You’ll see the printout change when you press and release.

### Edge vs level

In the final lab, you usually want to **toggle on a press**, not spam toggles while you hold it.

Pattern idea:

- Keep a global `mode` (`"idle"` / `"active"`) and a global `prev_pressed` (`False` / `True`).
- Each loop:
  - Check `button.is_pressed`.
  - If `not prev_pressed` and `button.is_pressed`, then the button was **just pressed** → toggle `mode`.
  - Set `prev_pressed = button.is_pressed` at the end.

You’ll wire this into your `handle_button()` function.

---

## Full Starter (structure to compare)

This is the **same structure** as in the Lab’s Skeleton Starter, collected here in one place.  
It still has TODOs — *you* decide thresholds, colors, and patterns.

```python
from picozero import LED, Button, RGBLED, DistanceSensor, Speaker
from time import sleep

# --- Pin setup (matches the lab instructions) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 15
RGB_RED_PIN = 16
RGB_GREEN_PIN = 17
RGB_BLUE_PIN = 18
ULTRASONIC_ECHO_PIN = 2
ULTRASONIC_TRIG_PIN = 3
SPEAKER_PIN = 12

# --- Objects ---
status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
rgb = RGBLED(red=RGB_RED_PIN, green=RGB_GREEN_PIN, blue=RGB_BLUE_PIN)
sensor = DistanceSensor(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)

# Simple mode variable: "idle" or "active"
mode = "idle"

# Optional: track previous button state for edge detection
prev_pressed = False


def read_distance_cm():
    '''Return the distance in centimeters (float).'''
    d_m = sensor.distance        # distance in meters
    d_cm = d_m * 100
    return d_cm


def update_lights(distance_cm):
    '''
    TODO: Set status_led and rgb color based on:
      - mode (idle vs active)
      - distance_cm (far / medium / close)

    Example idea (you can change thresholds/colors):
      - idle: status off, RGB off
      - far:  status on, RGB green
      - medium: status on, RGB yellow
      - close: status on, RGB red
    '''
    global mode

    if mode == "idle":
        status_led.off()
        rgb.off()
        return

    # mode == "active"
    status_led.on()

    # TODO: choose colors for distance ranges.
    # Example thresholds (change if you like):
    # close < 20 cm, medium 20–40 cm, far > 40 cm
    # Use rgb.color = (r, g, b) with values 0.0–1.0
    # e.g. rgb.color = (1, 0, 0)  # red


def update_sound(distance_cm):
    '''
    TODO: Decide when/how the speaker should beep.

    Ideas:
      - idle: speaker.off()
      - far:  silent
      - medium: short beep once in a while
      - close: faster beeps

    Keep this function quick so the main loop stays responsive.
    '''
    global mode

    if mode == "idle":
        speaker.off()
        return

    # TODO: pick a pattern based on distance_cm.
    # Hint: very short play() calls + no long sleeps here.
    # You can also choose to call speaker.off() when "far".


def handle_button():
    '''
    TODO: Flip mode when the button is pressed.

    Use Button.is_pressed or when_pressed/when_released callbacks.

    Simple approach:
      - check if button.is_pressed and it was not pressed last loop
      - then toggle mode between "idle" and "active"
    '''
    global mode, prev_pressed

    # TODO: detect the transition from "not pressed" to "pressed"
    # Example pattern (not full code):
    #
    # pressed_now = button.is_pressed
    # if (not prev_pressed) and pressed_now:
    #     mode = "active" if mode == "idle" else "idle"
    # prev_pressed = pressed_now
    #
    # Fill in the real code here.


def main():
    print("Pico Smart Distance Station starting...")
    print("Move your hand in front of the sensor to test.")
    try:
        while True:
            handle_button()

            if mode == "active":
                distance_cm = read_distance_cm()
                print(f"Distance: {distance_cm:.1f} cm")
            else:
                distance_cm = None  # no reading in idle

            # Even if distance_cm is None, update_lights/sound can handle it.
            # For example, they can ignore None when in idle mode.
            update_lights(distance_cm if distance_cm is not None else 0)
            update_sound(distance_cm if distance_cm is not None else 0)

            sleep(0.1)  # small delay to avoid spamming the sensor
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        status_led.off()
        rgb.off()
        speaker.off()


if __name__ == "__main__":
    main()
```

---

### Final Tip

If your version doesn’t match this structure exactly, that’s okay:

- If it **works and is readable**, it’s valid.
- Use this file to **borrow good ideas** (separate functions, main loop pattern).
- Keep making small changes and re-testing — that’s how real embedded projects grow.
