# picobot_web_dashboard.py
"""
PicoBot Web Dashboard (Drive + Live Status)

What this does
- Web dashboard at http://<Pico IP>/
- Drive controls: Forward / Back / Left / Right / Stop
- Power slider (0–100)
- Live status JSON at /data
- Displays same core info as OLED: State + Distance + IP (plus Speed)

Notes
- Uses picobot_lib for:
  - drive_forward/drive_back/drive_left/drive_right/stop
  - distance_cm()
  - oled_show_status()
  - oled_set_ip()
"""

import gc
import socket
import ujson
import utime

import picobot_lib as bot


# -----------------------------
# Config
# -----------------------------
POLL_MS = 250               # browser polling interval
SENSOR_UPDATE_MS = 150      # how often to refresh distance on device
DEFAULT_SPEED = 60          # default power slider value on boot


# -----------------------------
# Runtime state
# -----------------------------
_current_speed = DEFAULT_SPEED
_current_state = "STOPPED"     # STOPPED / FORWARD / BACK / LEFT / RIGHT
_last_distance_cm = None
_last_sensor_update_ms = 0
_ip_str = None


# -----------------------------
# Helpers
# -----------------------------
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


def _parse_path(request_text: str) -> str:
    try:
        first_line = request_text.split("\r\n", 1)[0]
        parts = first_line.split(" ")
        if len(parts) >= 2:
            return parts[1]
    except Exception:
        pass
    return "/"


def _split_path_query(path: str):
    # returns (route, query_string)
    if "?" in path:
        route, qs = path.split("?", 1)
        return route, qs
    return path, ""


def _get_query_param(qs: str, key: str):
    # super small query parser: key=value&key2=value2
    if not qs:
        return None
    pairs = qs.split("&")
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            if k == key:
                return v
    return None


def _maybe_update_sensor(force: bool = False):
    global _last_distance_cm, _last_sensor_update_ms

    now = utime.ticks_ms()
    if (not force) and (utime.ticks_diff(now, _last_sensor_update_ms) < SENSOR_UPDATE_MS):
        return
    _last_sensor_update_ms = now

    try:
        _last_distance_cm = bot.distance_cm()
    except Exception:
        _last_distance_cm = None


def _oled_refresh():
    # Keep OLED showing the same core info as the dashboard
    # (State + Distance + IP already stored in bot via oled_set_ip)
    try:
        bot.oled_show_status(dist=_last_distance_cm, state=_current_state)
    except Exception:
        pass


def _set_speed(new_speed: int):
    global _current_speed
    try:
        s = int(new_speed)
    except Exception:
        return

    if s < 0:
        s = 0
    if s > 100:
        s = 100

    _current_speed = s

    # If currently moving, re-apply motion at new speed (smooth)
    if _current_state == "FORWARD":
        bot.drive_forward(_current_speed)
    elif _current_state == "BACK":
        bot.drive_back(_current_speed)
    elif _current_state == "LEFT":
        bot.drive_left(_current_speed)
    elif _current_state == "RIGHT":
        bot.drive_right(_current_speed)

    _oled_refresh()


def _set_motion(state: str):
    global _current_state

    state = state.upper()
    if state == _current_state:
        return

    if state == "STOPPED" or state == "STOP":
        bot.stop(brake=False)
        _current_state = "STOPPED"
    elif state == "FORWARD":
        bot.drive_forward(_current_speed)
        _current_state = "FORWARD"
    elif state == "BACK":
        bot.drive_back(_current_speed)
        _current_state = "BACK"
    elif state == "LEFT":
        bot.drive_left(_current_speed)
        _current_state = "LEFT"
    elif state == "RIGHT":
        bot.drive_right(_current_speed)
        _current_state = "RIGHT"
    else:
        return

    _oled_refresh()


def _page_html(ip: str, poll_ms: int = 250) -> bytes:
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PicoBot Web Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: sans-serif; margin: 1rem; }}
    .box {{ border: 1px solid #ccc; padding: 0.9rem; border-radius: 12px; margin: 0.8rem 0; }}
    .row {{ display: flex; gap: 0.6rem; flex-wrap: wrap; }}
    button {{
      padding: 0.9rem 1.1rem; border-radius: 12px;
      border: 1px solid #999; background: #f6f6f6;
      font-size: 1rem;
      min-width: 110px;
    }}
    button.stop {{ background: #ffecec; }}
    .value {{ font-weight: 700; }}
    .small {{ opacity: 0.8; font-size: 0.95rem; }}
    input[type="range"] {{ width: 100%; }}
    code {{ background: #eee; padding: 0.1rem 0.25rem; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>PicoBot Dashboard</h1>
  <p class="small"><strong>IP:</strong> <span class="value">{ip}</span></p>

  <div class="box">
    <h2>Drive</h2>
    <div class="row">
      <button onclick="move('forward')">Forward</button>
      <button onclick="move('back')">Back</button>
      <button onclick="move('left')">Left</button>
      <button onclick="move('right')">Right</button>
      <button class="stop" onclick="move('stop')">Stop</button>
    </div>

    <p style="margin-top:1rem;"><strong>Power:</strong> <span id="speedVal" class="value">--</span>%</p>
    <input id="speed" type="range" min="0" max="100" value="{DEFAULT_SPEED}" oninput="setSpeed(this.value)">
    <p class="small">Tip: set power first, then click a direction. The robot keeps moving until Stop.</p>
  </div>

  <div class="box">
    <h2>Live Status</h2>
    <p><strong>State:</strong> <span id="state" class="value">--</span></p>
    <p><strong>Distance:</strong> <span id="dist" class="value">--</span> <span class="small">cm</span></p>
    <p><strong>IP:</strong> <code id="ip">{ip}</code></p>
    <p><strong>Power:</strong> <span id="speedNow" class="value">--</span>%</p>
    <p class="small">Updates every {poll_ms} ms</p>
  </div>

<script>
let speedTimer = null;

async function move(dir) {{
  try {{
    await fetch('/move/' + dir, {{ cache: 'no-store' }});
    await tick();
  }} catch (e) {{}}
}}

function setSpeed(v) {{
  document.getElementById('speedVal').textContent = v;
  // debounce requests so we don't hammer the Pico while sliding
  if (speedTimer) clearTimeout(speedTimer);
  speedTimer = setTimeout(async () => {{
    try {{
      await fetch('/speed?value=' + encodeURIComponent(v), {{ cache: 'no-store' }});
      await tick();
    }} catch (e) {{}}
  }}, 120);
}}

async function tick() {{
  try {{
    const r = await fetch('/data', {{ cache: 'no-store' }});
    const j = await r.json();

    document.getElementById('state').textContent = j.state;
    document.getElementById('speedNow').textContent = j.speed;

    if (j.distance_cm === null) {{
      document.getElementById('dist').textContent = '---';
    }} else {{
      document.getElementById('dist').textContent = j.distance_cm.toFixed(1);
    }}

  }} catch (e) {{
    document.getElementById('dist').textContent = '---';
  }}
}}

document.getElementById('speedVal').textContent = document.getElementById('speed').value;
tick();
setInterval(tick, {poll_ms});
</script>
</body>
</html>
"""
    return html.encode("utf-8")


# -----------------------------
# Server
# -----------------------------
def run_server(ip: str, poll_ms: int = POLL_MS):
    """
    Start the dashboard server.
    Pass in the Pico's IP string (e.g., from wifi.connect_wifi()).
    """
    global _ip_str

    _ip_str = ip
    try:
        bot.oled_set_ip(ip)
    except Exception:
        pass

    # start safe
    _set_motion("STOP")
    _maybe_update_sensor(force=True)
    _oled_refresh()

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.settimeout(0.1)          # short timeout so we can update sensor between requests
    s.bind(addr)
    s.listen(1)

    print("Listening on", addr)
    print("Open: http://%s/" % ip)

    while True:
        # update distance + OLED periodically (even if no web client is connected)
        _maybe_update_sensor(force=False)
        _oled_refresh()

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
            route, qs = _split_path_query(path)

            # ---- control routes ----
            if route.startswith("/move/"):
                cmd = route.split("/move/", 1)[1].strip("/").lower()
                if cmd == "forward":
                    _set_motion("FORWARD")
                elif cmd == "back":
                    _set_motion("BACK")
                elif cmd == "left":
                    _set_motion("LEFT")
                elif cmd == "right":
                    _set_motion("RIGHT")
                else:
                    _set_motion("STOP")

                body = ujson.dumps({"ok": True, "state": _current_state}).encode()
                cl.sendall(_http_response(body, "application/json"))
                continue

            if route.startswith("/speed"):
                v = _get_query_param(qs, "value")
                if v is not None:
                    _set_speed(v)
                body = ujson.dumps({"ok": True, "speed": _current_speed}).encode()
                cl.sendall(_http_response(body, "application/json"))
                continue

            # ---- data route ----
            if route.startswith("/data"):
                _maybe_update_sensor(force=False)

                payload = {
                    "ip": _ip_str,
                    "state": _current_state,
                    "speed": _current_speed,
                    "distance_cm": _last_distance_cm,
                    "ms": utime.ticks_ms(),
                }
                cl.sendall(_http_response(ujson.dumps(payload).encode(), "application/json"))
                continue

            # ---- page ----
            cl.sendall(_http_response(_page_html(ip, poll_ms=poll_ms), "text/html"))

        except Exception as e:
            try:
                cl.sendall(_http_response(("Error: %s" % e).encode(), "text/plain",
                                          status="500 Internal Server Error"))
            except Exception:
                pass
            print("Client error:", e)
        finally:
            try:
                cl.close()
            except Exception:
                pass
            gc.collect()
