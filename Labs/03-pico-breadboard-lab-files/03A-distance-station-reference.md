# 03A — Pico Smart Distance Station (Reference)

> ### Quick Summary
> **Level:** 03A • **Time:** 15–25 min  
> **Prereqs:** 02 (basic Pico + breadboard skills)  
> **Hardware:** Pico / Pico W / Pico 2W, HC-SR04P (or compatible ultrasonic), RGB LED, pushbutton, status LED, piezo speaker/buzzer  
> **You’ll practice:** reading a sensor, using thresholds, LED/RGB feedback, button state (toggle), simple sound patterns

This page is a *reference* for the **03_distance_station.py** code used in **Lab 03 (Part A)**. It explains what the code does, how it’s wired, and what to change if you want different behavior.

---

## What this program does

The Distance Station has **two modes**:

- **IDLE:** everything is off (quiet + no lights)
- **ACTIVE:** the Pico measures distance and gives feedback:
  - **RGB LED color** shows distance range  
    - **Green** = far  
    - **Yellow** = medium  
    - **Red** = close
  - **Speaker** beeps faster as you get closer  
  - **Status LED** turns on while ACTIVE

You press the **button** to toggle between **IDLE** and **ACTIVE**.

---

## Pin map used by this code

These pins match the code exactly:

| Part | Pico Pin (GPIO) | Code constant |
|---|---:|---|
| Status LED | GP14 | `STATUS_LED_PIN = 14` |
| Button | GP13 | `BUTTON_PIN = 13` |
| RGB LED Red | GP17 | `RGB_RED_PIN = 17` |
| RGB LED Green | GP18 | `RGB_GREEN_PIN = 18` |
| RGB LED Blue | GP19 | `RGB_BLUE_PIN = 19` |
| Ultrasonic TRIG | GP10 | `ULTRASONIC_TRIG_PIN = 10` |
| Ultrasonic ECHO | GP11 | `ULTRASONIC_ECHO_PIN = 11` |
| Speaker | GP20 | `SPEAKER_PIN = 20` |

---

## Wiring notes (important)

### 1) Button
- One side of the button to **GP13**
- The other side to **GND**
- The `picozero.Button()` class uses an internal pull-up by default, so the pin reads **pressed** when it’s pulled to ground.

### 2) Status LED
- GP14 → resistor → LED → GND  
  (Resistor typically 220Ω–330Ω)

### 3) RGB LED
- Use **three resistors** (one per color) if your RGB LED doesn’t have them built-in.
- Connect each color leg to GP17/18/19 through a resistor, and connect the common leg to:
  - **GND** (common cathode) ✅ *most common*
  - or **3.3V** (common anode) ⚠️ needs inverted logic (see Troubleshooting)

### 4) Ultrasonic sensor (HC-SR04P recommended)
- VCC → 5V (VBUS) **if your sensor needs it** (HC-SR04P often supports 3.3–5V; check your module)
- GND → GND
- TRIG → GP10
- ECHO → GP11  
  ⚠️ Some ultrasonic sensors output a 5V ECHO signal. If yours does, you must level-shift or use a sensor designed for 3.3V logic.

### 5) Speaker / buzzer
- GP20 → speaker/buzzer (+) and (-) to GND (or follow your module’s markings)

---

## Distance thresholds

These two values control when the lights/sounds change (in **centimeters**):

```python
CLOSE_CM = 20.0
MEDIUM_CM = 40.0
```

That creates three zones:

- **Close:** `< 20 cm`  → red + fast beeps
- **Medium:** `20–40 cm` → yellow + occasional beeps
- **Far:** `>= 40 cm` → green + silent

Want it more sensitive? Increase the numbers.  
Want it less sensitive? Decrease the numbers.

---

## How the code is structured

### Objects created (hardware)

```python
status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
rgb = RGBLED(red=RGB_RED_PIN, green=RGB_GREEN_PIN, blue=RGB_BLUE_PIN)
sensor = DistanceSensor(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)
```

### Mode toggle logic (button)
The program does **edge detection**: it only toggles *once* per press.

- `prev_pressed` remembers the previous state
- When it changes **not pressed → pressed**, the mode flips

```python
if (not prev_pressed) and pressed_now:
    mode = "active" if mode == "idle" else "idle"
```

### Reading distance
`picozero.DistanceSensor.distance` returns **meters**, so the code converts to centimeters:

```python
d_m = sensor.distance
d_cm = d_m * 100
```

### Lights
- If **IDLE**: lights off
- If **ACTIVE**:
  - status LED on
  - RGB color based on the distance zone

### Sound
- If **IDLE**: speaker off
- **Far**: silent
- **Medium**: beep every 5 loops
- **Close**: beep every loop

The loop runs about every `0.1s`, so:
- Medium beeps about every `0.5s`
- Close beeps about `10 times/sec` (fast)

---

## Where to customize (easy changes)

### Change the update speed
At the bottom of the loop:

```python
sleep(0.1)
```

- Smaller = more responsive (but more prints + more sensor reads)
- Bigger = calmer + less spam

### Change beep pattern
In `update_sound(distance_cm, loop_count)`:

- Medium zone uses `loop_count % 5 == 0`
- Close zone beeps every loop

You can change the beep timing:

```python
speaker.beep(on_time=0.05, off_time=0.05, n=1)
```

Try `on_time=0.1` for longer beeps, or increase `off_time` for slower beeps.

### Change the colors
In `update_lights(distance_cm)` the RGB values are:

- Red: `(1.0, 0.0, 0.0)`
- Yellow: `(1.0, 1.0, 0.0)`
- Green: `(0.0, 1.0, 0.0)`

You can make a “blue far” mode, for example:
- Far: `(0.0, 0.0, 1.0)`

---

## Troubleshooting

### “Button does nothing”
- Confirm the button really connects **GP13 to GND** when pressed.
- Try printing `button.is_pressed` in a tiny test file.

### “RGB colors are backwards / always on”
- Your RGB LED may be **common anode** (common leg to 3.3V).
- In that case, you’ll need inverted values (1 becomes 0, 0 becomes 1), or rewire to a common-cathode RGB LED.

### “Distance is stuck at 0 or random”
- Double-check TRIG/ECHO pins (GP10 and GP11).
- Confirm your ultrasonic module is compatible with 3.3V logic on ECHO.
- Move your hand slowly 10–50 cm in front of the sensor and watch the serial output.

### “The speaker won’t beep”
- Some buzzers are **active** (beep with just HIGH/LOW), others are **passive** (need PWM/tone).
- If yours is passive and very quiet, try a different buzzer module or check polarity.

---

## Expected serial output (example)

When ACTIVE:

```
Pico Smart Distance Station starting...
Press the button to toggle between IDLE and ACTIVE.
Move your hand in front of the sensor to test.
Mode changed to: active
Distance: 52.3 cm
Distance: 41.8 cm
Distance: 35.7 cm
Distance: 18.9 cm
```

---

## File reference

- Code: `03_distance_station.py`
