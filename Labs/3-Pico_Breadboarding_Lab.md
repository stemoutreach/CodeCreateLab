
# 3 – Raspberry Pi Pico Breadboarding

## Overview  
In this lab, you’ll build an interactive breadboard circuit using a Raspberry Pi Pico. Your design will include required components to start a distance-measuring system and provide visual feedback, along with optional enhancements to make it your own.

You’ll write code that activates on a button press, reads from an ultrasonic distance sensor, and displays the result in inches. Visual cues will be given through an RGB LED. You’re encouraged to explore and personalize your project using the optional components.

---

## Learning Objectives  
By completing this lab, you will:

- Use a button with pull-down resistor as a digital input.
- Control a standard LED and RGB LED using digital and PWM outputs.
- Measure distance using the HC-SR04 ultrasonic sensor and convert to inches.
- Display distance using both code output and RGB LED feedback.
- Organize code using MicroPython functions and logic blocks.
- (Optional) Add enhancements using additional components.

---

## Prerequisites  
Complete the following
- [Python Guide](/Guides/0-Python_Guide.md)
- [Sense HAT Guide](Guides/1-SenseHat_Guide.md)
- [Pico Breadboarding Guide](/Guides/2-Pico_Breadboarding_Guide.md)

---

## Hardware Requirements

### 🧩 Required Components  
- **Push-button** – used to initiate a distance reading.  
- **Ultrasonic Distance Sensor (HC-SR04)** – measure distance to nearby objects.  
- **RGB LED** – provides color-based feedback tied to distance.  
  - Example: red = close, green = far, blue = medium range.

### 💡 Optional Components (Add Your Creative Touch!)  
- **Piezo Buzzer** – give audio feedback based on proximity.  
- **Single-Color LEDs with variable brightness** – use PWM for effects like fading or traffic light logic.  
- **Traffic Light LED Module** – simulate stoplight behavior depending on distance.  
- **LED Matrix or LED Board** – display animations or bar graphs based on distance.

---

## Circuit Diagram  

See [PicoZero Recipes](https://picozero.readthedocs.io/en/latest/recipes.html) 

NOTE: PicoZero documentation doesn’t always show wiring pictures. You may refer to [GPIOZero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html) for circuit examples.

---

## Starter Code (with TODOs)

```python
# TODO: Import necessary modules

# TODO: Define pins for TRIG, ECHO, BUTTON, and RGB (use PWM for RGB)

# TODO: Define constant for SPEED_CM_PER_US

# TODO: Define set_rgb() function
# - Set frequency for each color channel
# - Convert RGB values (0–255) to duty cycle (0–65535)

# TODO: Define read_distance_inches() function
# - Trigger ultrasonic pulse
# - Measure pulse duration
# - Convert to distance in inches

# TODO: Main loop
# - If button is pressed:
#   - Read distance
#   - Print distance in inches
#   - Set RGB LED color based on range (e.g., red < 8", blue < 16", green otherwise)
# - Add optional features here (buzzer, LEDs, etc.)
```

---

## Challenges & Stretch Goals  

🛠 **Basic Challenge**  
- Complete the required circuit and code.
- Make sure RGB color changes based on distance.

🎯 **Stretch Goals (Optional)**  
- Use the buzzer to beep faster as objects get closer.
- Fade LED brightness based on distance.
- Create a traffic light behavior: green (safe), yellow (caution), red (too close).
- Use an LED board to show distance as a visual meter.
- Add a second button to reset or change modes.
