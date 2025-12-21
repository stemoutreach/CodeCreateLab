# 03 — web_dashboard.py Reference

> ### Quick Summary  
> **Level:** 03 • **Time:** 15–25 min  
> **Prereqs:** Pico 2 W connected to WiFi (IP shown on OLED or in Thonny)  
> **Hardware:** HC-SR04P (3.3V), RGB LED, **buzzer (PWM)**, optional SSD1306 OLED, button  
> **You’ll practice:** simple web server, JSON endpoint, polling, state toggles, debouncing, **non-blocking buzzer control**

# What This File Does
`web_dashboard.py` runs a tiny web server on the Pico and provides:

- `/` — a dashboard web page (HTML + JavaScript)
- `/data` — live JSON data (distance, button state, capture state, RGB info)
- `/capture/toggle` — flips **Capture** between ACTIVE and INACTIVE

The web page **polls** `/data` on a timer (every ~500 ms by default), so the readings update live without you refreshing the page.

# The Big Idea: “Capture” Controls Everything
This program has one shared on/off state called **Capture** (`sensor_active`).

## Capture INACTIVE
- Ultrasonic sensor is **not read**
- RGB LED is **OFF**
- OLED shows `Distance=PAUSED` (if OLED installed)
- **Buzzer is OFF**

## Capture ACTIVE
- Ultrasonic sensor is read on a steady interval
- RGB LED color updates based on distance
- OLED shows `Distance=12.3cm` (example)
- **Buzzer beeps** based on how close an object is

You can toggle Capture from:
- The **web** button (**Toggle Capture**) → calls `/capture/toggle`
- The **physical button** on the Pico → debounced toggle in the main loop

# Pin Map Used in This File
These constants are at the top of the code so you can match them to your breadboard wiring:

```python
STATUS_LED_PIN = 14     # optional external LED
BUTTON_PIN     = 13     # physical toggle button
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11
RGB_R_PIN      = 17
RGB_G_PIN      = 18
RGB_B_PIN      = 19
SPEAKER_PIN    = 20     # buzzer/speaker (PWM)
```

## Button wiring and `pull_up=True`
The line below is important:

```python
button = Button(BUTTON_PIN, pull_up=True)
```

This expects a **“button to GND”** wiring style:

- One leg of the button → **GPIO 13**
- Other leg of the button → **GND**

When the button is *not pressed*, the internal pull-up holds the pin at logic **1**.  
When pressed, the pin is connected to **GND** and becomes logic **0**.

If your button is wired to **3V3** instead, you would use `pull_up=False` (but in this lab we use the safer “to GND” style).

# RGB Distance Colors (Part A Thresholds)
These match the Part A ranges from the distance station:

- **RED:** distance **< 20 cm**
- **YELLOW:** distance **20–40 cm**
- **GREEN:** distance **> 40 cm**
- **BLUE:** sensor read error (distance is `None`) while Capture is ACTIVE

The thresholds are controlled by:

```python
CLOSE_CM = 20.0
MEDIUM_MAX_CM = 40.0
```

## Common-anode RGB LEDs
Some RGB LEDs are **common-anode**, which makes colors look “inverted”.
If your colors are wrong, flip this setting:

```python
RGB_COMMON_ANODE = True
```

# Buzzer Beeps (How It Works)
The buzzer uses **PWM** (Pulse Width Modulation):

```python
_buzzer_pwm = PWM(Pin(SPEAKER_PIN))
_buzzer_pwm.freq(BUZZER_FREQ_HZ)
_buzzer_pwm.duty_u16(0)  # OFF
```

Why PWM?
- A buzzer needs a fast square wave to make a tone (for example, 2000 Hz).
- PWM generates that wave for you.

## Beep rules (distance in cm)
- **< 20 cm** → fast beeps  
- **20–40 cm** → slow beeps  
- **> 40 cm / no read** → silent

## Non-blocking (super important)
Beginners often write beeps like this:

```python
# DON'T DO THIS in a web server loop
buzzer.on()
sleep(0.1)
buzzer.off()
sleep(0.2)
```

That blocks the Pico from:
- reading the sensor
- handling web requests
- updating the page

This program uses a **non-blocking scheduler**:
- `_buzzer_tick()` is called every loop
- It checks time using `utime.ticks_ms()`
- It turns the buzzer on/off at the right moments **without `sleep()`**

The key idea is:  
**“Check the clock, do tiny work, then keep looping.”**

## Beep settings you can tune
At the top of the file:

```python
BUZZER_FREQ_HZ = 2000
BUZZER_DUTY_U16 = 20000

BEEP_FAST_PERIOD_MS = 250
BEEP_FAST_ON_MS     = 60

BEEP_SLOW_PERIOD_MS = 800
BEEP_SLOW_ON_MS     = 50
```

- Increase `BUZZER_DUTY_U16` to be louder (up to ~65535)
- Change `BUZZER_FREQ_HZ` to change pitch
- Period = how often a beep starts
- On-time = how long each beep stays on

# How the Main Loop Works
Inside `run_server(ip)` there is one `while True:` loop that does four jobs:

1. **Check the physical button** and toggle Capture (with debounce)
2. **Update distance/RGB/OLED** on a fixed interval (`_SENSOR_UPDATE_MS`)
3. **Run buzzer scheduler** (`_buzzer_tick(...)`) every loop
4. **Handle one web request** if a browser connects

That ordering matters: even if no one is on the web page, the sensor/buzzer logic still runs.

# Web Endpoints (What the Browser Calls)

## GET `/`
Returns the HTML page (with JavaScript polling).

## GET `/data`
Returns a JSON payload like:

```json
{
  "distance_cm": 27.4,
  "sensor_active": true,
  "button_pressed": false,
  "led_on": true,
  "rgb_name": "YELLOW",
  "rgb_255": [255, 255, 0],
  "ms": 1234567
}
```

## GET `/capture/toggle`
Flips Capture ON/OFF and returns:

```json
{ "sensor_active": true }
```

# Timing Controls (Two Different “Rates”)
There are two update rates and they do different jobs:

## Pico sensor update rate
How often the Pico reads the sensor and updates RGB/OLED:

```python
_SENSOR_UPDATE_MS = 500
```

## Browser polling rate
How often the web page requests `/data`:

- Controlled by the `poll_ms` argument in the HTML.
- Default is **500 ms**.

**Tip:** If the page feels “laggy”, reduce `poll_ms`.  
If the Pico feels overloaded, increase `poll_ms` and/or `_SENSOR_UPDATE_MS`.

# Troubleshooting

## Web loads, but the physical button doesn’t toggle
- Confirm your button is on **GPIO 13** and wired to **GND**
- Make sure the file uses:
  - `BUTTON_PIN = 13`
  - `Button(BUTTON_PIN, pull_up=True)`

## Web loads, but distance never changes
- Make sure Capture is **ACTIVE**
- Check ultrasonic wiring:
  - TRIG → GPIO 10
  - ECHO → GPIO 11
  - VCC → 3.3V (HC-SR04P version)
  - GND → GND

## Buzzer is silent
- Confirm buzzer wire is on **GPIO 20**
- Check ground connection
- Increase `BUZZER_DUTY_U16` a little

## RGB colors look wrong
- Double-check pins (R=17, G=18, B=19)
- Try `RGB_COMMON_ANODE = True`
