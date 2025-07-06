# Lab 1 – Sense HAT Basics: Weather Monitor

## Overview
Turn your Raspberry Pi into a mini weather station: display temperature and humidity on the Sense HAT LED matrix every few seconds.

## Learning objectives
- Read environmental sensors with the `sense_hat` Python library
- Format strings for tidy output
- Use `time.sleep()` for periodic updates

## Prerequisites
- Lab 0 completed
- Sense HAT attached & drivers installed (see **Guides/SenseHat_Guide.md**)

## Materials
- Raspberry Pi with Sense HAT
- Python 3 and the `sense_hat` module

## Steps
1. Create `weather_monitor.py` from the template below.
2. Run `python3 weather_monitor.py`.
3. Watch the scrolling display; Ctrl‑C to stop.

## Starter code

```python
from sense_hat import SenseHat
import time

DELAY = 3  # seconds between readings
sense = SenseHat()

def read_sensors():
    temp_c = sense.get_temperature()
    humidity = sense.get_humidity()
    return round(temp_c, 1), round(humidity, 1)

def main():
    while True:
        temp, hum = read_sensors()
        message = f"T:{temp}°C H:{hum}%"
        sense.show_message(message, scroll_speed=0.05, text_colour=[0, 255, 0])
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
```

## Stretch goals
- Auto‑switch °C/°F with a Sense HAT joystick press.
- Change LED colour based on humidity range.
