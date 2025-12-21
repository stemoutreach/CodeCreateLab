

# 03 — Pico Smart Distance Station

> ### Quick Summary  
> **Level:** 03 • **Time:** 60–90 min  
> **Prereqs:**  
> - [Guide: 00 — Python Basics](../Guides/00-python-basics-guide.md)  
> - [Guide: 01 — Python Functions](../Guides/01-python-functions-guide.md)  
> - [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding-guide.md)  
> - *(Optional)* WiFi setup + web app basics (for the Live Dashboard upgrade)
> **Hardware:**  
> - Raspberry Pi Pico + micro-USB cable  
> - Breadboard + jumper wires  
> - 1 × single-color LED  
> - 2 × pushbutton  
> - 1 × RGB LED
> - *(Optional)* 0.96" SSD1306 OLED (I2C)  
> - 1 × Ultrasonic sensor (HC-SR04 or 3.3V-safe variant)  
> - 1 × passive piezo speaker/buzzer  
> **You’ll practice:** GPIO input/output, distance sensing, mapping sensor values to colors/sounds, simple state machine loops  
>
> **Learn → Try → Do:** You *Learned* each part (LED, button, RGB, ultrasonic, speaker) in the Guide and *Tried* tiny examples. In this Lab you’ll **Do** a full project that combines them into one smart station.

# Why This Matters

Real projects combine **multiple inputs and outputs**: a sensor, a couple of lights, and sound. In this lab you’ll turn the Pico into a **smart distance station** that *sees* how close something is and responds with light and sound. This is the same idea used in parking sensors, robot bump warnings, and “too close” alerts on machines.

---

# What You’ll Build

You’ll build a **Pico Smart Distance Station**:

- The **ultrasonic sensor** measures how far away an object is.  
- A normal **LED** shows when the system is “armed” and measuring.  
- An **RGB LED** acts like a traffic light:
  - Green = far, Yellow = medium, Red = too close.  
- A **speaker** beeps faster as things get too close.  
- A **pushbutton** toggles between “idle” and “active” scanning (and can also be used to silence the alarm).

In the end, moving your hand closer will change colors and beeps in real time.

---

# Outcomes

By the end you can:

- Wire and use **five** different I/O parts together on one breadboard.  
- Read distance from an ultrasonic sensor and convert it to **cm**.  
- Map distance ranges to **RGB colors**, a **status LED**, and **speaker beeps**.  
- Structure a simple **state machine** (idle vs active) driven by a pushbutton.  

---

# Setup

- **Environment:** Classroom default is **Raspberry Pi 500** (Raspberry Pi OS) + **Thonny IDE**.  
- **Interpreter:** In Thonny, set **Tools → Options → Interpreter → MicroPython (Raspberry Pi Pico)**.  
- **Connect Pico:** Plug in the Pico with a micro-USB cable.  
- **Project folder:** Save your work in `~/Documents/CodeCreate/` (or your class folder).  
- **Run steps:**
  1. Open Thonny.  
  2. **File → New**, paste your starter code, then **File → Save As…**.  
  3. Save to **This computer** *or* directly to **Raspberry Pi Pico**.  
  4. Click **Run ▶** and watch the Thonny Shell for prints.  
  5. For auto-run, save the final version on the Pico as **`main.py`**.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open  
> **[STUDENT_START.md](../Example_Code/03-pico-breadboard/STUDENT_START.md)**.

## 1) Plan (2–3 min)

Before wiring anything, sketch your idea:

- Draw a tiny diagram (stick figure is fine) showing:
  - **Ultrasonic sensor** in front.  
  - **RGB LED** and **single LED** on your “control panel.”  
  - **Speaker** near the edge.  
  - **Pushbutton** somewhere easy to press.  
- Decide on distance ranges (you can adjust later), for example:
  - Far: > 40 cm → RGB = green, no beep.  
  - Medium: 20–40 cm → RGB = yellow, slow beep.  
  - Close: < 20 cm → RGB = red, fast beep.  
- Decide what the **pushbutton** does:
  - Option A: Toggle between *IDLE* (off) and *ACTIVE* (measuring).  
  - Option B: *Mute / unmute* the speaker while still showing colors.

Write your ranges and button behavior as a short list in comments or on paper.

## 2) Standard pin map used in this guide

Use this **standard map** so the Lab and Guide match:

```python
# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN  = 13        # main pushbutton
LED_PIN     = 14        # external LED
RGB_R_PIN   = 17
RGB_G_PIN   = 18
RGB_B_PIN   = 19
SPEAKER_PIN = 20        # passive buzzer / speaker

# OLED Display (0.96" I2C 128x64, SSD1306)
OLED_SDA_PIN = 0        # I2C0 SDA
OLED_SCL_PIN = 1        # I2C0 SCL
```

You can copy this at the top of your program and use the names instead of raw pin numbers.

---

Double-check:

- All grounds (Pico GND, sensor GND, LED GND, speaker GND) are connected.  
- Only **one wire per hole** on the breadboard.  

## 3) Code (8–12 min)

You’ll write code to:

- Read distance in **centimeters**.  
- Show system status with the **single LED** (on = active).  
- Map distance ranges to **RGB colors**.  
- Beep faster as objects get closer.  
- Use the **button** to toggle between states (or mute).

Start from the **Skeleton Starter** at the bottom of this lab:

- Fill in the **TODOs** for:
  - Setting RGB color based on distance.  
  - Choosing beep patterns for each distance range.  
  - Handling button presses to switch modes.  
- Keep each job in its own function:
  - `read_distance_cm()` (already started).  
  - `update_lights(distance_cm)` for both LEDs.  
  - `update_sound(distance_cm)` for the speaker.  
  - `handle_button()` to toggle a simple state variable like `"idle"` / `"active"`.

**Tips:**

- Use prints in the Shell: `print(distance_cm)` to see values.  
- Avoid blocking the loop with very long `sleep()` calls; lots of tiny sleeps are better.  
- Re-use patterns from the Guide instead of starting from scratch.

## 4) Discovery (checklist + pseudocode) (8–12 min)

**Checklist**

Make sure you can say “yes” to each:

- [ ] The status LED clearly shows when the station is *active* vs *idle*.  
- [ ] The RGB LED shows at least **three** different colors for three distance ranges.  
- [ ] The speaker makes **different beep patterns** (or silence) for each range.  
- [ ] The button can **change the mode** (e.g., idle/active or mute/unmute).  
- [ ] Your main loop reads distance regularly (not once) and updates lights/sounds.  

**Pseudocode (guide, not code)**

```text
start in IDLE mode
turn status LED off
maybe show a "ready" color on the RGB LED

loop forever:
    read the pushbutton:
        if button was just pressed:
            if mode is IDLE:
                switch to ACTIVE
            else:
                switch back to IDLE

    if mode is ACTIVE:
        measure distance in cm from ultrasonic
        show distance in the Shell for debugging
        choose a distance band:
            if distance is "too close":
                set RGB to red
                make very fast beeps
            else if distance is "medium":
                set RGB to yellow
                make slow beeps
            else:
                set RGB to green
                be silent
        turn status LED on
    else:
        turn status LED off
        set RGB to a neutral color (e.g., off or blue)
        make sure speaker is off

    short sleep (e.g. 0.1 s) to avoid spamming the sensor
```

Use this pseudocode as a **map**, but write the actual Python yourself.

## 5) Test (3–5 min)

Test one feature at a time:

1. **Distance only**: Comment out the sound code and just print distance.  
2. **RGB mapping**: Move your hand from far → close and check the colors change where you expect.  
3. **Sound patterns**: Temporarily print what pattern you’re using:  
   - `"beep: fast"` vs `"beep: slow"` vs `"silent"`.  
4. **Button behavior**: Press the button:
   - Does the mode flip every press (not many times per press)?  
   - Does the status LED match the current mode?  

If something fails, add `print()` statements to see what your variables are doing.

## 6) Iterate (2–3 min)

Pick **one** improvement:

- Adjust distance thresholds to match real behavior in your classroom.  
- Change colors (e.g., use cyan/purple instead of pure green/blue).  
- Make sound patterns less annoying (or more dramatic).  
- Smooth the distance readings (ignore obviously “glitchy” values).

Update your code, re-test, and stop when it feels like a polished mini-project.

---

# Optional Upgrade — Live WiFi Dashboard + OLED + RGB

> You said you already learned WiFi setup + a simple web app.  
> This upgrade uses that skill to make your Distance Station **interactive**.

## What you’ll build

When you open the Pico’s IP address in a browser, you’ll get a live dashboard:

- **Distance** updates live (no manual refresh)
- A **Toggle Capture** button turns measuring **ON/OFF**
- The Pico’s **GPIO 13 button** also toggles capture
- The **RGB LED color** is controlled by distance (Part A thresholds)
- The **OLED 4th line** shows `Distance=...` (or `Distance=PAUSED`)

## Part A distance colors (same thresholds)

These match the Part A ranges:

- **RED:** distance **< 20 cm**
- **YELLOW:** distance **20–40 cm**
- **GREEN:** distance **> 40 cm**

> If your RGB looks “backwards,” you may have a **common-anode** RGB LED.

## Files you need on the Pico

*(Optional)* If your repo includes reference pages, see:
- `03-web-dashboard-reference.md`
- `03-oled-status-reference.md`


Copy these files to your Pico project:

- `wifi_config.py` — your SSID + password (**do not commit to GitHub**)
- `wifi.py` — `connect_wifi()` connects and returns the Pico’s IP
- `oled_status.py` — shows IP + `Distance=...` on the OLED
- `web_dashboard.py` — serves the dashboard + controls Capture + updates RGB/OLED
- `main.py` — glue file that connects WiFi then starts the dashboard

## How to run it

1. **Update `wifi_config.py`** with your WiFi name and password.
2. Run `main.py`.
3. Look at the OLED:
   - Top lines show the IP address
   - Bottom line starts as `Distance=PAUSED`
4. On a laptop/phone on the same WiFi, open:
   - `http://<PICO_IP>/`
5. Click **Toggle Capture**:
   - Web distance starts updating
   - OLED switches to `Distance=12.3cm`
   - RGB shows RED/YELLOW/GREEN based on distance
6. Press the physical Pico button (GPIO 13) to toggle Capture too.

## What “Capture” means

- **Capture INACTIVE**
  - Ultrasonic sensor is **not read**
  - RGB is **OFF**
  - OLED shows `Distance=PAUSED`
  - Web shows `Distance: PAUSED`

- **Capture ACTIVE**
  - Ultrasonic sensor is read on a steady interval
  - RGB updates to match distance
  - OLED shows live distance

## Troubleshooting

- **OLED stays on `Distance=PAUSED` even when Capture is ACTIVE**
  - Make sure your `oled_status.py` includes the `show_distance()` function.
- **Web page loads but distance never changes**
  - Make sure you are opening the Pico’s IP (the OLED shows it).
  - The dashboard uses polling, so it should update automatically.
- **RGB colors don’t match**
  - Re-check RGB pins (R=17, G=18, B=19).
  - If using a common-anode RGB LED, set `RGB_COMMON_ANODE = True` in `web_dashboard.py`.


---

# Skeleton Starter (start here)

> Use this as your base file. **Do not** remove the TODOs until you’ve implemented them.

```python
from picozero import LED, Button, RGBLED, DistanceSensor, Speaker
from time import sleep

# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN  = 13        # main pushbutton
BUTTON2_PIN = 15        # second button (reaction game)
LED_PIN     = 14        # external LED
RGB_R_PIN   = 17
RGB_G_PIN   = 18
RGB_B_PIN   = 19
SPEAKER_PIN = 20        # passive buzzer / speaker

# OLED Display (0.96" I2C 128x64, SSD1306)
OLED_SDA_PIN = 0        # I2C0 SDA
OLED_SCL_PIN = 1        # I2C0 SCL

# --- Objects ---
status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
rgb = RGBLED(red=RGB_RED_PIN, green=RGB_GREEN_PIN, blue=RGB_BLUE_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)

# Simple mode variable: "idle" or "active"
mode = "idle"


def read_distance_cm():
    """Return the distance in centimeters (float)."""
    d_m = sensor.distance        # distance in meters
    d_cm = d_m * 100
    return d_cm


def update_lights(distance_cm):
    """
    TODO: Set status_led and rgb color based on:
      - mode (idle vs active)
      - distance_cm (far / medium / close)
    Example idea (you can change thresholds/colors):
      - idle: status off, RGB off
      - far:  status on, RGB green
      - medium: status on, RGB yellow
      - close: status on, RGB red
    """
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
    """
    TODO: Decide when/how the speaker should beep.
    Ideas:
      - idle: speaker.off()
      - far:  silent
      - medium: short beep once in a while
      - close: faster beeps
    Keep this function quick so the main loop stays responsive.
    """
    global mode

    if mode == "idle":
        speaker.off()
        return

    # TODO: pick a pattern based on distance_cm.
    # Hint: very short play() calls + no long sleeps here.
    # You can also choose to call speaker.off() when "far".


def handle_button():
    """
    TODO: Flip mode when the button is pressed.
    Use Button.is_pressed or when_pressed/when_released callbacks.
    Simple approach:
      - check if button.is_pressed and it wasn't pressed last loop
      - then toggle mode between "idle" and "active"
    """
    global mode

    # TODO: store previous button state (e.g., in a global variable)
    # and only toggle when the state changes from not-pressed to pressed.
    # Example pattern (not full code):
    # if button_was_released and button.is_pressed:
    #     mode = "active" if mode == "idle" else "idle"
    pass


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

# Submission / Demo Checklist

- [ ] Status LED clearly shows **idle vs active** mode.  
- [ ] RGB LED shows **at least three** distinct colors for different distance ranges.  
- [ ] Speaker produces **different beep patterns** (or silence) for different ranges.  
- [ ] Button reliably toggles between modes (or mute/unmute) without glitching.  
- [ ] Program exits cleanly (LEDs off, speaker off) when stopped.  
- [ ] Code is organized into functions (no giant 100-line `while True`).

---

# Extensions (choose one)

- **Extension A — Danger zone:** Add a “danger” behavior when distance is *very* small (e.g., < 10 cm): flash RGB quickly and play an alarm pattern.  
- **Extension B — Distance bargraph:** Use RGB brightness as a “bar” for distance (very bright when close, dim when far).  
- **Extension C — Silent mode:** Add a second button press sequence that cycles through `active`, `active but muted`, and `idle`. Show the current mode with different colors.

---

# Troubleshooting

- **RGB LED never lights:**  
  - Check the **common pin**: is it really on GND (common cathode) or 3V3 (common anode)?  
  - Try a simple test in the Shell: `rgb.color = (1, 0, 0)`.

- **Distance readings are random or zero:**  
  - Double-check that **TRIG** and **ECHO** pins match your code.  
  - Make sure **GND is shared** between Pico and sensor.  
  - Confirm your module is **3.3V-safe** or that you used the recommended level shifting.  
  - Slow down: use a longer sleep (e.g. `sleep(0.2)`) between readings.

- **Speaker only makes one constant tone or is silent:**  
  - If every sound is the same no matter what, you might have an **active buzzer**—use simple `.beep()` patterns instead of `Speaker` notes.  
  - Check polarity (`+` to GPIO, `-` to GND).  
  - Try a tiny test: `speaker.play(440, 0.5)` in the Shell.

- **Button toggles many times per press:**  
  - You are probably checking `button.is_pressed` without tracking changes.  
  - Add a “previous state” variable and only toggle when it changes from not-pressed to pressed.  
  - Add a very short delay (`sleep(0.05)`) in your loop to help.

---

# Reflection (1–2 sentences)

- When did combining five different parts feel confusing, and how did you break the problem into smaller pieces?  
- If you had another hour, what is the **next feature** you would add to your Smart Distance Station?

---

# Next Up

Ready for Wifi setup Guide? Develop an app interface and connect to smart station through a web interface in **[04 — Pico Wifi_Smart Station App](../Guides/04-pico-wifi-breadboard-app.md)**.

