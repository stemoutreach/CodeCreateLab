# main.py
from wifi import connect_wifi
from oled_status import show_wifi_ip, show_distance
from web_dashboard import run_server

def main():
    ip = connect_wifi()
    if not ip:
        return

    show_wifi_ip(ip)
    # Replace "Waiting for web..." with a distance placeholder immediately
    show_distance(None, active=False)

    run_server(ip)

if __name__ == "__main__":
    main()
