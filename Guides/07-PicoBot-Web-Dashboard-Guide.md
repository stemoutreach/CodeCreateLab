# PicoBot Web Dashboard Guide (WiFi + Drive Controls + Live Status)

This guide explains how the PicoBot **web control** works using these files:

- `main_web.py` — connects WiFi, shows IP, starts the dashboard server fileciteturn1file3  
- `wifi.py` — reusable `connect_wifi()` helper fileciteturn1file1  
- `picobot_web_dashboard.py` — the HTTP server + web page + routes fileciteturn1file0  
- `picobot_lib.py` — motors, ultrasonic distance, OLED helpers fileciteturn1file2  

---

## What to get from this project

- A web page at: `http://<PicoBot-IP>/`
- Buttons to drive: **Forward / Back / Left / Right / Stop**
- A **Power slider** (0–100)
- Live status updates:
  - **state** (FORWARD/BACK/LEFT/RIGHT/STOPPED)
  - **distance_cm** from the ultrasonic sensor
  - **ip** and **speed**
- OLED mirrors the same core info (state + distance + IP)

---

# 1) Big picture: how it runs

### Step A — `main_web.py` is the launcher
`main_web.py` does three jobs fileciteturn1file3:

1. **Safe startup**
   - `bot.stop()` and `bot.set_speed(0)`
2. **Connect to WiFi**
   - `ip = connect_wifi(... status_cb=oled_status)`
3. **Start the dashboard server**
   - `dash.run_server(ip)`

If WiFi fails, it shows **NO WIFI** and loops forever so the robot doesn’t drive blindly.

---

### Step B — `wifi.py` connects using `wifi_config.py`
`connect_wifi()` optionally loads credentials from `wifi_config.py` fileciteturn1file1:

```python
from wifi_config import SSID, PASSWORD
```

It retries and supports a callback (`status_cb`) so you can display short messages on the OLED while connecting.

**Important rule:**  
✅ `wifi_config.py` is editable and should not be committed to GitHub.

---

### Step C — `picobot_web_dashboard.py` is the server + UI
This file contains:
- A tiny HTTP server (sockets)
- The HTML page
- Control endpoints:
  - `/move/<direction>`
  - `/speed?value=NN`
  - `/data` (JSON)

It also keeps “runtime state” in global variables:
- `_current_speed`
- `_current_state`
- `_last_distance_cm`
- `_ip_str`

fileciteturn1file0

---

# 2) The web server (MicroPython socket server)

## Listening on port 80
Inside `run_server(ip)`:

- Binds `0.0.0.0:80` so it accepts connections from any device on the network
- Uses a short socket timeout (`0.1`) so it can keep updating sensor + OLED even when nobody is connected

fileciteturn1file0

### Why the timeout matters
If `accept()` blocked forever, the robot would only update distance/OLED when someone clicks a button.

With timeout:
- Sensor and OLED refresh happen regularly
- Web clients can connect anytime

---

## Parsing the request
The server reads the first line of the request, then extracts the path:

```python
GET /move/forward HTTP/1.1
```

Helper functions:
- `_parse_path()` → returns `/move/forward`
- `_split_path_query()` → splits `/speed?value=70` into route + query string
- `_get_query_param()` → gets `value` from the query string

fileciteturn1file0

---

# 3) Routes (the “API”)

## A) Drive routes: `/move/<cmd>`
Examples:
- `/move/forward`
- `/move/back`
- `/move/left`
- `/move/right`
- `/move/stop`

These call `_set_motion()` which updates motors and `_current_state`.

fileciteturn1file0

### Motion is “non-blocking”
The drive functions in `picobot_lib.py` **do not sleep**. They just set motor direction + PWM. fileciteturn1file2

That’s why the robot keeps moving after you click **Forward** — it will keep moving until **Stop** is pressed.

---

## B) Speed route: `/speed?value=NN`
Example:
- `/speed?value=60`

The handler calls `_set_speed()`:
- clamps 0–100
- stores `_current_speed`
- if currently moving, it “re-applies” the direction at the new speed (smooth change)

fileciteturn1file0

---

## C) Data route: `/data`
Returns JSON like:

```json
{
  "ip": "192.168.1.42",
  "state": "FORWARD",
  "speed": 60,
  "distance_cm": 33.4,
  "ms": 1234567
}
```

The browser polls this route repeatedly for live updates. fileciteturn1file0

---

## D) Page route: `/`
Any other path returns the HTML page from `_page_html()`.

The HTML is generated as a Python f-string so it can embed the IP and default speed. fileciteturn1file0

---

# 4) The browser UI (HTML + JavaScript)

## Buttons call `/move/...`
When you click a button, JavaScript does:

```js
await fetch('/move/' + dir);
```

Then it calls `tick()` to refresh the live status. fileciteturn1file0

---

## Power slider calls `/speed?value=...`
The slider uses a small “debounce”:
- waits ~120 ms before sending the request
- prevents spamming the Pico with requests while you drag the slider

fileciteturn1file0

---

## Live polling (updates every POLL_MS)
This line makes the dashboard update continuously:

```js
setInterval(tick, 250);
```

So the page stays current even if you don’t click anything. fileciteturn1file0

---

# 5) OLED mirroring (same info as the dashboard)

The dashboard code regularly calls:

- `_maybe_update_sensor()` → reads ultrasonic distance
- `_oled_refresh()` → uses `bot.oled_show_status(dist=..., state=...)`

And it stores the IP once:

```python
bot.oled_set_ip(ip)
```

So the OLED shows:
- State
- Distance
- IP (or “offline”)

fileciteturn1file0 fileciteturn1file2

---

# 6) Safety behavior 

### On boot
`main_web.py` ensures motors are stopped and speed is 0. fileciteturn1file3

### On “Stop”
The dashboard uses:

```python
bot.stop(brake=False)
```

That’s a **coast stop** (gentler). If you want a faster stop, use `brake=True`. fileciteturn1file2

### On “no echo” (distance read fails)
The dashboard doesn’t force-stop on `None`, it just displays it.  
If you want safety-first behavior, you can add:

- If `_last_distance_cm is None`: stop the robot
- Or if distance < X: auto-stop

(See improvement ideas below.)

---

# 7) Improvement ideas 

## Level 1 (easy)
### A) Add a “Brake Stop” button
- New route: `/move/brake`
- Call: `bot.stop(brake=True)`
- Label: “Emergency Stop”

### B) Add a “Horn / Beep” button
If your PicoBot has a buzzer, create `/beep` and call `bot.beep()` (you’d add beep code to `picobot_lib.py`).

### C) Show “signal quality” or WiFi info
In `wifi.py`, you can expose RSSI (if available) and return it in `/data`.

---

## Level 2 (medium)
### D) Add “Drive for 0.5 seconds” commands
Right now, movement continues until Stop.

Add routes like:
- `/pulse/forward?ms=400`
- It drives, sleeps, then stops

This can help drive more precisely.

---

## Level 3 (advanced)
### E) Add a “Maze Mode” toggle (manual → autonomous)
Add routes:
- `/mode/manual`
- `/mode/maze`

Then in the server loop, if mode is maze, run your maze logic periodically.

**Key idea:** don’t block the web server for a long time.  
Do small steps and return quickly so the web UI still responds.

---

# 8) Debugging checklist

## Can’t open the web page
- Confirm the OLED shows an IP address
- Try:
  - `http://<ip>/` (same network as the Pico)
- Some school networks block device-to-device traffic. Use a travel router/hotspot if needed.

## Buttons work but distance stays `---`
- Check ultrasonic wiring (TRIG/ECHO pins)
- Ensure the sensor is powered correctly (HC-SR04P at 3.3V)
- Try printing distance in a simple test script

fileciteturn1file2

## Robot drifts while moving forward
Adjust trims in `picobot_lib.py`:
- `LEFT_TRIM`
- `RIGHT_TRIM`

fileciteturn1file2

---

# TODOs (copy/paste)

- TODO 1: Add an “Emergency Stop (Brake)” button.
- TODO 2: Add auto-stop if distance < 10 cm.
- TODO 3: Add a “Pulse move” (drive for 300 ms).
- TODO 4: Add a “Maze Mode” start/stop toggle.
- TODO 5: Add a “Turn Left” button (already supported by `bot.drive_left()`).

---

## One more safety reminder
Test on a table-free floor area first (no stairs), start with lower power (50–60), and keep a hand near the power switch.
