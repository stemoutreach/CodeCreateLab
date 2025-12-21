# wifi.py
import network
import time
from wifi_config import SSID, PASSWORD

def connect_wifi():
    """Connect Pico 2 W to WiFi (station/client mode). Return IP string or None."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)

        max_wait = 15
        while max_wait > 0 and not wlan.isconnected():
            print("  waiting...", max_wait)
            max_wait -= 1
            time.sleep(1)

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print("Connected! IP:", ip)
        return ip

    print("WiFi connection failed.")
    return None