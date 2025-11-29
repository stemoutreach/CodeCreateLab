# picobot_wiring_test.py
#
# Quick wiring test for PicoBot standard pin map:
# - L298N motors (A=Left, B=Right)
# - HC-SR04P ultrasonic
# - Button
# - RGB LED
# - Speaker / buzzer
#
# Run this on your Pico (as main.py or from Thonny).
# Watch the robot and the Thonny Shell for messages.

from machine import Pin, PWM
from time import sleep

try:
    from picozero import DistanceSensor, Speaker
    HAVE_PICOZERO = True
except ImportError:
    HAVE_PICOZERO = False
    print("⚠ picozero not found – ultrasonic & speaker tests will be skipped")

# === PicoBot Standard Pin Map ===
# Motors (L298N) - Motor A = Left, Motor B = Right

ENB_PIN = 2   # Right enable (Motor B, PWM)
IN4_PIN = 3   # Right IN4 (Motor B OUT4)
IN3_PIN = 4   # Right IN3 (Motor B OUT3)

IN1_PIN = 6   # Left IN1  (Motor A OUT1)
IN2_PIN = 7   # Left IN2  (Motor A OUT2)
ENA_PIN = 8   # Left enable (Motor A, PWM)

# Ultrasonic (HC-SR04P)
ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

# Inputs / Outputs
BUTTON_PIN = 16

RGB_R_PIN = 17
RGB_G_PIN = 18
RGB_B_PIN = 19

SPEAKER_PIN = 20

# === Motor setup ===
IN1 = Pin(IN1_PIN, Pin.OUT)
IN2 = Pin(IN2_PIN, Pin.OUT)
IN3 = Pin(IN3_PIN, Pin.OUT)
IN4 = Pin(IN4_PIN, Pin.OUT)

ENA = PWM(Pin(ENA_PIN))
ENB = PWM(Pin(ENB_PIN))

PWM_FREQ = 1000
PWM_SPEED = 45000  # 0-65535, ~70% power

ENA.freq(PWM_FREQ)
ENB.freq(PWM_FREQ)


def all_motor_pins_low():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


def stop_motors():
    ENA.duty_u16(0)
    ENB.duty_u16(0)
    all_motor_pins_low()


def left_forward():
    # Left only, forward
    ENA.duty_u16(PWM_SPEED)
    ENB.duty_u16(0)
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


def left_back():
    ENA.duty_u16(PWM_SPEED)
    ENB.duty_u16(0)
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(0)


def right_forward():
    ENA.duty_u16(0)
    ENB.duty_u16(PWM_SPEED)
    IN1.value(0)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def right_back():
    ENA.duty_u16(0)
    ENB.duty_u16(PWM_SPEED)
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)


# === RGB LED & button ===
rgb_r = Pin(RGB_R_PIN, Pin.OUT)
rgb_g = Pin(RGB_G_PIN, Pin.OUT)
rgb_b = Pin(RGB_B_PIN, Pin.OUT)

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

# === Ultrasonic & speaker (using picozero if available) ===
if HAVE_PICOZERO:
    sensor = DistanceSensor(echo=ULTRA_ECHO_PIN, trigger=ULTRA_TRIG_PIN)
    speaker = Speaker(SPEAKER_PIN)


def test_motors():
    print("\n=== MOTOR TEST ===")
    print("1) Left motor FORWARD (Motor A). Wheels should spin forward on the LEFT.")
    left_forward()
    sleep(1.5)

    print("2) Left motor BACKWARD (Motor A). Wheels should spin backward on the LEFT.")
    left_back()
    sleep(1.5)

    print("3) Right motor FORWARD (Motor B). Wheels should spin forward on the RIGHT.")
    right_forward()
    sleep(1.5)

    print("4) Right motor BACKWARD (Motor B). Wheels should spin backward on the RIGHT.")
    right_back()
    sleep(1.5)

    stop_motors()
    print("Motor test done.\n")


def set_rgb(r, g, b):
    rgb_r.value(1 if r else 0)
    rgb_g.value(1 if g else 0)
    rgb_b.value(1 if b else 0)


def test_rgb():
    print("\n=== RGB LED TEST ===")
    print("Red on...")
    set_rgb(1, 0, 0)
    sleep(1.0)

    print("Green on...")
    set_rgb(0, 1, 0)
    sleep(1.0)

    print("Blue on...")
    set_rgb(0, 0, 1)
    sleep(1.0)

    print("White (R+G+B)...")
    set_rgb(1, 1, 1)
    sleep(1.0)

    print("Off.")
    set_rgb(0, 0, 0)
    print("RGB LED test done.\n")


def test_button(duration_sec=8):
    print("\n=== BUTTON TEST ===")
    print("Press and release the button several times (GP16).")
    print(f"Watching for about {duration_sec} seconds...")

    last_state = button.value()
    print("Initial state:", "PRESSED" if last_state else "released")

    start = 0
    # crude timing loop (we'll just iterate ~duration_sec * 10 times with sleep(0.1))
    loops = int(duration_sec * 10)
    for _ in range(loops):
        state = button.value()
        if state != last_state:
            if state:
                print("Button PRESSED")
            else:
                print("Button released")
            last_state = state
        sleep(0.1)

    print("Button test done.\n")


def test_speaker():
    if not HAVE_PICOZERO:
        print("\n=== SPEAKER TEST SKIPPED (picozero not installed) ===")
        return

    print("\n=== SPEAKER TEST ===")
    print("You should hear three short beeps...")
    speaker.beep(on_time=0.15, off_time=0.15, n=3)
    sleep(1)
    print("Speaker test done.\n")


def test_ultrasonic():
    if not HAVE_PICOZERO:
        print("\n=== ULTRASONIC TEST SKIPPED (picozero not installed) ===")
        return

    print("\n=== ULTRASONIC TEST (HC-SR04P) ===")
    print("Hold your hand ~10–50 cm in front of the sensor.")
    print("Reading distance 10 times...")

    for i in range(10):
        d_m = sensor.distance  # in meters
        d_cm = d_m * 100
        print("Reading", i + 1, ":", "{:.1f} cm".format(d_cm))
        sleep(0.5)

    print("Ultrasonic test done.\n")


# === MAIN ===

print("====================================")
print(" PicoBot Wiring Test")
print(" Standard pin map: motors, RGB, button, ultrasonic, speaker")
print(" Make sure the wheels are off the table for motor tests!")
print("====================================")
sleep(3)

stop_motors()
set_rgb(0, 0, 0)

try:
    test_motors()
    test_rgb()
    test_speaker()
    test_button()
    test_ultrasonic()
finally:
    # Safety: make sure everything is off at the end
    stop_motors()
    set_rgb(0, 0, 0)
    if HAVE_PICOZERO:
        speaker.off()

print("All wiring tests complete.")
