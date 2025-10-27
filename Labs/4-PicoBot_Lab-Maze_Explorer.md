# 4 PicoBot Lab – Maze Explorer 🧭

Program your PicoBot to **think** its way through a cardboard maze!  
This lab uses the motors and ultrasonic‑distance code you created in the *3.0 PicoBot Guide*.  
You’ll now combine them into a smarter robot that decides when—and **where**—to turn.

---

## 🎯 Learning objectives
* Re‑use helper functions from **`robot_utils.py`**
* Measure distance on the **left, front, and right** to choose a path
* Execute ~80 ° turns for left / right decisions
* Build a main loop that keeps the robot moving until the maze is solved

---

## Prerequisites  
Complete the following
- [Python Guide](/Guides/0-Python_Guide.md)
- [Sense HAT Guide](Guides/1-SenseHat_Guide.md)
- [Pico Breadboarding Guide](/Guides/2-Pico_Breadboarding_Guide.md)
- [PicoBot Guide](Guides/3.0-PicoBot_Guide.md)

---

## 🗂 Recommended project files
```
/PicoBot/
 ├─ robot_utils.py     <- your reusable movement + sensor functions
 └─ main.py            <- *this* maze‑explorer program
```

---

## 1 · Update **`robot_utils.py`**

Add *timed* turning helpers so your main program can request an ~80° turn.

```python
# robot_utils.py  (ADD or COMPLETE these 👇)

TURN_DURATION = 0.40      # TODO: Tune until an 80 ° turn on **your** floor

def turn_left(duration: float = TURN_DURATION):
    """Spin in place to the left for *duration* seconds."""
    # TODO: Set motor pins so left wheel goes backward and right wheel forward
    #       Hint: copy your existing 'turn_left()' then add `time.sleep(duration)`
    pass

def turn_right(duration: float = TURN_DURATION):
    """Spin in place to the right for *duration* seconds."""
    # TODO: Mirror the pin logic from turn_left()
    pass
```
> **Why timed turns?**  
> Using `time.sleep()` avoids extra sensors; tune the constant until the robot turns ≈80° (slightly less than 90°) on your surface.

---

## 2 · Starter **`main.py`** (fill the To‑Dos)

```python
"""PicoBot Maze Explorer – starter code
Complete the TODO sections to finish the challenge.
"""

import time
import robot_utils

SAFE_DISTANCE = 10        # cm – adjust per maze wall spacing
TURN_DURATION = robot_utils.TURN_DURATION

def choose_direction() -> str:
    """Look left & right, return 'left' or 'right' based on **longest** clear path."""
    # TODO 1: Face LEFT (≈80°) and measure distance_left = robot_utils.read_distance()
    # TODO 2: Face RIGHT (≈160°, i.e.\ turn right *twice* TURN_DURATION) and
    #         measure distance_right
    # TODO 3: Return to ORIGINAL heading (hint: another left turn)
    # TODO 4: Decide which way to turn based on the larger distance value
    return "left"  # placeholder so the program runs

def navigate_maze():
    """Keep driving until nothing blocks the way ahead."""
    while True:
        distance_ahead = robot_utils.read_distance()

        if distance_ahead < SAFE_DISTANCE:
            # Obstacle!  Decide which side is clearer.
            robot_utils.stop_motors()
            direction = choose_direction()

            if direction == "left":
                robot_utils.turn_left(TURN_DURATION)
            else:
                robot_utils.turn_right(TURN_DURATION)
        else:
            robot_utils.move_forward()

        time.sleep(0.05)

if __name__ == "__main__":
    try:
        navigate_maze()
    finally:
        robot_utils.stop_motors()
```

### 🧩 Your To‑Dos, step‑by‑step
1. **Tune `TURN_DURATION`** in `robot_utils.py` until a single call rotates ~80 °.
2. **Implement `choose_direction()`** so the robot:
   * Looks left, records the distance.
   * Looks right, records the distance.
   * Faces forward again.
   * Chooses the side with the **longer** distance.
3. Test in an open area first, then in the maze.

---

## 3 · Stretch goals
* Use **three** ultrasonic sensors for simultaneous left/center/right readings.
* Add a finish‑line **light or sound** when the robot exits the maze.
* Implement **PID** control to keep a fixed distance from the left wall (“wall follower”).

---

## ✅ Submission checklist
* `robot_utils.py` contains **working** movement + sensor helpers.
* `main.py` successfully explores the maze without manual touches.
* You’ve answered:
  * How did you tune the turn angle?
  * What strategy does your `choose_direction()` use when distances tie?

Good luck,<br>
**– Your Code & Create Lab Coaches** 🚀
