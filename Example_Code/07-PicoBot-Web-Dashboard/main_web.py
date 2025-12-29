# main_web.py
# PicoBot Web Control Launcher
#
# Files expected on the Pico:
#   - picobot_lib.py
#   - wifi.py
#   - wifi_config.py        (student edits; do not commit)
#   - picobot_web_dashboard.py
#   - ssd1306.py
#
# What it does:
#   1) Connects to WiFi
#   2) Shows IP on OLED (if OLED is present)
#   3) Starts the web dashboard server

import time

import picobot_lib as bot
from wifi import connect_wifi
import picobot_web_dashboard as dash


def oled_status(msg: str):
    # Short messages so they fit on OLED
    bot.oled_show_status(dist=None, state=msg)


def main():
    # Safe startup
    bot.stop(brake=False)
    bot.set_speed(0)
    bot.oled_show_status(dist=None, state="BOOT")
    time.sleep(0.5)

    # Connect WiFi
    ip = connect_wifi(timeout_s=15, retries=3, status_cb=oled_status)

    if not ip:
        # If WiFi fails, show message and stop. (Could also retry forever.)
        bot.oled_show_status(dist=None, state="NO WIFI")
        print("WiFi failed. Check wifi_config.py SSID/PASSWORD.")
        while True:
            time.sleep(5)

    # Show IP and start dashboard
    bot.oled_set_ip(ip)
    bot.oled_show_status(dist=None, state="DASHBOARD")
    time.sleep(1)

    print("Starting PicoBot Web Dashboard at http://%s/" % ip)
    dash.run_server(ip)


if __name__ == "__main__":
    main()
