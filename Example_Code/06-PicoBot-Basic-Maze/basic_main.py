# main.py (6th grade - smooth driving + hysteresis)
import time

import picobot_lib as bot
from wifi import connect_wifi

SPEED = 70

STOP_CM = 20          # if distance is <= this, we avoid
GO_CM = 25            # only start forward again when distance is >= this

BACKUP_S = 0.4
TURN_S = 0.5


def show(state, dist=None):
    bot.oled_show_status(dist=dist, state=state)


def connect_wifi_show_ip():
    show("BOOT")
    ip = connect_wifi(timeout_s=15, retries=2, status_cb=lambda m: show(m))
    if ip:
        bot.oled_set_ip(ip)
        show("ONLINE")
    else:
        show("OFFLINE")
    time.sleep(1)


def main():
    bot.stop()
    bot.set_speed(0)

    connect_wifi_show_ip()

    show("MAZE")
    time.sleep(1)

    try:
        # Start moving forward once (no burst steps)
        mode = "FORWARD"
        bot.drive_forward(SPEED)

        while True:
            d = bot.distance_cm()

            # If no reading, stop for safety
            if d is None:
                show("NO ECHO", None)
                bot.stop(brake=True)
                time.sleep(0.2)
                # Try moving forward again
                mode = "FORWARD"
                bot.drive_forward(SPEED)
                continue

            show(mode, d)

            # --- Main rule: keep moving until too close ---
            if mode == "FORWARD":
                if d <= STOP_CM:
                    mode = "AVOID"

                    show("STOP", d)
                    bot.stop(brake=True)
                    time.sleep(0.1)

                    show("BACK", d)
                    bot.drive_back(SPEED)
                    time.sleep(BACKUP_S)
                    bot.stop(brake=True)
                    time.sleep(0.1)

                    show("TURN", d)
                    bot.drive_right(SPEED)
                    time.sleep(TURN_S)
                    bot.stop(brake=True)
                    time.sleep(0.1)

                    # After turning, we don't immediately start forward unless it's "clear enough"
                    # That's the hysteresis: we wait until d >= GO_CM below.

            elif mode == "AVOID":
                # Wait until it is clearly safe before driving forward again
                if d >= GO_CM:
                    mode = "FORWARD"
                    show("FORWARD", d)
                    bot.drive_forward(SPEED)

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        bot.stop()
        bot.set_speed(0)
        show("STOPPED", None)


if __name__ == "__main__":
    main()
