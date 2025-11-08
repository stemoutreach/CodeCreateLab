
# Sense HAT Mission Dashboard (Advanced) — Starter
# Interpreter: Python 3 (Local) on Raspberry Pi OS

from sense_hat import SenseHat
from time import time, sleep

sense = SenseHat()
sense.low_light = True

# === MODES & STATE ===
MODES = ["Temp", "Humidity", "Pressure"]
mode_idx = 0
show_overlay = True

# === COLORS ===
R = (255, 0, 0); Y = (255, 170, 0); G = (0, 180, 0); B = (0, 0, 200)
K = (0, 0, 0)

# TODO: replace placeholders with real 8x8 icons (list of 64 tuples)
def temp_icon(color): return [K] * 64
def humidity_icon(color): return [K] * 64
def pressure_icon(color): return [K] * 64

def thresholds_for(mode, value):
    if mode == "Temp":
        if value < 18: return B
        if value <= 27: return G
        return R
    if mode == "Humidity":
        if value < 30: return Y
        if value <= 60: return G
        return R
    if mode == "Pressure":
        if value < 990: return Y
        if value <= 1020: return G
        return R
    return G

def read_values():
    t = round(sense.get_temperature(), 1)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())
    return t, h, p

def render(mode, value, color, overlay):
    # TODO: select icon by mode and draw with sense.set_pixels()
    # TODO: if overlay is True, show numeric briefly (show_message or custom row overlay)
    sense.set_pixels(temp_icon(color))  # placeholder

def on_joystick_event(event):
    global mode_idx, show_overlay
    if event.action != "pressed":
        return
    if event.direction == "right":
        mode_idx = (mode_idx + 1) % len(MODES)
    elif event.direction == "left":
        mode_idx = (mode_idx - 1) % len(MODES)
    elif event.direction == "middle":
        show_overlay = not show_overlay

def main():
    sense.stick.direction_any = on_joystick_event
    target_fps = 8
    dt = 1.0 / target_fps
    last = 0.0
    try:
        while True:
            now = time()
            if now - last >= dt:
                last = now
                t, h, p = read_values()
                mode = MODES[mode_idx]
                value = t if mode == "Temp" else h if mode == "Humidity" else p
                color = thresholds_for(mode, value)
                render(mode, value, color, show_overlay)
            sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

if __name__ == "__main__":
    main()
