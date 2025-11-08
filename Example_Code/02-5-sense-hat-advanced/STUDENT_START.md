# STUDENT_START — 02.5 Sense HAT Advanced (Mission Dashboard)

**Use this only if you're stuck for 5–7 minutes.**
This is a minimal starter with TODOs — no full solution.

```python
from sense_hat import SenseHat, ACTION_PRESSED
import time, math

sense = SenseHat()
sense.clear()

R = (255, 0, 0); G = (0, 255, 0); B = (0, 0, 255); W = (255,255,255); K = (0,0,0)

# TODO: ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT = [... 64 tuples ...]

MODES = ["orientation", "environment", "compass"]
mode_index = 0

def draw_orientation_arrow(sense):
    # TODO
    pass

def scroll_environment(sense):
    # TODO
    pass

def draw_compass(sense, heading):
    # TODO
    pass

def on_joystick(event):
    # TODO: if center pressed → mode_index = (mode_index + 1) % len(MODES); sense.clear()
    pass

def main():
    # TODO: attach joystick callback
    try:
        while True:
            m = MODES[mode_index]
            if m == "orientation":
                draw_orientation_arrow(sense)
            elif m == "environment":
                scroll_environment(sense)
            else:
                # TODO: heading = sense.get_compass(); draw_compass(sense, heading)
                pass
            time.sleep(0.1)
    except KeyboardInterrupt:
        sense.clear()
        print("Goodbye!")

if __name__ == "__main__":
    main()
```
