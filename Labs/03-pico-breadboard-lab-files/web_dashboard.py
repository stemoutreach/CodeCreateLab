"""
Pico WiFi Dashboard (Live + Capture Toggle + Part A RGB + OLED Distance + Buzzer)

What this does
- Web dashboard at http://<Pico IP>/
- Toggle "capture" (ultrasonic sampling) from the page or from the physical button
- While ACTIVE:
  - Reads distance
  - Sets RGB color using Part A thresholds
  - Updates OLED bottom line (if present)
  - Beeps the buzzer (same "distance-station" style feedback)

RGB thresholds (cm)
- distance < 20   -> RED
- 20–40           -> YELLOW
- > 40            -> GREEN

Buzzer behavior (cm)
- distance < 20   -> fast beeps
- 20–40           -> slow beeps
- > 40 / no read  -> silent
"""

import gc
import socket
import ujson
import utime
from machine import Pin, PWM
from picozero import LED, Button, DistanceSensor, RGBLED

# --- Pins (Lab Standard Map) ---
STATUS_LED_PIN = 14            # external status LED (optional)
BUTTON_PIN     = 13            # pushbutton toggles capture
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11
RGB_R_PIN      = 17
RGB_G_PIN      = 18
RGB_B_PIN      = 19
SPEAKER_PIN    = 20            # buzzer/speaker

# --- Part A thresholds (cm) ---
CLOSE_CM = 20.0
MEDIUM_MAX_CM = 40.0

# --- Timing ---
_DEBOUNCE_MS = 250
_SENSOR_UPDATE_MS = 500

# --- Buzzer tune ---
BUZZER_FREQ_HZ = 2000
BUZZER_DUTY_U16 = 20000  # volume (0..65535)

# Beep patterns (ms) while ACTIVE
BEEP_FAST_PERIOD_MS = 250
BEEP_FAST_ON_MS     = 60

BEEP_SLOW_PERIOD_MS = 800
BEEP_SLOW_ON_MS     = 50

# If your RGB is common-anode, set True to invert
RGB_COMMON_ANODE = False

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN, pull_up=True)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
rgb = RGBLED(red=RGB_R_PIN, green=RGB_G_PIN, blue=RGB_B_PIN)
onboard_led = Pin("LED", Pin.OUT)

# --- OLED support (show_distance preferred, show_status_line fallback) ---
try:
    import oled_status
except Exception:
    oled_status = None

# --- Buzzer (PWM) ---
_buzzer_pwm = None
try:
    _buzzer_pwm = PWM(Pin(SPEAKER_PIN))
    _buzzer_pwm.freq(BUZZER_FREQ_HZ)
    _buzzer_pwm.duty_u16(0)  # OFF
except Exception:
    _buzzer_pwm = None

sensor_active = False
_last_distance_cm = None
_last_rgb_name = "OFF"
_last_rgb_f = (0.0, 0.0, 0.0)
_last_sensor_update_ms = 0

# Buzzer scheduler state
_buzzing = False
_buzzer_on_until_ms = 0
_buzzer_next_start_ms = 0


def _buzzer_off():
    global _buzzing
    if _buzzer_pwm is None:
        return
    try:
        _buzzer_pwm.duty_u16(0)
    except Exception:
        pass
    _buzzing = False


def _buzzer_on():
    global _buzzing
    if _buzzer_pwm is None:
        return
    try:
        _buzzer_pwm.duty_u16(BUZZER_DUTY_U16)
    except Exception:
        pass
    _buzzing = True


def _buzzer_reset():
    global _buzzer_on_until_ms, _buzzer_next_start_ms
    _buzzer_off()
    _buzzer_on_until_ms = 0
    _buzzer_next_start_ms = 0


def _buzzer_pattern_for_distance(distance_cm):
    """Return (period_ms, on_ms) or (None, None) for silent."""
    if distance_cm is None:
        return (None, None)

    if distance_cm < CLOSE_CM:
        return (BEEP_FAST_PERIOD_MS, BEEP_FAST_ON_MS)

    if distance_cm <= MEDIUM_MAX_CM:
        return (BEEP_SLOW_PERIOD_MS, BEEP_SLOW_ON_MS)

    return (None, None)


def _buzzer_tick(distance_cm, active: bool):
    """Non-blocking buzzer scheduler. Call frequently."""
    global _buzzer_on_until_ms, _buzzer_next_start_ms

    if (not active) or (_buzzer_pwm is None):
        _buzzer_reset()
        return

    period_ms, on_ms = _buzzer_pattern_for_distance(distance_cm)

    if period_ms is None:
        _buzzer_reset()
        return

    now = utime.ticks_ms()

    # Turn off when on-time expires
    if _buzzing and utime.ticks_diff(now, _buzzer_on_until_ms) >= 0:
        _buzzer_off()

    # Start a new beep if it's time (and we're currently off)
    if (not _buzzing) and (utime.ticks_diff(now, _buzzer_next_start_ms) >= 0):
        _buzzer_on()
        _buzzer_on_until_ms = utime.ticks_add(now, on_ms)
        _buzzer_next_start_ms = utime.ticks_add(now, period_ms)


def _set_active(active: bool) -> bool:
    global sensor_active, _last_distance_cm, _last_rgb_name, _last_rgb_f
    sensor_active = bool(active)

    if sensor_active:
        status_led.on()
        onboard_led.on()
        _maybe_update_sensor(force=True)
    else:
        status_led.off()
        onboard_led.off()
        _last_distance_cm = None
        _last_rgb_name = "OFF"
        _last_rgb_f = (0.0, 0.0, 0.0)
        _rgb_off()
        _oled_distance(None, active=False)
        _buzzer_reset()

    return sensor_active


def _toggle_active() -> bool:
    return _set_active(not sensor_active)


def _safe_distance_cm():
    try:
        d_m = sensor.distance
        d_cm = float(d_m) * 100.0
        if d_cm < 0:
            return None
        return d_cm
    except Exception:
        return None


def _rgb_apply(r: float, g: float, b: float):
    if RGB_COMMON_ANODE:
        r, g, b = (1.0 - r), (1.0 - g), (1.0 - b)
    rgb.color = (r, g, b)


def _rgb_off():
    _rgb_apply(0.0, 0.0, 0.0)


def _color_from_distance(distance_cm):
    if distance_cm is None:
        return "NO READ", (0.0, 0.0, 1.0)  # BLUE = read error while active

    if distance_cm < CLOSE_CM:
        return "RED", (1.0, 0.0, 0.0)
    elif distance_cm <= MEDIUM_MAX_CM:
        return "YELLOW", (1.0, 1.0, 0.0)
    else:
        return "GREEN", (0.0, 1.0, 0.0)


def _oled_distance(distance_cm, active: bool):
    """
    Update OLED bottom line:
    - Prefer oled_status.show_distance(distance_cm, active=...)
    - Fallback: oled_status.show_status_line("Distance=...")
    """
    if oled_status is None:
        return

    try:
        if hasattr(oled_status, "show_distance"):
            oled_status.show_distance(distance_cm, active=active)
            return

        if not active:
            oled_status.show_status_line("Distance=PAUSED")
            return

        if distance_cm is None:
            oled_status.show_status_line("Distance=---")
            return

        oled_status.show_status_line("Distance=%0.1fcm" % float(distance_cm))
    except Exception:
        pass


def _maybe_update_sensor(force: bool = False):
    global _last_distance_cm, _last_rgb_name, _last_rgb_f, _last_sensor_update_ms

    if not sensor_active:
        return

    now = utime.ticks_ms()
    if (not force) and utime.ticks_diff(now, _last_sensor_update_ms) < _SENSOR_UPDATE_MS:
        return
    _last_sensor_update_ms = now

    d_cm = _safe_distance_cm()
    rgb_name, (r, g, b) = _color_from_distance(d_cm)

    _last_distance_cm = d_cm
    _last_rgb_name = rgb_name
    _last_rgb_f = (r, g, b)

    _rgb_apply(r, g, b)
    _oled_distance(d_cm, active=True)


def _rgb_to_255(r: float, g: float, b: float):
    return int(r * 255), int(g * 255), int(b * 255)


def _http_response(body: bytes, content_type: str = "text/plain", status: str = "200 OK") -> bytes:
    headers = (
        "HTTP/1.1 " + status + "\r\n"
        "Content-Type: " + content_type + "\r\n"
        "Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n"
        "Pragma: no-cache\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body


def _page_html(ip: str, poll_ms: int = 500) -> bytes:
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Pico WiFi Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; margin: 1rem; }}
    .box {{ border: 1px solid #ccc; padding: 0.75rem; border-radius: 10px; margin: 0.75rem 0; }}
    button {{ padding: 0.75rem 1.1rem; margin-right: 0.5rem; border-radius: 10px; border: 1px solid #999; }}
    .value {{ font-weight: 700; }}
    .small {{ opacity: 0.8; font-size: 0.95rem; }}
    code {{ background: #eee; padding: 0.1rem 0.25rem; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Pico WiFi Dashboard</h1>
  <p class="small"><strong>IP:</strong> {ip}</p>

  <div class="box">
    <h2>Ultrasonic Capture</h2>
    <p>
      <button onclick="toggleActive()">Toggle Capture</button>
      <span class="small">Tip: button (GPIO {BUTTON_PIN}) toggles too.</span>
    </p>
    <p><strong>Capture:</strong> <span id="active" class="value">--</span></p>
  </div>

  <div class="box">
    <h2>Live Readings</h2>
    <p><strong>Distance:</strong> <span id="dist" class="value">--</span> <span class="small">cm</span></p>
    <p><strong>Button:</strong> <span id="btn" class="value">--</span></p>
    <p><strong>Status LED:</strong> <span id="led" class="value">--</span></p>

    <p><strong>RGB Color:</strong> <span id="rgbName" class="value">--</span></p>
    <p class="small"><strong>RGB (0–255):</strong> <code id="rgb255">--</code></p>

    <p class="small">Updates every {poll_ms} ms</p>
  </div>

<script>
async function toggleActive() {{
  try {{
    await fetch('/capture/toggle', {{ cache: 'no-store' }});
    await tick();
  }} catch (e) {{}}
}}

async function tick() {{
  try {{
    const r = await fetch('/data', {{ cache: 'no-store' }});
    const j = await r.json();

    document.getElementById('btn').textContent = j.button_pressed ? 'Pressed' : 'Released';
    document.getElementById('led').textContent = j.led_on ? 'ON' : 'OFF';
    document.getElementById('active').textContent = j.sensor_active ? 'ACTIVE' : 'INACTIVE';

    document.getElementById('rgbName').textContent = j.rgb_name;
    document.getElementById('rgb255').textContent = `(${{j.rgb_255[0]}}, ${{j.rgb_255[1]}}, ${{j.rgb_255[2]}})`;

    if (!j.sensor_active) {{
      document.getElementById('dist').textContent = 'PAUSED';
    }} else {{
      document.getElementById('dist').textContent = (j.distance_cm === null) ? '---' : j.distance_cm.toFixed(1);
    }}
  }} catch (e) {{
    document.getElementById('dist').textContent = '---';
  }}
}}

tick();
setInterval(tick, {poll_ms});
</script>
</body>
</html>
"""
    return html.encode("utf-8")


def _parse_path(request_text: str) -> str:
    try:
        first_line = request_text.split("\r\n", 1)[0]
        parts = first_line.split(" ")
        if len(parts) >= 2:
            return parts[1]
    except Exception:
        pass
    return "/"


def run_server(ip: str, poll_ms: int = 500):
    _set_active(False)
    _oled_distance(None, active=False)
    _buzzer_reset()

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.settimeout(0.1)
    s.bind(addr)
    s.listen(1)

    print("Listening on", addr)
    print("Open: http://%s/" % ip)

    last_pressed = False
    last_toggle_ms = utime.ticks_ms()

    while True:
        pressed = bool(button.is_pressed)
        if pressed and (not last_pressed):
            now = utime.ticks_ms()
            if utime.ticks_diff(now, last_toggle_ms) >= _DEBOUNCE_MS:
                _toggle_active()
                last_toggle_ms = now
        last_pressed = pressed

        _maybe_update_sensor(force=False)

        # Non-blocking buzzer
        _buzzer_tick(_last_distance_cm, active=sensor_active)

        try:
            cl, _ = s.accept()
        except OSError:
            gc.collect()
            continue

        try:
            cl.settimeout(2)
            req = cl.recv(1024)
            if not req:
                cl.close()
                continue

            path = _parse_path(req.decode("utf-8", "ignore"))

            if path.startswith("/capture/toggle"):
                new_state = _toggle_active()
                body = ujson.dumps({"sensor_active": bool(new_state)}).encode()
                cl.sendall(_http_response(body, "application/json"))
                continue

            if path.startswith("/data"):
                _maybe_update_sensor(force=False)

                if sensor_active:
                    d_cm = _last_distance_cm
                    rgb_name = _last_rgb_name
                    r, g, b = _last_rgb_f
                else:
                    d_cm = None
                    rgb_name = "OFF"
                    r, g, b = (0.0, 0.0, 0.0)

                payload = {
                    "distance_cm": d_cm,
                    "sensor_active": bool(sensor_active),
                    "button_pressed": bool(button.is_pressed),
                    "led_on": bool(status_led.value),
                    "rgb_name": rgb_name,
                    "rgb_255": _rgb_to_255(r, g, b),
                    "ms": utime.ticks_ms(),
                }
                cl.sendall(_http_response(ujson.dumps(payload).encode(), "application/json"))
                continue

            cl.sendall(_http_response(_page_html(ip, poll_ms=poll_ms), "text/html"))

        except Exception as e:
            try:
                cl.sendall(_http_response(("Error: %s" % e).encode(), "text/plain", status="500 Internal Server Error"))
            except Exception:
                pass
            print("Client error:", e)
        finally:
            try:
                cl.close()
            except Exception:
                pass
            gc.collect()
