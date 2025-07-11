# Solution: 1 Sense Hat Basic Lab: Weather Warning Light

Solution Code

```python

#!/usr/bin/env python
"""
Weather Warning Light for Sense HAT
Shows red if the environment is outside safe limits,
otherwise shows green. Demonstrates input, print,
conditions, and functions.
"""

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def get_readings():
    """Return rounded temperature (°C) and humidity (%) as a tuple."""
    temp = round(sense.get_temperature(), 1)
    hum  = round(sense.get_humidity(), 1)
    return temp, hum

def show_status(temp, hum, temp_limit, hum_limit):
    """Print readings and set LED colour based on the limits."""
    print(f"Temp: {temp} °C | Humidity: {hum} %")
    if temp > temp_limit or hum < hum_limit:
        sense.clear(255, 0, 0)   # Red alert
        print("⚠️  WARNING: Unsafe environment!")
    else:
        sense.clear(0, 255, 0)   # Green OK
        print("Environment OK")

def main():
    print("Sense HAT Weather Warning Light")
    # Ask the user for limits
    temp_limit = float(input("Enter the high‑temperature limit (°C): "))
    hum_limit  = float(input("Enter the low‑humidity limit (%): "))
    print("Press Ctrl‑C to exit.")

    try:
        while True:
            temp, hum = get_readings()
            show_status(temp, hum, temp_limit, hum_limit)
            time.sleep(2)
    except KeyboardInterrupt:
        sense.clear()
        print("\nProgram ended. Stay safe!")

if __name__ == "__main__":
    main()
```
