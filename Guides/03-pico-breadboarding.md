# Raspberry Pi Pico Breadboarding

> ### Quick info
> **Level:** 03 • **Time:** 45–75 min  
> **Prereqs:** Guides: [Python Basics](../Guides/00-python-basics.md) & [Python Functions](../Guides/01-python-functions.md)  
> **Hardware:** Raspberry Pi Pico + micro‑USB cable; Breadboard, jumper wires, LEDs, pushbutton  
> **You’ll practice:**
> - Configure Thonny for MicroPython on the Pico
> - Explain breadboard layout and use resistors safely
> - Use picozero to control onboard/external LEDs
> - Read inputs from a pushbutton
> - Explore and adapt PicoZero recipes (RGB LED, ultrasonic sensor, etc.)

# Why This Matters
This guide gets your **Raspberry Pi Pico** ready for **hands‑on electronics**. You’ll set up MicroPython in Thonny, learn breadboard basics, blink LEDs (onboard and external), read a button, and explore PicoZero recipes—preparing you for the **Pico Breadboard Lab**.

## What you’ll learn
- How breadboards are wired internally (power rails and rows)
- GPIO basics: inputs vs. outputs, pin numbering
- MicroPython with Thonny + the `picozero` library
- Wiring and coding LEDs and buttons
- Where to find and adapt PicoZero recipes

## Materials
- Raspberry Pi Pico (not W required, either is fine)
- Breadboard, jumper wires
- 2–3 LEDs and **220–330Ω** resistors
- 1 pushbutton
- (Optional) RGB LED, ultrasonic distance sensor (HC‑SR04), TMP36 or light sensor

## Intro to GPIO & Breadboards
**GPIO** stands for *General Purpose Input/Output*. These pins allow your Pico to send or receive signals, enabling control over LEDs, buttons, motors, sensors, etc.

**Breadboards** are tools for prototyping circuits without soldering. They make it easy to test and modify electronic setups.

**Inside a Breadboard**:

<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/Insidebread.jpg" width="400" >

### Key Concepts
- GPIO pins can be configured as input or output
- Breadboards help organize and test circuits
- Each GPIO pin is numbered — reference the [Pico GPIO Pinout Guide](https://picozero.readthedocs.io/en/latest/recipes.html#pin-out)

## Setup
1. **Connect the Pico** to your computer with micro‑USB.
2. Open **Thonny** → **Tools ▸ Options ▸ Interpreter**.
   - Interpreter: **MicroPython (Raspberry Pi Pico)**
   - Port: **Automatic**
3. In the Thonny **Shell**, you should see the `>>>` MicroPython prompt.

## Walkthrough

### 1) Blink the onboard LED
```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```
> Press **Run**. The small onboard LED should blink.

### 2) Blink an external LED
**Wiring**
- Long leg (anode) → **GPIO 14**
- Short leg (cathode) → **resistor** → **GND**

**Code**
```python
from picozero import LED
from time import sleep

led = LED(14)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

<img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/BlinkLED1.jpeg" width="400" >   <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/BlinkLED2.jpeg" width="400" > 

### 3) Read a pushbutton
**Wiring**
- One side of button → **GPIO 15**
- Opposite side → **GND**

**Code**
```python
from picozero import Button, LED
from time import sleep

button = Button(15)   # internal pull-up handled by library
led = LED(14)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
    sleep(0.02)  # simple debounce
```
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReadpushbuttonOn.jpeg" width="500" > <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReadpushbuttonOFF.jpeg" width="450" >  

## Try it: Mini‑exercise (Reaction Game)
- See example here - [PicoZero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html#reaction-game) 
- LED turns off after a random delay (0.5–3 s).  
- When it lights up, press the button **as fast as you can**.  
- Print the reaction time in milliseconds.  
> Stretch: Keep best‑of‑3 score; add a penalty if the button is pressed too early.

**Code**
```python
from picozero import Button, LED
from time import sleep
import random

led = LED(14)

player_1 = Button(15)
player_2 = Button(17)

time = random.uniform(5, 10)
sleep(time)
led.on()

while True:
    if player_1.is_pressed:
        print("Player 1 wins!")
        break
    if player_2.is_pressed:
        print("Player 2 wins!")
        break

led.off()
```
 <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/assets/ReactionGame.jpeg" width="500" > 


### 4) Explore PicoZero recipes (pick 1–2 to try)
Visit [PicoZero Recipes](https://picozero.readthedocs.io/en/latest/recipes.html) to explore:
- RGB LED (set colors with `(r,g,b)`)
- Ultrasonic distance sensor (measure cm)
- Buzzer tones
> Start from examples in the PicoZero docs and modify pins to match your wiring.

## Check your understanding
2. What’s the difference between **GPIO input** and **output**?
3. How are breadboard rows/rails connected internally?

## Troubleshooting
- **LED doesn’t light** → Check LED orientation, resistor, and pin number. Try `led.blink()` to test.
- **Button always “pressed”** → Verify wiring across the **opposite** legs of the switch; ensure one side goes to **GND**.
- **No `picozero` module** → Update Thonny/MicroPython; ensure you’re running on the **Pico**, not your computer’s Python.
- **Nothing runs** → Confirm **Interpreter** in Thonny is set to **MicroPython (Raspberry Pi Pico)** and you see `>>>`.

## Next up
Do the matching lab: **[03 – Pico Breadboard Lab](../Labs/03-pico-breadboard-lab.md)**

