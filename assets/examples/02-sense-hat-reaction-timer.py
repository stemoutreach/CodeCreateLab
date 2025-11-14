"""
02 — Sense HAT Reaction Timer — Full Solution (with Optional Part B)

This reference implements:
- Part A: Reaction timer with best (high) score.
- Part B (optional): Sensor intermission that shows T/H/P briefly.

Classroom defaults: Raspberry Pi 500 + Sense HAT, Thonny editor.
"""

from sense_hat import SenseHat
from time import sleep, time
import random
from typing import Optional, Tuple

# ----------------------
# Config
# ----------------------
LOW_LIGHT = True
SCROLL_SPEED = 0.06
GO_DELAY_RANGE = (1.0, 3.0)
INTERMISSION_ENABLED = True     # Toggle Part B on/off
INTERMISSION_SECONDS = 5        # Duration for Part B
INTERMISSION_UPS = 4            # Updates per second during intermission
SMOOTH_SAMPLES = 3              # 1 = no smoothing, 3 = light smoothing

# ----------------------
# Colors
# ----------------------
BLACK  = (0, 0, 0)
NAVY   = (0, 0, 30)
GREEN  = (0, 150, 0)
RED    = (180, 0, 0)
WHITE  = (255, 255, 255)
DIM_OK = (0, 60, 0)

# ----------------------
# Part A — Display helpers
# ----------------------
def show_ready(sense: SenseHat) -> None:
    sense.clear(NAVY)
    sense.show_message("Ready", scroll_speed=SCROLL_SPEED, text_colour=WHITE, back_colour=NAVY)

def show_go(sense: SenseHat) -> None:
    sense.clear(GREEN)
    sense.show_letter("G", text_colour=WHITE, back_colour=GREEN)

def show_score(sense: SenseHat, ms: int, best_ms: Optional[int]) -> None:
    sense.show_message(f"{ms} ms", scroll_speed=SCROLL_SPEED, text_colour=WHITE)
    if best_ms is not None and ms == best_ms:
        # Small celebration for a new best
        sense.show_letter("✓", text_colour=(0, 200, 0), back_colour=DIM_OK)
        sleep(0.6)

def wait_for_middle_press(sense: SenseHat) -> None:
    """Block until the joystick middle is pressed; return when it happens."""
    while True:
        for e in sense.stick.get_events():
            if e.action == "pressed" and e.direction == "middle":
                return
        sleep(0.01)  # small yield

# ----------------------
# Optional — False start detection (not required)
# ----------------------
def false_start_detected(sense: SenseHat) -> bool:
    """Return True if the middle joystick was pressed (false start)."""
    for e in sense.stick.get_events():
        if e.action == "pressed" and e.direction == "middle":
            return True
    return False

def handle_false_start(sense: SenseHat) -> None:
    sense.clear(RED)
    sense.show_letter("!", text_colour=WHITE, back_colour=RED)
    sleep(0.8)
    sense.clear()

# ----------------------
# Part B — Sensor Intermission (Optional)
# ----------------------
def _smooth(values) -> float:
    return round(sum(values) / len(values), 1)

def _read_env_triplet(sense: SenseHat, samples: int = 1) -> Tuple[float, float, float]:
    """Read temperature (°C), humidity (%), pressure (hPa) with optional light smoothing."""
    t_vals, h_vals, p_vals = [], [], []
    for _ in range(max(1, samples)):
        t_vals.append(sense.get_temperature())
        h_vals.append(sense.get_humidity())
        p_vals.append(sense.get_pressure())
        if samples > 1:
            sleep(0.02)  # tiny spacing between samples
    if samples > 1:
        t = _smooth(t_vals)
        h = _smooth(h_vals)
        p = _smooth(p_vals)
    else:
        t = round(t_vals[-1], 1)
        h = round(h_vals[-1], 1)
        p = round(p_vals[-1], 1)
    return t, h, p

def show_env_intermission(sense: SenseHat,
                          seconds: int = INTERMISSION_SECONDS,
                          ups: int = INTERMISSION_UPS,
                          samples: int = SMOOTH_SAMPLES) -> None:
    """
    Briefly show live T/H/P readings, then return to the main loop.
    Uses scrolling text for readability. Keep it short and tidy.
    """
    end_time = time() + max(1, seconds)
    pause = 1.0 / max(1, ups)
    while time() < end_time:
        t, h, p = _read_env_triplet(sense, samples=samples)
        msg = f"T:{t}C  H:{h}%  P:{p}h"
        sense.show_message(msg, scroll_speed=0.05, text_colour=(220, 220, 220))
        sleep(pause)
    # Tidy up handled by caller; keep current screen or clear next.

# ----------------------
# Main
# ----------------------
def main() -> None:
    sense = SenseHat()
    sense.low_light = LOW_LIGHT

    best_ms: Optional[int] = None
    try:
        while True:
            # 1) Ready
            show_ready(sense)

            # 2) Random delay (optionally detect a false start)
            delay = random.uniform(*GO_DELAY_RANGE)
            t0 = time()
            while time() - t0 < delay:
                if false_start_detected(sense):   # optional feature
                    handle_false_start(sense)
                    break
                sleep(0.01)
            else:
                # 3) GO and precise start time
                show_go(sense)
                start = time()

                # 4) Wait for press and compute elapsed
                wait_for_middle_press(sense)
                elapsed_ms = int((time() - start) * 1000)

                # 5) Best score update + display
                if best_ms is None or elapsed_ms < best_ms:
                    best_ms = elapsed_ms
                show_score(sense, elapsed_ms, best_ms)

                # 6) Optional Part B — Sensor Intermission
                if INTERMISSION_ENABLED:
                    show_env_intermission(sense)

                # 7) Small pause and clear before next round
                sleep(1.0)
            sense.clear()
    finally:
        sense.clear()

if __name__ == "__main__":
    main()
