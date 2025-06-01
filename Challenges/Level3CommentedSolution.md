# 🧠 Teaching Sample Solution: Level 3 Sense HAT Challenge

This version includes comments to help students understand the purpose of each section.

```python
from sense_hat import SenseHat
import time

# Create a SenseHat object
sense = SenseHat()

# Function to display a welcome message
def show_welcome():
    sense.show_message("Welcome!", text_colour=[0, 255, 0])

# Function to show temperature
def show_temperature():
    temp = sense.get_temperature()
    sense.show_message(f"Temp: {temp:.1f}C", text_colour=[255, 0, 0])

# Function to show humidity
def show_humidity():
    humidity = sense.get_humidity()
    sense.show_message(f"Humidity: {humidity:.1f}%", text_colour=[0, 0, 255])

# Function to show pressure
def show_pressure():
    pressure = sense.get_pressure()
    sense.show_message(f"Pressure: {pressure:.1f} hPa", text_colour=[255, 255, 0])

# Start by greeting the user
show_welcome()

# Main loop
running = True
while running:
    for event in sense.stick.get_events():
        # Only respond to button press
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
    time.sleep(0.1)  # Pause slightly to avoid overloading CPU
```

### 🧾 What Students Learn:
- Modular code with functions
- Sense HAT joystick as input
- Sensor output using LED display
- Program flow control with loops and conditionals

---

[Back to Level 3 Challenge](Level3Challenge.md)
