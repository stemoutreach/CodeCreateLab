#!/usr/bin/env python3
"""
Sense HAT Mission Dashboard (Starter Template)
———————————————————————————————
This program uses the Sense HAT to display environmental data and orientation
information. Students will implement multiple display modes and joystick control.

Press the joystick center to cycle modes.
Press Ctrl-C to exit cleanly.
"""

from sense_hat import SenseHat, ACTION_PRESSED
import time
import math

sense = SenseHat()
sense.set_rotation(180)  # Optional: adjust based on your Pi's orientation

# ─────────────────────── ToDo: Define Pixel Art for Arrows ─────────────────────── #
# Use RGB triplets to define pixel colors, e.g.:
# R = [255, 0, 0]   # Red
# Then define 8x8 arrow matrices like ARROW_UP, ARROW_DOWN, etc.

# ToDo: Create ARROW_UP, ARROW_DOWN, ARROW_LEFT, and ARROW_RIGHT arrays here

# ─────────────────────────── Compass Needle Drawing ───────────────────────────── #

def draw_compass(heading):
    """ToDo: Draw compass needle based on heading (0–360 degrees)."""
    # Convert heading to radians and calculate x/y for needle
    # Place a white dot at center and red pixel in needle direction
    pass

# ─────────────────────────── Orientation Arrow Drawing ────────────────────────── #

def draw_orientation_arrow():
    """ToDo: Use pitch and roll to decide which arrow to show."""
    # Read orientation using sense.get_orientation()
    # Use if-else logic to determine arrow direction and set pixels
    pass

# ─────────────────────────── Environment Display ──────────────────────────────── #

def scroll_environment():
    """ToDo: Scroll temperature, humidity, and pressure with color coding."""
    # Read temp, humidity, pressure
    # Use sense.show_message to scroll each value in different color
    pass

# ───────────────────────────── Joystick Handling ──────────────────────────────── #

MODES = ["orientation", "environment", "compass"]
mode_index = 0

def on_joystick(event):
    """ToDo: Handle joystick center press to change mode."""
    global mode_index
    if event.action == ACTION_PRESSED and event.direction == "middle":
        mode_index = (mode_index + 1) % len(MODES)
        sense.clear()  # Optional: clear LED matrix on mode change

# Attach joystick callback
sense.stick.direction_any = on_joystick

# ──────────────────────────────── Main Loop ───────────────────────────────────── #

try:
    while True:
        current = MODES[mode_index]

        if current == "orientation":
            draw_orientation_arrow()

        elif current == "environment":
            scroll_environment()

        elif current == "compass":
            heading = sense.get_compass()
            draw_compass(heading)

        time.sleep(0.1)

except KeyboardInterrupt:
    sense.clear()
    print("\nMission Dashboard closed. Goodbye!")
