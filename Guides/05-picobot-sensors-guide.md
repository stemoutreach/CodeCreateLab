# 05 — PicoBot Sensors: Start Button, Distance, Lights & Sound

> ### Quick Summary  
> **Level:** 05 • **Time:** 60–90 min  
> **Prereqs:**  
> - [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> - [Guide: 04 — PicoBot (Drive with L298N)](../Guides/04-picobot.md)  
> **Hardware:** PicoBot (Pico + L298N + 2 motors + battery), button, RGB LED, HC-SR04P, speaker  
> **You’ll practice:** planning behavior, wiring multiple I/O on a robot, using `picozero` with drive code, reading distance, mapping distance to color/sound, building a simple robot state machine  

---

# Why This Matters

You already made the Pico **blink LEDs, read buttons, beep, and measure distance** on a breadboard, and you made your PicoBot **drive on purpose** with the L298N. Now you’ll bolt those skills together: a **start button** to begin the mission, an **ultrasonic sensor** to watch for obstacles, an **RGB LED** to show distance bands, and a **speaker** to warn when things get too close. This “sensors + behavior” pattern is the backbone of obstacle-avoid robots, parking sensors, and safety alerts.

---

## What you’ll learn

- Choose a clear behavior and map it to **robot states** (idle, driving, backing up).
- Plan a **pin map** that works with your existing L298N wiring.
- Safely wire an **HC-SR04P** ultrasonic sensor to the Pico’s 3.3 V system.
- Use `picozero` to read distance and drive an **RGB LED** + **speaker**.
- Add a **start button** that controls when your robot is allowed to move.
- Build a simple **state machine loop** that ties sensors to motion.
- Debug common sensor issues (0 cm readings, random jumps, no beeps).

---

## Setup

_Classroom default: **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**._

- In Thonny:  
  - `Tools → Options → Interpreter` → **MicroPython (Raspberry Pi Pico)**.  
  - Connect your Pico over USB.
- Re-use your **PicoBot drive file** from the L298N guide (for example `picobot_drive.py`) that already has `forward()`, `back()`, and `stop()` functions.  
- Create a new file for this guide, for example:  
  `~/Documents/CodeCreate/picobot_sensors_demo.py`
- You’ll *either*:
  - import your drive helpers:  
    `from picobot_drive import forward, back, stop, set_speed`  
  - or copy just the functions you need into this new file.

---

## Materials

- **PicoBot chassis**  
  - Raspberry Pi Pico  
  - L298N motor driver (already wired to motors + battery)  
  - 2× DC gear motors + wheels  
- **Inputs/Outputs to add to the robot**
  - 1 × **tactile pushbutton** (start button)
  - 1 × **RGB LED**, common cathode preferred (one common GND pin)  
  - 1 × **Ultrasonic distance sensor — HC-SR04P (3.3 V-safe)**  
  - 1 × **passive piezo speaker** (or buzzer)  
  - Assorted **jumper wires** and **breadboard** or mounting board  
- **Power / safety**
  - Pico powered via USB *or* VSYS from motor battery (as in your PicoBot build)  
  - Shared **GND** between Pico, L298N, sensor, RGB LED, and speaker  

> ⚠ **Voltage safety**  
> - Use the **HC-SR04P** (3.3–5 V) and power it from **Pico 3V3(OUT)**, not 5 V.  
> - All GPIO are **3.3 V logic only**. Never feed 5 V into a GPIO pin.  

---

## Walkthrough — Step by Step (with explanations)

### 1) Plan the behavior & pin map

**Idea:** Decide what your robot *should do* before wiring. That keeps your code clean and avoids random spaghetti.

We’ll use three **states**:

- `"idle"` – Motors off. RGB LED shows “ready” color, speaker silent.  
- `"drive"` – Robot drives forward. RGB color shows distance band.  
- `"backup"` – Robot backs up and beeps, then returns to `"idle"`.

**Behavior sketch**

- On power-up → `"idle"` (wheels off, RGB blue).  
- When **start button** is pressed in `"idle"` → switch to `"drive"`.  
- In `"drive"`:
  - Read distance (cm) from ultrasonic.  
  - If `distance_cm < CLOSE_CM` → switch to `"backup"`.  
- In `"backup"`:
  - Back up for a short time with beeps.  
  - Return to `"idle"` and wait for another button press.

**Pin map (suggested)**

We’ll leave your L298N pins exactly as they were in the drive guide and add new pins around them.  

- **Already used by L298N (from 04 guide, do not change):**  
  - GP10 → IN1 (Left)  
  - GP11 → IN2 (Left)  
  - GP12 → IN3 (Right)  
  - GP13 → IN4 (Right)  
  - GP14 → ENA (PWM)  
  - GP15 → ENB (PWM)

- **New for this guide (sensors + feedback):**
  - **Button** → GP16  
  - **RGB LED (common cathode)**  
    - Red → GP17  
    - Green → GP18  
    - Blue → GP19  
    - Common cathode → GND  
  - **Ultrasonic (HC-SR04P)**  
    - VCC → Pico **3V3(OUT)**  
    - GND → Pico **GND**  
    - TRIG → GP3  
    - ECHO → GP2  
  - **Speaker** → GP20 (+) and GND (–)

> 💡 If you must use different pins, it’s fine—just update the numbers in your code and keep the *patterns*.

---

### 2) Wire & test the start button and RGB LED

**Idea:** Get your “control panel” working on the robot: a button to start/stop and an RGB LED to show state.

#### Wiring (button + RGB)

- Button: one leg → GP16, opposite leg → GND.  
- RGB LED:  
  - Longest leg (common cathode) → GND.  
  - R, G, B legs → GP17, GP18, GP19 (order may need trying).

#### Code: quick “panel” test

```python
from picozero import Button, RGBLED
from time import sleep

button = Button(16)
rgb = RGBLED(red=17, green=18, blue=19)

mode = "idle"

def show_mode():
    if mode == "idle":
        rgb.color = (0, 0, 1)      # blue (waiting)
    elif mode == "drive":
        rgb.color = (0, 1, 0)      # green (driving)
    elif mode == "backup":
        rgb.color = (1, 0.5, 0)    # orange (backing up)

show_mode()

while True:
    if button.is_pressed and mode == "idle":
        mode = "drive"
        show_mode()
        sleep(0.2)   # tiny debounce

    elif button.is_pressed and mode == "drive":
        mode = "idle"
        show_mode()
        sleep(0.2)

    # (Later you’ll also change mode based on distance.)
    sleep(0.05)
```

**Anatomy / breaking it down**

- `Button(16)` uses an internal pull-up; wiring to GND means “pressed = 0”.  
- `RGBLED` expects values from `0.0` to `1.0` for `(r, g, b)`.  
- `show_mode()` is a helper: you can change colors later in **one place**.

**Notes & pitfalls**

- If the button does nothing:
  - Make sure legs are across the **breadboard gap**, not on the same side.
  - Confirm one leg is truly on **GND**, the other on **GP16**.
- If RGB colors look “weird”:
  - You might have red/green/blue legs in a different order—swap wires until red/green/blue are correct.
- RGB always off? Ensure you’re using a **common cathode** LED or set `active_high=False` for a common anode.

---

### 3) Add ultrasonic distance and speaker beeps

**Idea:** Your robot needs “eyes” (distance sensor) and a “voice” (speaker) to warn about obstacles.

We’ll reuse the HC-SR04P pattern from the breadboarding guide and Smart Distance Station lab.  

#### Wiring (HC-SR04P + speaker)

- HC-SR04P:  
  - VCC → **3V3(OUT)** (not 5 V).  
  - GND → Pico GND.  
  - TRIG → GP3.  
  - ECHO → GP2.  
- Speaker (passive piezo recommended):  
  - `+` → GP20.  
  - `–` → GND.

> ⚠ Double-check that your module is **HC-SR04P** (3.3–5 V).  
> If it’s the older 5 V HC-SR04, talk to your teacher about a safe level shifter before connecting ECHO to the Pico.

#### Code: test distance + beeps (no driving yet)

```python
from picozero import DistanceSensor, Speaker
from time import sleep

sensor = DistanceSensor(echo=2, trigger=3)  # meters
speaker = Speaker(20)

CLOSE_CM = 15
WARN_CM = 30

while True:
    d_m = sensor.distance
    d_cm = d_m * 100
    print(f"{d_cm:.1f} cm")

    if d_cm < CLOSE_CM:
        # very close: short “alarm” beep
        speaker.play(880, 0.1)   # high tone
    elif d_cm < WARN_CM:
        # in warning range: slow soft beep
        speaker.play(440, 0.05)
        sleep(0.2)
    else:
        # far: stay silent
        speaker.off()

    sleep(0.1)
```

**Anatomy**

- `DistanceSensor.distance` returns meters; multiply by 100 for cm.  
- We defined two bands:
  - `< CLOSE_CM` → “danger”.  
  - `< WARN_CM` → “warning”.  
  - Otherwise: safe.

**Notes & pitfalls**

- Distance stuck around `0.0` or huge numbers:
  - Confirm **3V3(OUT)**, not 5 V.  
  - Check that ECHO/TRIG pins (`2` and `3`) match your wiring.  
  - Ensure the sensor points at something within ~2–300 cm.
- Speaker always one constant tone?
  - You might have an **active buzzer**; it ignores frequency changes. Use shorter `on()` / `off()` pulses instead of `Speaker.play()` or swap to a passive piezo.

---

### 4) Tie it together: states, distance bands, and drive helpers

**Idea:** Now glue everything together: button + distance + RGB + speaker + your existing drive code. We’ll build a simple **state machine loop** that decides what motors should do.

This snippet assumes you have these helpers defined in your drive file (from the L298N guide) or similar:

- `set_speed(percent)` – sets PWM speed for both motors.  
- `forward()` – sets both motors to forward (does not sleep).  
- `back()` – sets both motors to reverse.  
- `stop()` – stops both motors.

#### Code: basic obstacle-aware loop

```python
from time import sleep
from picozero import Button, RGBLED, DistanceSensor, Speaker

# --- from your drive code (import or copy) ---
from picobot_drive import forward, back, stop, set_speed

button = Button(16)
rgb = RGBLED(red=17, green=18, blue=19)
sensor = DistanceSensor(echo=2, trigger=3)
speaker = Speaker(20)

mode = "idle"
CLOSE_CM = 15
WARN_CM = 30

def rgb_for_distance(d_cm):
    """Pick color based on distance bands."""
    if d_cm < CLOSE_CM:
        return (1, 0, 0)      # red
    elif d_cm < WARN_CM:
        return (1, 1, 0)      # yellow
    else:
        return (0, 1, 0)      # green

def do_backup():
    """Backup behavior: beep + reverse briefly, then stop."""
    global mode
    print("Backing up...")
    set_speed(60)
    back()
    for _ in range(10):       # ~1 second total
        speaker.play(880, 0.05)
        sleep(0.05)
    stop()
    speaker.off()
    mode = "idle"

def handle_button():
    """Toggle idle/drive when the button is pressed."""
    global mode
    if button.is_pressed and mode == "idle":
        mode = "drive"
        sleep(0.2)  # debounce
    elif button.is_pressed and mode == "drive":
        mode = "idle"
        stop()
        sleep(0.2)

def main_loop():
    global mode
    set_speed(65)  # good starting speed

    while True:
        handle_button()

        if mode == "idle":
            rgb.color = (0, 0, 1)   # blue waiting
            speaker.off()
            stop()

        elif mode == "drive":
            d_cm = sensor.distance * 100
            print(f"{d_cm:.1f} cm")

            # update RGB based on distance
            rgb.color = rgb_for_distance(d_cm)

            if d_cm < CLOSE_CM:
                # too close → backup behavior
                do_backup()
                continue
            else:
                forward()

        sleep(0.05)

try:
    main_loop()
except KeyboardInterrupt:
    print("Stopping robot.")
finally:
    stop()
    rgb.off()
    speaker.off()
```

**Anatomy**

- `mode` holds “what the robot is doing right now.”  
- `handle_button()` toggles between `"idle"` and `"drive"` and uses a tiny `sleep(0.2)` as a simple debounce.  
- In `"drive"` mode:
  - We read distance, print it for debugging, and set `rgb.color`.  
  - If the robot is too close, we call `do_backup()`, which:
    - backs up while beeping, then  
    - sets `mode = "idle"`.  
- `try / finally` ensures motors and outputs are turned off when you stop the program.

**Notes & pitfalls**

- If the robot **won’t move**, check:
  - You actually imported the right names from `picobot_drive`.  
  - `set_speed()` is called before `forward()`/`back()`.  
  - Battery is charged and motor pack is switched on.
- If the robot **never reaches backup**:
  - Print `CLOSE_CM` and `d_cm` to see if your thresholds are realistic for your setup.  
  - Try `CLOSE_CM = 20` or `WARN_CM = 40` as a starting point.

---

### 5) Tune thresholds and polish the behavior

**Idea:** Small tweaks make your bot feel “smart” instead of twitchy.

Things to adjust:

- `CLOSE_CM` and `WARN_CM` – Fit your classroom:  
  - In a tight course, you might want `CLOSE_CM = 10` and `WARN_CM = 25`.  
- Back-up time in `do_backup()` – Longer if you want a bigger escape.  
- Colors – Maybe:
  - blue = idle,  
  - cyan = safe,  
  - yellow = warning,  
  - red = panic.  
- Speed – Too fast → sensor has less time to react. Try 50–70%.

Try one change at a time, test, and keep what works.

---

## Vocabulary

- **State** – A named mode your robot can be in (e.g., `"idle"`, `"drive"`, `"backup"`).  
- **State machine** – A pattern where the robot’s actions depend on its current state and inputs.  
- **Threshold** – A numeric cutoff (like `CLOSE_CM`) where behavior changes.  
- **Ultrasonic sensor** – A sensor that measures distance using sound pulses and echoes.  
- **3.3 V logic** – The safe voltage level for Pico GPIO pins.  
- **Common ground** – Connecting all GND pins together so devices share a reference.  
- **Debounce** – A small delay or logic that avoids counting one button press many times.  
- **Duty cycle** – Percentage of time a PWM signal is on (controls motor speed).  

---

## Check your understanding

1. **Why 3V3(OUT)?**  
   Why do we power the HC-SR04P from **3V3(OUT)** instead of 5 V on the PicoBot?

2. **Predict the RGB color:**  
   Using the `rgb_for_distance()` function above, what color will the RGB LED show for these distances (in cm)?  
   a) 45 cm  
   b) 25 cm  
   c) 8 cm  

3. **Button logic – predict the state:**  
   Imagine `mode` is `"idle"`. You press the button and *keep holding* it. What modes will you see as the loop runs through `handle_button()` a few times, and why?

4. **Bug fix – backup never stops:**  
   Suppose someone writes this inside `do_backup()`:

   ```python
   def do_backup():
       global mode
       set_speed(60)
       back()
       while True:
           speaker.play(880, 0.05)
           sleep(0.05)
       stop()
       speaker.off()
       mode = "idle"
   ```

   a) What is wrong with this code?  
   b) How would you fix it so the backup only runs for a short time and then returns to `"idle"`?

5. **Motor safety:**  
   Why do we still call `stop()` in a `finally:` block even though our code already stops the robot in `"idle"` state?

6. **Sensor reliability:**  
   Your robot sometimes backs up even though nothing is in front of it. List two possible reasons and one way to debug it.

---

## Try it: Mini-exercises

Pick a few of these to practice:

1. **Warning blink:**  
   In `"drive"` mode, if distance is in the **warning band** (`WARN_CM > d_cm >= CLOSE_CM`), make the RGB LED **blink** yellow briefly instead of staying solid.

2. **Soft stop:**  
   Add a `"soft_stop"` state: when close to an obstacle but not yet in emergency, slow the robot down instead of backing up right away. (Hint: reduce `set_speed()` for that band.)

3. **Start-button override:**  
   Change `handle_button()` so that **pressing the button during `"backup"`** immediately cancels the backup and returns to `"idle"`.

4. **Drive-time counter:**  
   Keep track of how many seconds the robot has been in `"drive"` mode during this run (print it every second in the Shell).

**Stretch goals**

- **Cycle modes:**  
  Instead of just `"idle"` and `"drive"`, use the button to cycle through `"idle" → "drive" → "drive_muted" → "idle"`. In `"drive_muted"`, keep RGB behaviors but silence the speaker.

- **Obstacle-course helper:**  
  Add a `"turn"` state: when too close, back up, then turn right for a moment before returning to `"drive"`. You now have a very basic obstacle-avoid robot.

---

## Troubleshooting

- **Error: `ImportError: no module named 'picobot_drive'`**  
  → Make sure `picobot_drive.py` is saved on the Pico or in the same folder on your Pi, and that you spelled the filename exactly the same.

- **Symptom: robot never reacts to obstacles (always “safe”).**  
  → Check that `echo=2` and `trigger=3` match your wiring. Confirm the sensor is labeled **HC-SR04P** and powered from **3V3(OUT)**. Print raw distance values and lower `CLOSE_CM`/`WARN_CM` to test.

- **Symptom: robot constantly backs up even in open space.**  
  → The sensor might be reading noise (e.g., reflections from the floor). Tilt it slightly, slow down the robot, or ignore obviously impossible values (like `d_cm < 2`).

- **Symptom: RGB LED never changes color when distance changes.**  
  → Check pin numbers for `RGBLED`, confirm the common leg is on **GND**, and print the `d_cm` values and chosen color in the Shell to see if your logic runs.

- **Symptom: button seems to toggle multiple times per press.**  
  → Add a small debounce delay (`sleep(0.1)`) inside `handle_button()` and only trigger on the transition from not-pressed to pressed (track a `last_pressed` flag).

- **Symptom: robot keeps moving after you stop the program.**  
  → Make sure you have the `try/except/finally` pattern and call `stop()`, `rgb.off()`, and `speaker.off()` in `finally:`.

---

## Next up

Turn this behavior into a full challenge: design and run a course where your robot must avoid obstacles using its new “eyes and voice”:

**[05 – PicoBot Obstacle Sensing](../Labs/05-picobot-obstacle-sensing.md)**
