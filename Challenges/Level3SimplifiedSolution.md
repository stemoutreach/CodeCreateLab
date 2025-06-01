# 🌱 Simplified Sample Solution: Level 3 Sense HAT Challenge

This version uses fewer functions and simpler structure, great for beginners just starting to understand input and output.

```python
from sense_hat import SenseHat
import time

sense = SenseHat()

sense.show_message("Welcome!", text_colour=[0, 255, 0])

while True:
    for event in sense.stick.get_events():
        if event.action == 'pressed':
            if event.direction == 'up':
                temp = sense.get_temperature()
                sense.show_message(f"{temp:.1f} C", text_colour=[255, 0, 0])
            elif event.direction == 'down':
                humidity = sense.get_humidity()
                sense.show_message(f"{humidity:.1f} %", text_colour=[0, 0, 255])
            elif event.direction == 'middle':
                sense.show_message("Bye!", text_colour=[255, 255, 255])
                break
    time.sleep(0.1)
```

### ✅ Key Concepts:
- Uses `while` loop and joystick input
- Displays sensor values on LED
- Exits when the middle button is pressed

---

[Back to Level 3 Challenge](Level3Challenge.md)
