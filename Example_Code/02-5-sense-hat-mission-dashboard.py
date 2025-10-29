
"""Sense HAT Advanced — Mission Dashboard (Starter)"""
from sense_hat import SenseHat, ACTION_PRESSED
import time, math

sense = SenseHat()
sense.set_rotation(180)

# Colors
R = (255, 0, 0); G = (0, 255, 0); B = (0, 0, 255); W = (255,255,255); K = (0,0,0)

# Simple arrow pixel art (8x8)
def arrow_up():
    X = R; O = K
    # simple triangle up; customize as desired
    pattern = [
        O,O,O,X,X,O,O,O,
        O,O,X,X,X,X,O,O,
        O,X,O,X,X,O,X,O,
        X,O,O,X,X,O,O,X,
        O,O,O,X,X,O,O,O,
        O,O,O,X,X,O,O,O,
        O,O,O,X,X,O,O,O,
        O,O,O,X,X,O,O,O,
    ]
    return pattern

ARROW_UP = arrow_up()
ARROW_DOWN = ARROW_UP[::-1]
ARROW_LEFT = ARROW_UP  # TODO: replace with your own left/right patterns
ARROW_RIGHT = ARROW_UP # TODO: replace with your own left/right patterns

def draw_compass(heading):
    rad = math.radians(heading)
    cx, cy = 3, 3
    x = int(round(cx + 3 * math.sin(rad)))
    y = int(round(cy - 3 * math.cos(rad)))
    x = max(0, min(7, x)); y = max(0, min(7, y))
    sense.clear()
    sense.set_pixel(3, 3, W); sense.set_pixel(4, 4, W)
    sense.set_pixel(x, y, R)

def draw_orientation_arrow():
    o = sense.get_orientation()
    pitch, roll = o['pitch'], o['roll']
    pattern = ARROW_UP
    if pitch > 30:   pattern = ARROW_DOWN
    elif roll > 30:  pattern = ARROW_RIGHT
    elif roll < -30: pattern = ARROW_LEFT
    sense.set_pixels(pattern)

def scroll_environment():
    t = sense.get_temperature()
    h = sense.get_humidity()
    p = sense.get_pressure()
    sense.show_message(f"T={t:.1f}C", text_colour=R, scroll_speed=0.06)
    sense.show_message(f"H={h:.1f}%", text_colour=G, scroll_speed=0.06)
    sense.show_message(f"P={p:.0f}mbar", text_colour=B, scroll_speed=0.06)

MODES = ["orientation", "environment", "compass"]
mode_index = 0

def on_joystick(event):
    global mode_index
    if event.action == ACTION_PRESSED and event.direction == "middle":
        mode_index = (mode_index + 1) % len(MODES)
        sense.clear()

sense.stick.direction_any = on_joystick

try:
    while True:
        m = MODES[mode_index]
        if m == "orientation":
            draw_orientation_arrow()
        elif m == "environment":
            scroll_environment()
        else:
            draw_compass(sense.get_compass())
        time.sleep(0.1)
except KeyboardInterrupt:
    sense.clear()
    print("\nGoodbye!")
