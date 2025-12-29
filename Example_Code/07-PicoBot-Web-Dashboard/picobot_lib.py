# picobot-lib.py  (NOTE: if you want to IMPORT this file, rename to picobot_lib.py)
# PicoBot library: L298N motors (PWM speed) + HC-SR04P ultrasonic (3.3V) + SSD1306 OLED
#
# - Drive functions are NON-BLOCKING (no sleep inside)
# - Ultrasonic returns distance in cm (float) or None on failure
# - OLED shows distance + state; later you can add WiFi IP via oled_set_ip("x.x.x.x")

from machine import Pin, PWM, I2C
import time

# Best/fastest echo timing helper (available on Pico MicroPython)
try:
    from machine import time_pulse_us
except ImportError:
    time_pulse_us = None

# OLED library (make sure ssd1306.py is on the Pico filesystem)
try:
    import ssd1306
except ImportError:
    ssd1306 = None


# ============================================================
# Motor + L298N
# ============================================================

# === L298N pin mapping ===
IN1 = Pin(6, Pin.OUT)   # Left motor direction
IN2 = Pin(7, Pin.OUT)
IN3 = Pin(4, Pin.OUT)   # Right motor direction
IN4 = Pin(3, Pin.OUT)

ENA = PWM(Pin(8))       # Left enable (PWM)
ENB = PWM(Pin(2))       # Right enable (PWM)
ENA.freq(1000)
ENB.freq(1000)

# --- Defaults / tuning ---
DEFAULT_SPEED = 100      # drive_forward() uses this
MIN_SPEED = 30           # deadband: motors often won't spin below this
LEFT_TRIM = 1.00         # tweak to drive straighter (e.g., 0.95)
RIGHT_TRIM = 1.00

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def set_speed(percent: int):
    """Set speed for both motors (deadband + trim). percent: 0..100"""
    p = _clamp(int(percent), 0, 100)
    if p != 0 and p < MIN_SPEED:
        p = MIN_SPEED

    left = _clamp(int(p * LEFT_TRIM), 0, 100)
    right = _clamp(int(p * RIGHT_TRIM), 0, 100)

    ENA.duty_u16(int(left / 100 * 65535))
    ENB.duty_u16(int(right / 100 * 65535))

# --- Direction only (no sleeping here) ---
def forward_dir():
    IN1.value(1); IN2.value(0)
    IN3.value(1); IN4.value(0)

def back_dir():
    IN1.value(0); IN2.value(1)
    IN3.value(0); IN4.value(1)

def left_dir():
    # turn left in place
    IN1.value(0); IN2.value(1)   # left backward
    IN3.value(1); IN4.value(0)   # right forward

def right_dir():
    # turn right in place
    IN1.value(1); IN2.value(0)   # left forward
    IN3.value(0); IN4.value(1)   # right backward

def stop_coast():
    # Coast: all inputs low
    IN1.value(0); IN2.value(0); IN3.value(0); IN4.value(0)

def stop_brake():
    # Brake: all inputs high
    IN1.value(1); IN2.value(1); IN3.value(1); IN4.value(1)

# --- Student-friendly drive API (speed defaults to max) ---
def drive_forward(speed: int = DEFAULT_SPEED):
    set_speed(speed)
    forward_dir()

def drive_back(speed: int = DEFAULT_SPEED):
    set_speed(speed)
    back_dir()

def drive_left(speed: int = DEFAULT_SPEED):
    set_speed(speed)
    left_dir()

def drive_right(speed: int = DEFAULT_SPEED):
    set_speed(speed)
    right_dir()

def stop(brake: bool = False):
    stop_brake() if brake else stop_coast()


# ============================================================
# Ultrasonic (HC-SR04P) — Powered at 3.3V
# ============================================================
# Because Vcc is 3.3V, ECHO is ~3.3V (Pico-safe).
# If you ever power from 5V, you MUST level-shift ECHO.

ULTRA_TRIG_PIN = 10
ULTRA_ECHO_PIN = 11

_trig = Pin(ULTRA_TRIG_PIN, Pin.OUT)
_echo = Pin(ULTRA_ECHO_PIN, Pin.IN)

def _pulse_us_manual(pin, level, timeout_us=30000):
    """
    Fallback pulse measurement if time_pulse_us isn't available.
    Returns pulse duration in microseconds, or -1 on timeout.
    """
    start = time.ticks_us()

    # Ensure clean start: wait while already at requested level
    while pin.value() == level:
        if time.ticks_diff(time.ticks_us(), start) > timeout_us:
            return -1

    # Wait for pulse start
    while pin.value() != level:
        if time.ticks_diff(time.ticks_us(), start) > timeout_us:
            return -1

    pulse_start = time.ticks_us()

    # Wait for pulse end
    while pin.value() == level:
        if time.ticks_diff(time.ticks_us(), pulse_start) > timeout_us:
            return -1

    return time.ticks_diff(time.ticks_us(), pulse_start)

def distance_cm(timeout_us=30000, samples=3, settle_ms=10):
    """
    Measure distance in centimeters.
    Returns:
      float distance_cm, or None if failed (no echo / timeout).
    """
    readings = []

    for _ in range(max(1, samples)):
        # Trigger: LOW -> HIGH 10us -> LOW
        _trig.value(0)
        time.sleep_us(2)
        _trig.value(1)
        time.sleep_us(10)
        _trig.value(0)

        # Measure echo HIGH pulse width
        if time_pulse_us:
            dur = time_pulse_us(_echo, 1, timeout_us)  # microseconds
        else:
            dur = _pulse_us_manual(_echo, 1, timeout_us)

        # dur <= 0 indicates timeout or error
        if dur and dur > 0:
            # Convert to cm: approx dur / 58.3
            readings.append(dur / 58.3)

        time.sleep_ms(settle_ms)

    if not readings:
        return None

    readings.sort()
    return readings[len(readings) // 2]  # median-ish


# ============================================================
# OLED (SSD1306 128x64 I2C) on I2C0: SDA=GP0, SCL=GP1
# ============================================================

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1

_oled = None
_oled_ip = None

def oled_init():
    """Initialize OLED if ssd1306 is available. Safe to call multiple times."""
    global _oled
    if _oled is not None:
        return
    if ssd1306 is None:
        return  # library missing
    try:
        i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
        _oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    except Exception:
        _oled = None

def oled_set_ip(ip_str):
    """Store IP to display later (call this when WiFi is added)."""
    global _oled_ip
    _oled_ip = ip_str

def oled_show_status(dist=None, state="READY", ip=None):
    """
    Display status:
      - dist: float in cm or None
      - state: short string (FORWARD/STOP/etc.)
      - ip: optional override; if None uses stored _oled_ip
    """
    oled_init()
    if _oled is None:
        return  # no OLED available

    show_ip = ip if ip is not None else _oled_ip

    _oled.fill(0)
    _oled.text("PicoBot", 0, 0)

    _oled.text("State:", 0, 16)
    _oled.text(state[:10], 54, 16)

    if dist is None:
        _oled.text("Dist: --.- cm", 0, 32)
    else:
        _oled.text("Dist:", 0, 32)
        _oled.text("{:5.1f} cm".format(dist), 48, 32)

    if show_ip:
        _oled.text("IP:", 0, 48)
        _oled.text(str(show_ip)[:16], 24, 48)
    else:
        _oled.text("IP: offline", 0, 48)

    _oled.show()


# ============================================================
# Demo / test harness
# ============================================================

def demo_basic_moves():
    """Motor-only test sequence (no sensors)."""
    print("\n=== Basic Motor Test ===")
    print("Tip: lift wheels for the first test. Ctrl+C to stop.\n")
    oled_show_status(dist=None, state="MOTOR TEST")

    try:
        print("Forward 60%")
        oled_show_status(dist=None, state="FWD 60")
        drive_forward(60); time.sleep(1.0); stop(); time.sleep(0.4)

        print("Back 60%")
        oled_show_status(dist=None, state="BACK 60")
        drive_back(60); time.sleep(0.8); stop(); time.sleep(0.4)

        print("Left 60%")
        oled_show_status(dist=None, state="LEFT 60")
        drive_left(60); time.sleep(0.5); stop(); time.sleep(0.4)

        print("Right 60%")
        oled_show_status(dist=None, state="RIGHT60")
        drive_right(60); time.sleep(0.5); stop(); time.sleep(0.4)

        print("Coast vs Brake stop demo...")
        print("  Forward then COAST stop")
        oled_show_status(dist=None, state="COAST")
        drive_forward(60); time.sleep(0.8); stop(brake=False); time.sleep(0.6)

        print("  Forward then BRAKE stop")
        oled_show_status(dist=None, state="BRAKE")
        drive_forward(60); time.sleep(0.8); stop(brake=True); time.sleep(0.6)

        oled_show_status(dist=None, state="DONE")
        print("Basic motor test done.\n")
    except KeyboardInterrupt:
        print("\nInterrupted!")
    finally:
        stop(brake=False)
        set_speed(0)

def demo_ultrasonic_readings(seconds=8, period_s=0.25):
    """Print ultrasonic distance readings and show on OLED."""
    print("\n=== Ultrasonic Reading Test ===")
    print("Hold your hand in front of the sensor and watch the values.")
    print("Ctrl+C to stop.\n")

    start = time.ticks_ms()
    try:
        while time.ticks_diff(time.ticks_ms(), start) < int(seconds * 1000):
            d = distance_cm()
            if d is None:
                print("Distance: -- (no echo)")
                oled_show_status(dist=None, state="NO ECHO")
            else:
                print("Distance: {:5.1f} cm".format(d))
                oled_show_status(dist=d, state="SENSE")
            time.sleep(period_s)
        print("Ultrasonic reading test done.\n")
    except KeyboardInterrupt:
        print("\nInterrupted!")

def demo_ultrasonic_avoidance(
    speed=60,
    stop_cm=20,
    backup_s=0.4,
    turn_s=0.5,
    brake_stop=True,
    loop_delay_s=0.05
):
    """
    Drive forward until distance <= stop_cm,
    then stop, back up briefly, turn right, and continue.
    """
    print("\n=== Ultrasonic Drive Demo ===")
    print("Robot drives until obstacle, then back up + turn.")
    print("Ctrl+C to stop.\n")

    stop(brake=False)
    set_speed(0)
    time.sleep(0.5)

    try:
        while True:
            d = distance_cm()

            if d is None:
                print("Distance: -- (no echo) -> stopping briefly")
                oled_show_status(dist=None, state="NO ECHO")
                stop(brake=brake_stop)
                time.sleep(0.2)
                continue

            print("Distance: {:5.1f} cm".format(d))

            if d <= stop_cm:
                oled_show_status(dist=d, state="STOP")
                stop(brake=brake_stop)
                time.sleep(0.1)

                oled_show_status(dist=d, state="BACK")
                drive_back(speed)
                time.sleep(backup_s)
                stop(brake=brake_stop)
                time.sleep(0.1)

                oled_show_status(dist=d, state="TURN R")
                drive_right(speed)
                time.sleep(turn_s)
                stop(brake=brake_stop)
                time.sleep(0.1)
            else:
                oled_show_status(dist=d, state="FORWARD")
                drive_forward(speed)

            time.sleep(loop_delay_s)

    except KeyboardInterrupt:
        print("\nInterrupted!")
    finally:
        stop(brake=False)
        set_speed(0)
        oled_show_status(dist=None, state="STOPPED")
        print("Motors stopped.")

def main():
    """
    Runs BOTH motor and ultrasonic tests.
    Later, when WiFi is added, call oled_set_ip(ip_string) after connecting.
    """
    try:
        oled_show_status(dist=None, state="START")

        # 1) Motor test
        demo_basic_moves()

        # 2) Ultrasonic sensor test (prints + OLED)
        demo_ultrasonic_readings(seconds=8, period_s=0.25)

        # 3) Full drive test using ultrasonic gating
        # Start in a safe area (or lift wheels first).
        demo_ultrasonic_avoidance(speed=60, stop_cm=20)

    except KeyboardInterrupt:
        print("\nMain interrupted!")
    finally:
        stop(brake=False)
        set_speed(0)

if __name__ == "__main__":
    main()
