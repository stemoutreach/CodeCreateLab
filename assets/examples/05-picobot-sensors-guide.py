"""
05_picobot_sensors_mentor_solution.py

Mentor reference solution for:
05-picobot-sensors-guide.md

This version combines:
- Motors (L298N driver)
- Ultrasonic distance sensor (HC-SR04P)
- RGB LED
- Pushbutton
- Speaker (buzzer)

Pins (per latest mapping):
    Enable B   ENB  -> GP2
    Motor B    IN4  -> GP3
    Motor B    IN3  -> GP4
    Motor A    IN1  -> GP6
    Motor A    IN2  -> GP7
    Enable A   ENA  -> GP8
"""

from machine import Pin, PWM
from picozero import DistanceSensor, RGBLED, Speaker, Button
from time import sleep

# ======================================================
# MOTOR SETUP  (L298N)
# ======================================================

# Pin mapping for motors
ENB_PIN = 2   # Enable B (right side, for example)
IN4_PIN = 3   # Motor B IN4
IN3_PIN = 4   # Motor B IN3

IN1_PIN = 6   # Motor A IN1
IN2_PIN = 7   # Motor A IN2
ENA_PIN = 8   # Enable A (left side)

# PWM setup for speed control
ENB = PWM(Pin(ENB_PIN))
ENA = PWM(Pin(ENA_PIN))
ENB.freq(1000)
ENA.freq(1000)

# Direction pins
IN4 = Pin(IN4_PIN, Pin.OUT)
IN3 = Pin(IN3_PIN, Pin.OUT)
IN1 = Pin(IN1_PIN, Pin.OUT)
IN2 = Pin(IN2_PIN, Pin.OUT)

def _set_speed(left: float, right: float):
    """
    Set motor speeds as values between 0.0 and 1.0.
    0.0 = stop, 1.0 = full speed.
    """
    left = max(0.0, min(1.0, left))
    right = max(0.0, min(1.0, right))

    ENA.duty_u16(int(left * 65535))
    ENB.duty_u16(int(right * 65535))

def motor_stop():
    """Stop both motors."""
    _set_speed(0, 0)
    IN1.low(); IN2.low()
    IN3.low(); IN4.low()

def forward(speed: float = 0.6):
    """Drive forward at given speed (0.0–1.0)."""
    # Left motor forward
    IN1.high()
    IN2.low()
    # Right motor forward
    IN3.high()
    IN4.low()

    _set_speed(speed, speed)

def backward(speed: float = 0.6):
    """Drive backward at given speed (0.0–1.0)."""
    # Left motor backward
    IN1.low()
    IN2.high()
    # Right motor backward
    IN3.low()
    IN4.high()

    _set_speed(speed, speed)

def turn_left(speed: float = 0.6):
    """Turn left in place."""
    # Left motor backward
    IN1.low()
    IN2.high()
    # Right motor forward
    IN3.high()
    IN4.low()

    _set_speed(speed, speed)

def turn_right(speed: float = 0.6):
    """Turn right in place."""
    # Left motor forward
    IN1.high()
    IN2.low()
    # Right motor backward
    IN3.low()
    IN4.high()

    _set_speed(speed, speed)


# ======================================================
# SENSORS + OUTPUTS (picozero)
# ======================================================

# Ultrasonic distance sensor (HC-SR04P)
ULTRASONIC_TRIGGER = 16  # GP16
ULTRASONIC_ECHO = 17     # GP17

distance_sensor = DistanceSensor(
    trigger=ULTRASONIC_TRIGGER,
    echo=ULTRASONIC_ECHO,
    max_distance=2.0  # meters (~200 cm)
)

# RGB LED (common cathode)
RGB_RED_PIN = 18         # GP18
RGB_GREEN_PIN = 19       # GP19
RGB_BLUE_PIN = 20        # GP20
status_led = RGBLED(RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN)

# Speaker (buzzer)
SPEAKER_PIN = 21
speaker = Speaker(SPEAKER_PIN)

# Pushbutton
BUTTON_PIN = 22
button = Button(BUTTON_PIN, pull_up=True)


# ======================================================
# HELPER FUNCTIONS
# ======================================================

def all_off():
    """Turn off LED, speaker, and motors."""
    status_led.off()
    speaker.off()
    motor_stop()

def startup_sequence():
    """Quick LED + sound sequence to show the robot is ready."""
    # LED color cycle
    status_led.color = (1, 0, 0); sleep(0.2)  # Red
    status_led.color = (0, 1, 0); sleep(0.2)  # Green
    status_led.color = (0, 0, 1); sleep(0.2)  # Blue
    status_led.color = (1, 1, 1); sleep(0.2)  # White
    status_led.off()

    # Simple "ready" beep-beep
    speaker.on(); sleep(0.15); speaker.off()
    sleep(0.1)
    speaker.on(); sleep(0.25); speaker.off()

def set_idle_state():
    """LED shows dim blue, motors and sound off in IDLE mode."""
    status_led.color = (0.0, 0.0, 0.1)  # dim blue
    speaker.off()
    motor_stop()

def get_distance_cm():
    """Read distance in centimeters (from meters)."""
    return distance_sensor.distance * 100.0

def update_feedback_for_distance(distance_cm):
    """
    LED + beep feedback based on distance.
    Driving behavior is handled separately in main().
    """
    if distance_cm < 0:
        # Sensor glitch or reading error
        status_led.color = (1, 0, 1)  # magenta = error
        speaker.off()
        return

    if distance_cm < 10:
        # Very close: RED + rapid beeps
        status_led.color = (1, 0, 0)
        speaker.on(); sleep(0.05); speaker.off()
    elif distance_cm < 30:
        # Medium distance: YELLOW + slower beep
        status_led.color = (1, 0.6, 0)
        speaker.on(); sleep(0.1); speaker.off()
    else:
        # Far: GREEN, no beep
        status_led.color = (0, 1, 0)
        speaker.off()


# ======================================================
# MAIN LOOP
# ======================================================

def main():
    """
    Main control loop.

    - Button toggles between IDLE and ACTIVE modes.
    - In ACTIVE mode:
        * Robot drives forward while path is clear.
        * If an obstacle is too close, robot stops and warns.
    """
    print("Starting PicoBot sensors + driving mentor solution...")
    startup_sequence()

    active = False
    set_idle_state()

    try:
        while True:
            # Toggle between IDLE and ACTIVE when button is pressed
            if button.was_pressed:
                active = not active
