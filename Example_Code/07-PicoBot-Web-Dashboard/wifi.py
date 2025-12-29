# wifi.py
import time
import network

def connect_wifi(
    ssid=None,
    password=None,
    timeout_s=15,
    retries=2,
    status_cb=None,
    return_wlan=False
):
    """
    Connect Pico W / Pico 2 W to WiFi (station/client mode).

    Args:
        ssid/password: Optional. If not provided, loads from wifi_config.py
        timeout_s: Seconds to wait per attempt
        retries: Number of attempts
        status_cb: Optional callback like status_cb(message: str)
        return_wlan: If True, returns (ip, wlan). Else returns ip.

    Returns:
        ip string if connected, else None (or (ip, wlan) if return_wlan=True)
    """
    # Load credentials from wifi_config.py if not provided
    if ssid is None or password is None:
        try:
            from wifi_config import SSID, PASSWORD  # student file
            ssid = SSID if ssid is None else ssid
            password = PASSWORD if password is None else password
        except Exception as e:
            if status_cb:
                status_cb("wifi_config missing")
            print("ERROR: wifi_config.py missing or invalid:", e)
            return (None, None) if return_wlan else None

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Already connected?
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        if status_cb:
            status_cb("WiFi already on")
        print("WiFi already connected. IP:", ip)
        return (ip, wlan) if return_wlan else ip

    for attempt in range(1, retries + 1):
        if status_cb:
            status_cb(f"WiFi connect {attempt}/{retries}")
        print(f"Connecting to WiFi (attempt {attempt}/{retries})...")

        try:
            wlan.connect(ssid, password)
        except Exception as e:
            print("wlan.connect error:", e)
            time.sleep(1)
            continue

        # Wait up to timeout_s
        start = time.ticks_ms()
        while not wlan.isconnected():
            elapsed_s = time.ticks_diff(time.ticks_ms(), start) / 1000

            if elapsed_s >= timeout_s:
                break

            if status_cb:
                # Short message; keep OLED-friendly
                status_cb(f"WiFi... {int(timeout_s - elapsed_s)}s")
            time.sleep(1)

        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            if status_cb:
                status_cb("WiFi connected")
            print("Connected! IP:", ip)
            return (ip, wlan) if return_wlan else ip

        # Not connected this attempt
        if status_cb:
            status_cb("WiFi failed")
        print("WiFi connect attempt failed.")
        try:
            wlan.disconnect()
        except Exception:
            pass
        time.sleep(1)

    print("WiFi connection failed after retries.")
    return (None, wlan) if return_wlan else None
