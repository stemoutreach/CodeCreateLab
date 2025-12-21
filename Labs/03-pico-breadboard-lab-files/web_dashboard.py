# web_dashboard.py
"""
Pico WiFi Dashboard (Live + Capture Toggle + Part A RGB + OLED Distance)

Why your OLED stayed on "PAUSED":
- Your current oled_status.py only has show_status_line().
- The live dashboard tries to call show_distance() for updates.
- If show_distance() doesn't exist, the dashboard can’t update the OLED.

This version:
- Updates OLED live using show_distance() if available,
  OR falls back to show_status_line("Distance=...") if not.
- Matches Part A thresholds:
    close < 20 cm  -> RGB RED
    20–40 cm       -> RGB YELLOW
    > 40 cm        -> RGB GREEN
"""

import gc
import socket
import ujson
import utime
from machine import Pin
from picozero import LED, Button, DistanceSensor, RGBLED

# --- Pins (Lab Standard Map) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 13
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11
RGB_R_PIN = 17
RGB_G_PIN = 18
RGB_B_PIN = 19

# --- Part A thresholds (cm) ---
CLOSE_CM = 20.0
MEDIUM_MAX_CM = 40.0

RGB_COMMON_ANODE = False
_DEBOUNCE_MS = 250
_SENSOR_UPDATE_MS = 500

status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
rgb = RGBLED(red=RGB_R_PIN, green=RGB_G_PIN, blue=RGB_B_PIN)
onboard_led = Pin("LED", Pin.OUT)

# OLED support (show_distance preferred, show_status_line fallback)
try:
    import oled_status
except Exception:
    oled_status = None

sensor_active = False
_last_distance_cm = None
_last_rgb_name = "OFF"
_last_rgb_f = (0.0, 0.0, 0.0)
_last_sensor_update_ms = 0


def _set_active(active: bool) -> bool:
    global sensor_active, _last_distance_cm, _last_rgb_name, _last_rgb_f
    sensor_active = bool(active)

    if sensor_active:
        status_led.on()
        onboard_led.on()
    else:
        status_led.off()
        onboard_led.off()
        _last_distance_cm = None
        _last_rgb_name = "OFF"
        _last_rgb_f = (0.0, 0.0, 0.0)
        _rgb_off()
        _oled_distance(None, active=False)

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


def _rgb_to_255(r: float, g: float, b: float):
    return int(r * 255), int(g * 255), int(b * 255)


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

        # Fallback to show_status_line only
        if not active:
            oled_status.show_status_line("Distance=PAUSED")
            return

        if distance_cm is None:
            oled_status.show_status_line("Distance=---")
            return

        # "Distance=123.4cm" fits 16 chars
        oled_status.show_status_line("Distance=%0.1fcm" % float(distance_cm))
    except Exception as e:
        # Don't hard-crash if OLED isn't present; just print once in a while if you want
        # print("OLED update error:", e)
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
      <span class="small">Tip: Pico button (GPIO 13) toggles too.</span>
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
                if sensor_active:
                    _maybe_update_sensor(force=True)
                last_toggle_ms = now
        last_pressed = pressed

        _maybe_update_sensor(force=False)

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
                if new_state:
                    _maybe_update_sensor(force=True)
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
