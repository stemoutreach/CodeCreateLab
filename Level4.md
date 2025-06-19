
# Level 4 Pico – Breadboarding Basics: Learn by Recipe

## 🧠 Learning Objectives

- Learn how to use GPIO pins through real-world projects
- Understand how inputs (buttons/sensors) and outputs (LEDs) work together
- Configure Thonny to use the MicroPython interpreter on the Pico.
- Run a script that blinks the onboard LED.
- Explore and modify recipes from the official [PICOZero](https://picozero.readthedocs.io/en/latest/gettingstarted.html)

## 🧰 Materials Needed

- Raspberry Pi Pico
- Breadboard and jumper wires
- LEDs (2–3) and resistors (220–330Ω)
- Push button
- (Optional) sensors like TMP36 or light sensor

---

## 🔌 Intro to GPIO & Breadboards

GPIO stands for General Purpose Input/Output. These are the physical pins on your Raspberry Pi that can be used to control electronic components like LEDs, buttons, and sensors.

Breadboards are tools for prototyping electronic circuits without soldering. They allow you to easily connect components together using jumper wires.

   Inside a breadboard

   <img src="https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Insidebread.jpg" width="400" >

### Key Concepts:
- GPIO pins can send or receive signals
- Breadboards help you organize and test circuits
- Use resistors to protect LEDs from too much current
- Each GPIO pin has a number — use the [PICO GPIO Pinout Guide](https://picozero.readthedocs.io/en/latest/recipes.html#pin-out)


## Connect & Configure Thonny

1. Plug the Pico into the Pi 500 using the USB cable (no BOOTSEL needed).  
2. Open **Thonny** → *Tools ▸ Options ▸ Interpreter*.  
3. Select **Interpreter** = **MicroPython (Raspberry Pi Pico)**, **Port** = *Automatic* (or `/dev/ttyACM0`).  
4. Click **OK**. The Shell should show the `>>>` MicroPython prompt.

---

### 🚦 Blink the On‑Board LED

```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```

Press ▶️ Run. The small **green LED near the antenna** blinks five times.

## 4 · Blink an LED

1. Plug in the LED to the breadboard - long lead to GPIO 14, short lead to ground (GPIO 13)
2. Load the below
3. Press ▶️ Run.
   
<img src="https://github.com/stemoutreach/PicoBot/blob/main/zzimages/LEDOnOff.jpg" width="500" >   


```python
from picozero import LED
from time import sleep

led = LED(14)

led.on()
sleep(1)
led.off()

```
Try additional LED function 
https://picozero.readthedocs.io/en/latest/recipes.html#leds

---

## 🧭 Explore GPIOZero Recipes

Visit: [PICOZero Recipes](https://picozero.readthedocs.io/en/latest/recipes.html#)  
Start exploring how to blink an LED, use a button, and interact with sensors. Below are a few recommended recipes to try.

- LEDs
- Buttons
- RGB LEDs
- Buzzer
- Speaker
- Internal temperature sensor
- Ultrasonic distance sensor

  PicoZero does not have many pictures to show how to wire the pico and breadboard. [GPIOZero](https://gpiozero.readthedocs.io/en/stable/recipes.html) may have some images that can be used. 

---

## ✅ Level Checkpoint

To pass this level, show:
- Demonstrate a Working Reaction Game 
- You modified a recipe in some way (change pins, timing, behavior)
- Create your own project using combination of sensor, LEDs, motors etc...

---

## 🧠 Reflect & Share

- What did you change or experiment with?
- Did you encounter an error? How did you figure it out?
- What’s one idea you’d like to try next?

---

