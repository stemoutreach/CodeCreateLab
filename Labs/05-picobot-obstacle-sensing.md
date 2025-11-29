# 05 — PicoBot Obstacle Sensing & Maze Explorer

> ### Quick Summary
> **Level:** 05 • **Time:** 45–60 min  
> **Prereqs:**  
> - [Guide: 03 — Pico Breadboarding](../Guides/03-pico-breadboarding.md)  
> - [Guide: 04 — PicoBot (Drive with L298N)](../Guides/04-picobot.md)  
> - [Guide: 05 — PicoBot Sensors: Start Button, Distance, Lights & Sound](../Guides/05-picobot-sensors-guide.md)  
> - [Lab: 04 — PicoBot Drive Basics](./04-picobot-drive-basics.md)  
> **Hardware:** PicoBot (Pico + L298N + motors), HC-SR04P, start button, RGB LED, speaker, maze walls  
> **You’ll practice:** tuning turn timing, using distance bands, writing a simple state machine, choosing turns, testing & refining robot behavior  

# Why This Matters

In the Guides, you **Learned & Tried** how to drive the PicoBot, read distance, and show states with LED and sound. In this Lab, you move to **Do**: turning those pieces into a robot that can **explore a simple maze on its own**, deciding when to go forward, when to turn, and what to do at dead ends. That “sense → decide → act” loop is the heart of real-world robot navigation.

---

# What You’ll Build

You’ll create a **Maze Explorer program** for PicoBot:

- Press the **start button** → PicoBot begins exploring the maze.  
- While the path ahead is clear, it **drives forward**.  
- When it detects a wall, it **decides** whether to turn **left or right** (or turn around in a dead end).  
- The **RGB LED** and **speaker** show what the robot is thinking (idle, driving, blocked, turning, stuck).  

The final artifact is a single `.py` file that can run on the PicoBot and handle a **simple maze of 90° turns**.

---

# Outcomes

By the end you can:

- Use **ultrasonic distance** and thresholds to control robot movement in a maze.  
- Tune **time-based 90° turns** using speed and timing constants.  
- Implement a tiny **state machine** for robot behaviors (`idle`, `drive_forward`, `decide_turn`, `turn`, `dead_end`).  
- Explain and test a **turn policy** (always-left or “look left / look right”).  

---

# Setup

- Hardware: **Raspberry Pi 500** running Raspberry Pi OS, plus your **PicoBot** wired as in Guides 04 and 05 (L298N, button, RGB LED, HC-SR04P, speaker).  
- Software: **Thonny IDE** with **MicroPython (Raspberry Pi Pico)** selected as the interpreter.  

Quick run steps:

1. Open **Thonny** on the Raspberry Pi 500.  
2. Set interpreter: `Tools → Options → Interpreter → MicroPython (Raspberry Pi Pico)`.  
3. Plug in the Pico over USB.  
4. Create a new file in `~/Documents/CodeCreate/` called, for example:  
   `picobot_maze_explorer.py`  
5. Save it **on the Pico** when ready to test.  
6. Click **Run ▶** and watch the Shell for debug prints while the robot drives.

You may also re-use your existing drive helper file (e.g. `picobot_drive.py`) from the previous Guide/Lab.

---

# Steps

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/05-picobot-obstacle-sensing/STUDENT_START.md)**.

## 1) Plan (2–3 min)

Before coding, decide:

- **Maze rules**:  
  - Will you use an **always-left rule**? (Try left; if blocked, try right; if both blocked, turn around.)  
  - Or will you **look left vs right** and choose the side with **greater distance**?
- **Distance thresholds** (rough draft):  
  - `SAFE_DISTANCE` (cm): okay to keep driving forward.  
  - `WALL_TOO_CLOSE` (cm): must stop and decide to turn.
- **States** (start with at least):  
  - `idle`  
  - `drive_forward`  
  - `decide_turn`  
  - `turning_left` / `turning_right`  
  - `turn_around` (dead end)
- **Feedback**:  
  - Which RGB colors and sounds signal each state?

Write your decisions at the top of your file as comments (this helps you and your partner “debug the idea” before debugging code).

---

## 2) Build / Prep (3–5 min)

- Double-check your **wiring** matches the 05 Guide for:
  - Ultrasonic sensor (HC-SR04P) → powered from **3V3(OUT)**, not 5 V.  
  - Button → `GP16` + GND.  
  - RGB LED → `GP17, GP18, GP19` + common GND.  
  - Speaker → `GP20` + GND.  
- Confirm your **drive helpers** work:
  - `forward()`, `back()`, `stop()`, `set_speed(percent)` from `picobot_drive.py`.
- Create a **simple maze**:
  - Use boxes, books, or wall pieces to form a few straight corridors and 90° turns.  
  - Leave enough room so the robot can move without scraping both sides.

Quick sanity test: run a tiny script that sets `set_speed(60)` and calls `forward()` for 1 second, then `stop()`. Make sure the robot moves straight.

---

## 3) Code (8–12 min)

In this step you’ll build the **structure** of your maze explorer but **leave some logic as TODOs**.

Suggested structure:

- Import your libraries (`picozero`, `time`) and your drive helpers.  
- Set up devices: `Button`, `RGBLED`, `DistanceSensor`, `Speaker`.  
- Define constants: `SAFE_DISTANCE`, `WALL_TOO_CLOSE`, `TURN_SPEED`, `TURN_90_TIME`.  
- Write **helper functions**:
  - `update_rgb_for_mode(mode)`  
  - `handle_button(mode)`  
  - `do_turn_left()` / `do_turn_right()`  
  - `do_turn_around()`  
- Write a `main_loop()` that:
  - Uses a `mode` variable.  
  - Reads distance.  
  - Decides when to switch between states.

Here’s a **partial structure** to help you start (do NOT copy-paste your full solution here—add your logic and keep TODOs):

```python
from time import sleep
from picozero import Button, RGBLED, DistanceSensor, Speaker

from picobot_drive import forward, back, stop, set_speed

# --- devices ---
button = Button(16)
rgb = RGBLED(red=17, green=18, blue=19)
sensor = DistanceSensor(echo=11, trigger=10)
speaker = Speaker(20)

# --- tuning constants (adjust in testing) ---
SAFE_DISTANCE = 40      # TODO: tune for your maze
WALL_TOO_CLOSE = 18     # TODO: tune so you don't hit walls
TURN_SPEED = 60
TURN_90_TIME = 0.5      # TODO: calibrate for ~90 degrees

mode = "idle"           # idle, drive_forward, decide_turn, turning, turn_around

def update_rgb_for_mode(current_mode):
    """Set LED color based on state."""
    if current_mode == "idle":
        rgb.color = (0, 0, 1)    # blue
    elif current_mode == "drive_forward":
        rgb.color = (0, 1, 0)    # green
    elif current_mode == "decide_turn":
        rgb.color = (1, 1, 0)    # yellow
    elif current_mode in ("turning", "turn_around"):
        rgb.color = (1, 0.5, 0)  # orange
    else:
        rgb.off()                # fallback

def handle_button(current_mode):
    """Toggle between idle and exploring when button is pressed."""
    # TODO: if button is pressed while idle, switch to drive_forward
    # TODO: if button is pressed while exploring, go back to idle + stop
    return current_mode

def do_turn_left():
    """Turn left ~90 degrees using time + speed."""
    # TODO: set speed and spin wheels so robot turns left ~90 degrees
    # Hint: one wheel forward, the other backward, for TURN_90_TIME

def do_turn_right():
    """Turn right ~90 degrees using time + speed."""
    # TODO: mirror your left turn logic

def do_turn_around():
    """Turn around (~180 degrees) for dead ends."""
    # TODO: you can either do two left turns or one longer turn

def main_loop():
    global mode
    set_speed(TURN_SPEED)
    while True:
        mode = handle_button(mode)
        update_rgb_for_mode(mode)

        # TODO: read distance in cm
        # d_cm = ...

        if mode == "idle":
            stop()
            speaker.off()

        elif mode == "drive_forward":
            # TODO: drive forward while distance >= SAFE_DISTANCE
            # TODO: if distance < WALL_TOO_CLOSE, stop and switch to decide_turn
            pass

        elif mode == "decide_turn":
            # TODO: choose a direction (always-left or "look left/right")
            # TODO: switch mode to a turning mode (e.g. "turning")
            pass

        elif mode == "turning":
            # TODO: perform left/right/around turn, then go back to drive_forward
            pass

        sleep(0.05)

try:
    main_loop()
except KeyboardInterrupt:
    print("Stopping robot.")
finally:
    stop()
    rgb.off()
    speaker.off()
```

Your job in this step is to **fill in the TODOs** and wire your plan from Step 1 into real behavior.

---

## 4) Discovery (checklist + pseudocode) (8–12 min)

Now you’ll refine your logic **on paper first** before editing code again.

**Checklist**

- [ ] I have chosen a **turn policy** (always-left OR look left/right).  
- [ ] I can explain when my robot should **switch states** (idle → drive_forward → decide_turn → turning → drive_forward).  
- [ ] I know what happens in a **dead end**.  
- [ ] I’ve thought about how my robot **avoids hitting the wall** (threshold values).  
- [ ] I have a plan for **90° turn timing** (how I will test and tune `TURN_90_TIME`).  

**Pseudocode (guide, not code)**

Use this to talk through your idea with a partner or mentor:

```text
on start:
    mode = "idle"

loop forever:
    if button pressed:
        toggle between idle and exploring

    if mode == "idle":
        stop motors
        set LED to idle color

    else:
        read distance d_cm

        if mode == "drive_forward":
            if d_cm >= SAFE_DISTANCE:
                drive forward
            else:
                stop
                mode = "decide_turn"

        else if mode == "decide_turn":
            choose turn_direction (left/right/turn_around)
                using chosen policy:
                    - always-left: try left, else right, else around
                    - or compare "free space" on left vs right
            mode = "turning"

        else if mode == "turning":
            perform the turn based on turn_direction
            mode = "drive_forward"
```

You can add **extra lines** for dead-end detection, stuck detection, or a “finished” state if your maze has a clear exit.

---

## 5) Test (3–5 min)

Time to see what the robot actually does.

- Run your program with the robot in the **start position**.  
- Watch for:
  - Does it start on **button press**?  
  - Does it **drive straight** when the corridor is clear?  
  - Does it **stop** before touching the wall?  
  - Does it **turn consistently** (about 90°) at each decision point?  
  - Do LED colors and sounds match what you think the robot is doing?

Use print statements (e.g. `print(mode, d_cm)`) in Thonny’s Shell to see what’s happening in the decision loop.

---

## 6) Iterate (2–3 min)

Pick **one** thing to improve, adjust, and test again:

- Tune `SAFE_DISTANCE` and `WALL_TOO_CLOSE` so you don’t get too close, but also don’t stop too early.  
- Adjust `TURN_90_TIME` so your turns are closer to 90°.  
- Make your **LED colors** and beeps clearer (e.g., short beep for normal turns, longer beep for dead ends).  
- If the robot often ends up **stuck** (repeating the same moves), add a simple “I’m stuck” state that flashes red and stops.

Repeat small tweaks until the behavior is reliable enough for a demo.

---

# Skeleton Starter (start here)

Use this minimal starter if your file got too messy or you want a clean base. You still need to fill in the TODOs—this is **not** a full solution.

```python
from time import sleep
from picozero import Button, RGBLED, DistanceSensor, Speaker
from picobot_drive import forward, back, stop, set_speed

button = Button(16)
rgb = RGBLED(red=17, green=18, blue=19)
sensor = DistanceSensor(echo=11, trigger=10)
speaker = Speaker(20)

SAFE_DISTANCE = 40       # TODO: tune after testing
WALL_TOO_CLOSE = 18      # TODO: tune after testing
TURN_SPEED = 60
TURN_90_TIME = 0.5       # TODO: calibrate 90-degree turn

mode = "idle"
turn_direction = "left"  # could be "left", "right", or "around"

def update_rgb_for_mode(current_mode):
    # TODO: choose colors for idle / drive_forward / decide_turn / turning
    pass

def handle_button(current_mode):
    # TODO: toggle between idle and drive_forward when button is pressed
    return current_mode

def do_turn_left():
    # TODO: use TURN_SPEED and TURN_90_TIME to turn left
    pass

def do_turn_right():
    # TODO: mirror left turn for right side
    pass

def do_turn_around():
    # TODO: either two left turns or a single longer spin
    pass

def main_loop():
    global mode, turn_direction
    set_speed(TURN_SPEED)

    while True:
        mode = handle_button(mode)
        update_rgb_for_mode(mode)

        # TODO: read distance in cm
        # d_cm = ...

        if mode == "idle":
            stop()
            speaker.off()

        elif mode == "drive_forward":
            # TODO: drive while safe, otherwise switch to decide_turn
            pass

        elif mode == "decide_turn":
            # TODO: apply your maze rule to set turn_direction
            # (always-left OR look-left/look-right)
            # then set mode = "turning"
            pass

        elif mode == "turning":
            # TODO: call do_turn_left/right/around based on turn_direction
            # then go back to drive_forward
            pass

        sleep(0.05)

try:
    main_loop()
except KeyboardInterrupt:
    print("Stopping robot.")
finally:
    stop()
    rgb.off()
    speaker.off()
```

---

# Submission / Demo Checklist

- [ ] Button press starts the robot exploring from **idle**.  
- [ ] Robot drives forward while the path ahead is **clear**.  
- [ ] Robot **stops before hitting** a wall and chooses a new direction.  
- [ ] Robot can handle at least **one left/right turn** in your maze without help.  
- [ ] RGB LED and speaker reflect different states (idle vs exploring vs turning).  
- [ ] Program exits cleanly (motors off, LED off) when stopped from Thonny.

---

# Extensions (choose one)

- **Left-hand rule upgrade:**  
  Add a simple “left-hand on the wall” policy: if left is open, always go left first; if not, try forward; if not, try right; otherwise turn around.

- **Look-before-you-turn:**  
  Implement “look left/ right” using your existing front sensor and turning logic: briefly turn left to measure distance, then right, then choose the better direction.

- **Stuck detector:**  
  If the robot makes more than **N decisions** in a short time without moving far, enter a “stuck” state: flash red and beep, then stop.

- **Exit celebration:**  
  If you define an “exit zone,” detect it (e.g., distance suddenly very large or a special marker) and play a celebration sequence with LED + sound.

---

# Troubleshooting

- **Symptom:** Robot doesn’t start moving when button is pressed.  
  → **Likely cause:** `handle_button()` never changes `mode` from `"idle"` to `"drive_forward"`.  
  → **Fix:** Add `print()`s inside `handle_button()` to confirm it sees button presses and updates `mode`.

- **Symptom:** Robot hits the wall before turning.  
  → **Likely cause:** `WALL_TOO_CLOSE` is too small or distance readings are noisy.  
  → **Fix:** Increase `WALL_TOO_CLOSE` and test again; ensure HC-SR04P is powered from **3V3(OUT)** and aimed correctly.

- **Symptom:** Turns are not 90° (too short or too long).  
  → **Likely cause:** `TURN_90_TIME` not tuned for your surface and battery level.  
  → **Fix:** Run a tiny test script that only does `do_turn_left()` and adjust `TURN_90_TIME` until it looks close to 90°.

- **Symptom:** Robot spins in place, never going forward.  
  → **Likely cause:** Logic keeps switching back into `decide_turn` or `turning` because distance is always considered “too close.”  
  → **Fix:** Print `d_cm` values, adjust `SAFE_DISTANCE` and `WALL_TOO_CLOSE`, and check that your maze leaves some clear space.

- **Symptom:** Robot keeps moving after you stop the program in Thonny.  
  → **Likely cause:** No cleanup in `finally:` block.  
  → **Fix:** Make sure you have `finally: stop(); rgb.off(); speaker.off()` as in the starter.

---

# Reflection (1–2 sentences)

- What did you learn about connecting **sensor readings** to **movement decisions**?  
- If you had one more hour, what’s the **next improvement** you would make to your maze explorer?

---

# Next Up

In the next Guide/Lab, you’ll build on this maze explorer by making your robot’s behavior **more robust and predictable**—for example, tracking its turns, logging its path, or using more advanced maze-solving strategies.
