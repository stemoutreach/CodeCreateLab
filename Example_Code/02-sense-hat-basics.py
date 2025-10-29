
"""Sense HAT Basics — Weather Warning Light (Starter)"""
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def get_readings():
    t = sense.get_temperature()
    h = sense.get_humidity()
    return round(t, 1), round(h, 1)

def show_status(temp, hum, t_limit, h_limit):
    too_hot = temp > t_limit
    too_dry = hum < h_limit
    if too_hot or too_dry:
        sense.clear(255, 0, 0)
        print(f"WARNING: T={temp}°C  H={hum}%  (limits: {t_limit}°C / {h_limit}%)")
    else:
        sense.clear(0, 255, 0)
        print(f"OK: T={temp}°C  H={hum}%")

if __name__ == "__main__":
    print("Sense HAT — Weather Warning Light")    
    try:
        t_limit = float(input("High temperature limit (°C)? ").strip())
        h_limit = float(input("Low humidity limit (%)? ").strip())
    except ValueError:
        print("Please enter numbers (e.g., 28 and 30). Exiting.")
        raise SystemExit(1)

    try:
        while True:
            temp, hum = get_readings()
            show_status(temp, hum, t_limit, h_limit)
            time.sleep(2)
    except KeyboardInterrupt:
        sense.clear()
        print("\nGoodbye!")
