
# 2 Pico Breadboarding Basics: Learn by Recipe

## 🧠 Learning Objectives
- Understand how to use GPIO pins with the Raspberry Pi Pico
- Learn how inputs (buttons/sensors) and outputs (LEDs) work together
- Configure Thonny to use MicroPython on the Pico
- Run basic scripts including blinking LEDs
- Explore and modify projects using [PicoZero Recipes](https://picozero.readthedocs.io/en/latest/gettingstarted.html)

---

## 🧰 Materials Needed
- Raspberry Pi Pico
- Breadboard and jumper wires
- LEDs (2–3) and resistors (220–330Ω)
- Push button
- (Optional) Sensor like TMP36 or light sensor

---

## 🔌 Intro to GPIO & Breadboards
**GPIO** stands for *General Purpose Input/Output*. These pins allow your Pico to send or receive signals, enabling control over LEDs, buttons, motors, sensors, etc.

**Breadboards** are tools for prototyping circuits without soldering. They make it easy to test and modify electronic setups.

**Inside a Breadboard**:

![Inside Breadboard](https://github.com/stemoutreach/CodeCreateLab/blob/main/zimages/Insidebread.jpg)

### Key Concepts
- GPIO pins can be configured as input or output
- Breadboards help organize and test circuits
- Resistors protect LEDs from too much current
- Each GPIO pin is numbered — reference the [Pico GPIO Pinout Guide](https://picozero.readthedocs.io/en/latest/recipes.html#pin-out)

---

## 🛠️ Configure Thonny for the Pico
1. Connect the Pico to your computer using a micro USB cable (no BOOTSEL button required).
2. Open **Thonny IDE** → Go to **Tools ▸ Options ▸ Interpreter**.
3. Set:
   - **Interpreter** = *MicroPython (Raspberry Pi Pico)*
   - **Port** = *Automatic* (or `/dev/ttyACM0` on Linux)
4. Click **OK**. You should see a `>>>` MicroPython prompt in the Shell.

---

## 🚦 Blink the Onboard LED
```python
from picozero import pico_led
from time import sleep

while True:
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
```
> Press ▶️ Run. The **green LED near the antenna** will blink repeatedly.

---

## 💡 Blink an External LED
### Wiring:
- Long lead of LED → GPIO 14
- Short lead → resistor → GND (e.g., GPIO 13 ground pin)

### Code:
```python
from picozero import LED
from time import sleep

led = LED(14)

led.on()
sleep(1)
led.off()
```

![LED Wiring Example](https://github.com/stemoutreach/PicoBot/blob/main/zzimages/LEDOnOff.jpg)

---

## 🧭 Explore PicoZero Recipes
Visit [PicoZero Recipes](https://picozero.readthedocs.io/en/latest/recipes.html) to explore:
- Blinking and fading LEDs
- Buttons and user input
- RGB LEDs
- Buzzers and speakers
- Ultrasonic distance sensors

> Note: PicoZero documentation doesn’t always show wiring pictures. You may refer to [GPIOZero Recipes](https://gpiozero.readthedocs.io/en/stable/recipes.html) for circuit examples.

---

## ✅ Level Checkpoint
To complete Level 4, show:
- ✅ A working **Reaction Game** based on [GPIOZero’s Reaction Game](https://gpiozero.readthedocs.io/en/stable/recipes.html#reaction-game)
- ✅ A modification of an existing recipe (e.g., different pins, changed delay)
- ✅ A self-designed project using a mix of LEDs, buttons, or sensors

---

## 🧠 Reflect & Share
- What changes or experiments did you try?
- What errors or challenges did you face?
- What’s one idea or project you’d like to attempt next?

---

Next [Level 5 – PicoBot:1 2-Wheel Driving](Level5.md)
