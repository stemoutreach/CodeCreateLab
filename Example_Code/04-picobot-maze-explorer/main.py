
"""
PicoBot Maze Explorer — main.py
Navigate forward; when blocked, back up and turn.
Stretch: look around to pick the clearer side.
"""
import time
import robot_utils as ru

def look_around_choose() -> str:
    """Return 'left' or 'right' by sampling distances with a quick look-around."""
    # Look LEFT
    ru.turn_left(ru.TURN_DURATION)        # face left
    time.sleep(0.05)
    left = ru.read_distance_cm() or 0.0

    # Look RIGHT (from facing-left, two rights = ~180° to face right)
    ru.turn_right(ru.TURN_DURATION)       # face forward
    ru.turn_right(ru.TURN_DURATION)       # face right
    time.sleep(0.05)
    right = ru.read_distance_cm() or 0.0

    # Return to FORWARD (from facing-right, one left)
    ru.turn_left(ru.TURN_DURATION)

    return 'left' if left >= right else 'right'

def navigate():
    try:
        while True:
            d = ru.read_distance_cm()
            if d is None:
                # Sensor hiccup; stop briefly
                ru.stop_motors()
                time.sleep(0.1)
                continue

            if d < ru.SAFE_DISTANCE:
                # Blocked — back up & choose a side
                ru.stop_motors()
                ru.move_backward()
                time.sleep(ru.BACKUP_DURATION)
                ru.stop_motors()

                direction = look_around_choose()
                if direction == 'left':
                    ru.turn_left(ru.TURN_DURATION)
                else:
                    ru.turn_right(ru.TURN_DURATION)
            else:
                ru.move_forward()

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        ru.stop_motors()

if __name__ == '__main__':
    navigate()
