from picozero import LED, Button, RGBLED, DistanceSensor, Speaker
from time import sleep

# 03 — Pico Smart Distance Station
# Completed reference solution for coaches/teachers.
# Students should work from the lab Skeleton Starter and STUDENT_START.md.

# --- Pin setup (matches the lab instructions) ---
STATUS_LED_PIN = 14
BUTTON_PIN = 13
RGB_RED_PIN = 16
RGB_GREEN_PIN = 17
RGB_BLUE_PIN = 18
ULTRASONIC_ECHO_PIN = 2
ULTRASONIC_TRIG_PIN = 3
SPEAKER_PIN = 20

# --- Distance thresholds (in cm) ---
CLOSE_CM = 20.0
MEDIUM_CM = 40.0

# --- Objects ---
status_led = LED(STATUS_LED_PIN)
button = Button(BUTTON_PIN)
rgb = RGBLED(red=RGB_RED_PIN, green=RGB_GREEN_PIN, blue=RGB_BLUE_PIN)
sensor = DistanceSensor(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIG_PIN)
speaker = Speaker(SPEAKER_PIN)

# Simple mode variable: "idle" or "active"
mode = "idle"

# Track previous button state for edge detection
prev_pressed = False


def read_distance_cm():
    """Return the distance in centimeters (float)."""
    d_m = sensor.distance        # distance in meters
    d_cm = d_m * 100
    return d_cm


def update_lights(distance_cm):
    """
    Set status_led and rgb color based on:
      - mode (idle vs active)
      - distance_cm (far / medium / close)
    """
    global mode

    if mode == "idle":
        status_led.off()
        rgb.off()
        return

    # mode == "active"
    status_led.on()

    if distance_cm is None:
        # If we somehow get here without a distance, just turn RGB off
        rgb.off()
        return

    # Choose colors for distance ranges
    if distance_cm < CLOSE_CM:
        # Too close: red
        rgb.color = (1.0, 0.0, 0.0)
    elif distance_cm < MEDIUM_CM:
        # Medium range: yellow (red + green)
        rgb.color = (1.0, 1.0, 0.0)
    else:
        # Far: green
        rgb.color = (0.0, 1.0, 0.0)


def update_sound(distance_cm, loop_count):
    """
    Decide when/how the speaker should beep.

    Pattern:
      - idle: speaker.off()
      - far:  silent
      - medium: short beep every few loops
      - close: faster short beep each loop
    """
    global mode

    if mode == "idle" or distance_cm is None:
        speaker.off()
        return

    # Far: silent
    if distance_cm >= MEDIUM_CM:
        speaker.off()
        return

    # Medium: occasional beep (every 5th loop)
    if CLOSE_CM <= distance_cm < MEDIUM_CM:
        if loop_count % 5 == 0:
            speaker.beep(on_time=0.05, off_time=0.05, n=1)
        else:
            speaker.off()
        return

    # Close: frequent beeps (every loop)
    if distance_cm < CLOSE_CM:
        speaker.beep(on_time=0.05, off_time=0.05, n=1)
        return


def handle_button():
    """
    Flip mode when the button is pressed (edge-triggered).

    We toggle when the state changes from "not pressed" to "pressed".
    """
    global mode, prev_pressed

    pressed_now = button.is_pressed

    # Detect transition: not pressed -> pressed
    if (not prev_pressed) and pressed_now:
        mode = "active" if mode == "idle" else "idle"
        print("Mode changed to:", mode)

    prev_pressed = pressed_now


def main():
    print("Pico Smart Distance Station starting...")
    print("Press the button to toggle between IDLE and ACTIVE.")
    print("Move your hand in front of the sensor to test.")

    loop_count = 0

    try:
        while True:
            loop_count += 1
            handle_button()

            if mode == "active":
                distance_cm = read_distance_cm()
                print(f"Distance: {distance_cm:.1f} cm")
            else:
                distance_cm = None  # no reading in idle

            update_lights(distance_cm)
            update_sound(distance_cm, loop_count)

            sleep(0.1)  # small delay to avoid spamming the sensor
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        status_led.off()
        rgb.off()
        speaker.off()


if __name__ == "__main__":
    main()
