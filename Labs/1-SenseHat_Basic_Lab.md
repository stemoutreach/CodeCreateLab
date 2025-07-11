# 1 Sense Hat Basic Lab: Weather Warning Light

Your Pi rover needs a **Weather Warning Light**.  
Use the Sense HAT to read the *temperature* and *humidity* every few seconds.  
If it gets **too hot** **OR** **too dry**, the LED matrix must flash **red**; otherwise stay **green**.

## Learning Goals
* Use **`input()`** to collect information from the user.
* Display messages with **`print()`**.
* Make decisions with **`if / else`**.
* Organise code into **functions**.

---

## Your Mission
1. **Ask** the engineer (that’s you!) for:
   * a *high‑temperature* limit in °C  
   * a *low‑humidity* limit in %
2. **Read** the current temperature & humidity from the Sense HAT.
3. **Print** the readings to the terminal.
4. **Decide**  
   * If the temperature is higher than the limit **OR** the humidity is lower, turn the LEDs **red** and print a warning.  
   * Otherwise turn them **green** and print “Environment OK”.
5. Keep checking every 2 seconds until *Ctrl +C* is pressed.

---

## Starter Code  

```python
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

def get_readings():
    """TODO: Return the current temperature and humidity."""
    # Write code here…
    pass  # TODO

def show_status(temp, hum, temp_limit, hum_limit):
    """TODO: Decide LED colour & print messages."""
    # Write code here…
    pass  # TODO

# ─── Main Program ──────────────────────────────────────────────── #

print("Sense HAT Weather Warning Light")

# TODO: Ask the user for the two limits using input()
temp_limit = ...   # replace with your code
hum_limit  = ...

try:
    while True:
        # TODO: Read sensors and show the status
        time.sleep(2)
except KeyboardInterrupt:
    sense.clear()
    print("Program stopped. Stay safe!")
```

### Hints  
* `sense.get_temperature()` and `sense.get_humidity()` return float numbers.  
* Use **`round(value, 1)`** to show one decimal place.  
* `sense.clear(r, g, b)` sets the whole display to a colour.

---

## 📑Optional Advanced Lab
[1.5 Sense HAT Advanced Lab: Mission Dashboard](1.5-SenseHat_Advance_Lab.md) 


---

**Have fun coding! When you’re done, compare with the solution file.**
