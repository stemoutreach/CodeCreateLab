# advanced_main.py
# PicoBot Maze Starter (ADVANCED - smooth driving, not jerky)
#
# Files expected on the Pico:
#   - picobot_lib.py      (motors + ultrasonic + OLED)
#   - wifi.py             (connect_wifi helper)
#   - wifi_config.py      (SSID/PASSWORD)  <-- student edits, do not commit
#   - ssd1306.py          (OLED driver)

import time
import picobot_lib as bot
from wifi import connect_wifi


# ============================================================
# WiFi + OLED status hook
# ============================================================

def oled_status(msg: str):
    bot.oled_show_status(dist=None, state=msg)


def connect_and_show_ip():
    bot.oled_show_status(dist=None, state="BOOT")
    time.sleep(0.4)

    ip = connect_wifi(timeout_s=15, retries=2, status_cb=oled_status)
    if ip:
        bot.oled_set_ip(ip)
        bot.oled_show_status(dist=None, state="ONLINE")
        time.sleep(1)
    else:
        bot.oled_show_status(dist=None, state="OFFLINE")
        time.sleep(1)

    return ip


# ============================================================
# MAZE TUNING
# ============================================================

SPEED = 70

STOP_CM = 20     # if distance <= STOP_CM, do an avoid maneuver
GO_CM   = 25     # only go forward again when distance >= GO_CM (hysteresis)

# Maneuver times (seconds)
BACKUP_S = 0.35
TURN_S   = 0.50

BRAKE_STOP = True

ACTION_FORWARD = "FORWARD"
ACTION_STOP    = "STOP"
ACTION_AVOID   = "AVOID"   # (recommended) triggers the default backup+turn maneuver


def read_distance():
    return bot.distance_cm()


def choose_action(distance_cm: float):
    """
    TODO (STUDENT): Decide what to do based on distance.

    Keep it simple at first:
      - If no reading -> STOP
      - If far enough (>= GO_CM) -> FORWARD
      - If too close (<= STOP_CM) -> AVOID

    You can get more advanced later:
      - change GO_CM/STOP_CM
      - decide LEFT vs RIGHT turns based on memory
      - count bumps / blocked events
    """
    if distance_cm is None:
        return ACTION_STOP

    # Hysteresis-friendly logic:
    if distance_cm <= STOP_CM:
        return ACTION_AVOID

    if distance_cm >= GO_CM:
        return ACTION_FORWARD

    # In the gray zone between STOP_CM and GO_CM,
    # keep doing whatever we were already doing (handled in the loop).
    return None


# ============================================================
# Smooth motion controller (no start/stop jitter)
# ============================================================

_current_motion = None  # what motors are currently doing: FORWARD/STOP/etc.

def set_motion(motion: str):
    """Only change motors if motion actually changed."""
    global _current_motion
    if motion == _current_motion:
        return

    if motion == ACTION_FORWARD:
        bot.oled_show_status(dist=None, state="FORWARD")
        bot.drive_forward(SPEED)
    elif motion == ACTION_STOP:
        bot.oled_show_status(dist=None, state="STOP")
        bot.stop(brake=BRAKE_STOP)
    else:
        # Any other motion types can be added later
        bot.stop(brake=BRAKE_STOP)

    _current_motion = motion


def do_avoid_maneuver(last_dist):
    """
    Default avoid maneuver:
      STOP -> BACKUP -> TURN RIGHT -> (then return to loop)
    Students can modify this later.
    """
    bot.oled_show_status(dist=last_dist, state="STOP")
    bot.stop(brake=True)
    time.sleep(0.10)

    bot.oled_show_status(dist=last_dist, state="BACK")
    bot.drive_back(SPEED)
    time.sleep(BACKUP_S)
    bot.stop(brake=True)
    time.sleep(0.10)

    bot.oled_show_status(dist=last_dist, state="TURN R")
    bot.drive_right(SPEED)
    time.sleep(TURN_S)
    bot.stop(brake=True)
    time.sleep(0.10)

    # After avoid, we dont force forward immediatelyloop will re-check distance.
    global _current_motion
    _current_motion = None  # force next set_motion() to re-apply


def run_maze():
    """
    Smooth loop:
      - Forward stays ON while safe
      - Avoid maneuver runs only when too close
      - Hysteresis reduces flip-flop
    """
    bot.oled_show_status(dist=None, state="MAZE")
    time.sleep(1)

    # start stopped; loop will decide when to move
    set_motion(ACTION_STOP)

    last_mode = ACTION_STOP

    while True:
        d = read_distance()

        # OLED always shows distance + current mode
        label = last_mode if last_mode else "RUN"
        bot.oled_show_status(dist=d, state=label)

        # Extra safety: super close = hard stop
        if d is not None and d <= 8:
            last_mode = ACTION_STOP
            set_motion(ACTION_STOP)
            time.sleep(0.2)
            continue

        action = choose_action(d)

        # If choose_action returns None, stay in the same mode (smooth)
        if action is None:
            time.sleep(0.05)
            continue

        if action == ACTION_STOP:
            last_mode = ACTION_STOP
            set_motion(ACTION_STOP)

        elif action == ACTION_FORWARD:
            last_mode = ACTION_FORWARD
            set_motion(ACTION_FORWARD)  # continuous, no stop/start

        elif action == ACTION_AVOID:
            last_mode = ACTION_AVOID
            do_avoid_maneuver(d)

        time.sleep(0.05)


def main():
    try:
        bot.stop(brake=False)
        bot.set_speed(0)

        connect_and_show_ip()
        run_maze()

    except KeyboardInterrupt:
        pass
    finally:
        bot.stop(brake=False)
        bot.set_speed(0)
        bot.oled_show_status(dist=None, state="STOPPED")


if __name__ == "__main__":
    main()
