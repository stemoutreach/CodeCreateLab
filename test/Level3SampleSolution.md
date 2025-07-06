# 💡 Sample Solution: Level 3 Sense HAT Challenge

Here's one way to solve the Level 3 challenge using functions, loops, conditionals, and Sense HAT I/O.

```python
from sense_hat import SenseHat
import time

sense = SenseHat()

def show_welcome():
    sense.show_message("Welcome!", text_colour=[0, 255, 0])

def show_temperature():
    temp = sense.get_temperature()
    sense.show_message(f"Temp: {temp:.1f}C", text_colour=[255, 0, 0])

def show_humidity():
    humidity = sense.get_humidity()
    sense.show_message(f"Humidity: {humidity:.1f}%", text_colour=[0, 0, 255])

def show_pressure():
    pressure = sense.get_pressure()
    sense.show_message(f"Pressure: {pressure:.1f} hPa", text_colour=[255, 255, 0])

# Start the program
show_welcome()

running = True

while running:
    for event in sense.stick.get_events():
        if event.action == 'pressed':
            if event.direction == 'up':
                show_temperature()
            elif event.direction == 'down':
                show_humidity()
            elif event.direction == 'right':
                show_pressure()
            elif event.direction == 'middle':
                sense.show_message("Goodbye!", text_colour=[255, 255, 255])
                running = False
    time.sleep(0.1)  # slight delay to avoid high CPU usage
```

---

### 💭 Notes:
- Uses **functions** to modularize code.
- Uses a **`while` loop** to keep the program running.
- Uses **Sense HAT joystick** for input and **LED matrix** for output.
- Includes **sensor data** reading and user-friendly display.

Encourage students to **personalize** the output, try different colors, or add more features!

---

[Back to Level 3 Challenge](Level3Challenge.md)
