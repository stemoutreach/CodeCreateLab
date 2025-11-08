# STUDENT_START — 02 Sense HAT Basics (Weather Warning Light)

**Use this only if you're stuck for 5–7 minutes.**
This gives you a minimal skeleton with TODOs — no full solution.

---

## Starter Skeleton
```python
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def read_readings():
    """Return (temp_c, humidity_percent). Round for printing."""
    # TODO: read temperature and humidity, round, and return
    return 0.0, 0.0

def show_status(temp, hum, t_limit, h_limit):
    """Set LED color and print a message based on limits."""
    # TODO: compute too_hot and too_dry
    # TODO: set LED: RED if unsafe else GREEN
    # TODO: print a readable line with units and limits

print("Sense HAT — Weather Warning Light")
# TODO: ask user for high temp limit (°C) and low humidity limit (%) as float
t_limit = 0.0
h_limit = 0.0

try:
    while True:
        temp, hum = read_readings()
        show_status(temp, hum, t_limit, h_limit)
        time.sleep(2)   # adjust sample rate
except KeyboardInterrupt:
    sense.clear()
    print("Stopped. Stay safe!")
```
---

## Self-check
- Loop stops on **Ctrl‑C** and clears LED
- Printed lines show **units** and **limits**
- LED color switches correctly around your thresholds
