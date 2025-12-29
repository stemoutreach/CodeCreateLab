# PicoBot Basic Maze Solver Guide (Smooth Driving + Hysteresis)

This guide explains the **basic maze code** in `main.py` and gives ideas for improving maze solving.

**What this program does (in one sentence):**  
The robot **drives forward continuously**, and when it gets too close to an obstacle it **stops → backs up → turns right**, then **waits until it’s clearly safe** before driving forward again.

---

## Files involved

- **`main.py`** — the maze loop (your “behavior” code)
- **`picobot_lib.py`** — robot helpers (motors, ultrasonic distance, OLED)

---

## Key ideas in the code

### 1) “Smooth driving” (no jerky bursts)
Instead of driving in tiny forward steps (start/stop/start/stop), the code:

- Calls `bot.drive_forward(SPEED)` **once**
- Keeps motors running
- Only changes motion when something happens (too close / no echo)

That’s why it feels smooth.

---

### 2) A tiny “state machine”
The code uses a variable called `mode`:

- `mode = "FORWARD"` → normal driving
- `mode = "AVOID"` → we just avoided something and are waiting until it’s safe again

This is a **two-state state machine** (simple but powerful).

---

### 3) Hysteresis (two thresholds so it doesn’t “bounce”)
There are two distance thresholds:

```python
STOP_CM = 20   # too close -> avoid
GO_CM   = 25   # safe again -> go forward
```

Why two numbers?

- If you used only one threshold (ex: 20 cm), the robot might “chatter”:
  - 19.9 cm → stop
  - 20.1 cm → go
  - 19.8 cm → stop
  - repeat…

Using **STOP_CM** and **GO_CM** adds a safety buffer so it doesn’t constantly switch.

---

## Walkthrough of the maze loop (line-by-line logic)

### Startup
```python
bot.stop()
bot.set_speed(0)
show("MAZE")
time.sleep(1)
```

- Makes sure motors are off at boot
- Shows a status message on the OLED

### Begin driving forward
```python
mode = "FORWARD"
bot.drive_forward(SPEED)
```

- Starts forward motion once (smooth)

### Main loop
```python
while True:
    d = bot.distance_cm()
```

- Repeats forever
- Reads the ultrasonic distance in cm (or `None` if it can’t get a good echo)

---

## Safety: handling “no echo”
```python
if d is None:
    show("NO ECHO", None)
    bot.stop(brake=True)
    time.sleep(0.2)
    mode = "FORWARD"
    bot.drive_forward(SPEED)
    continue
```

If the sensor can’t read distance:

- Show **NO ECHO**
- Stop briefly (brake stop is more “instant”)
- Try driving forward again

**Why this helps:** if the sensor glitches, you don’t want the robot to keep blasting forward blindly.

---

## Main behavior: FORWARD → AVOID
### When moving forward
```python
if mode == "FORWARD":
    if d <= STOP_CM:
        mode = "AVOID"
        bot.stop(brake=True)
        bot.drive_back(SPEED); time.sleep(BACKUP_S); bot.stop(brake=True)
        bot.drive_right(SPEED); time.sleep(TURN_S); bot.stop(brake=True)
```

When the robot is too close (≤ `STOP_CM`):

1. **STOP** (brake)
2. **BACK** for `BACKUP_S`
3. **TURN** right for `TURN_S`
4. Switch to `mode = "AVOID"`

**Why back up first?**  
If the robot turns while still very close, it can scrape the obstacle or get stuck.

---

## AVOID mode: wait until it’s “really safe”
```python
elif mode == "AVOID":
    if d >= GO_CM:
        mode = "FORWARD"
        bot.drive_forward(SPEED)
```

In AVOID mode:

- It does **nothing fancy**—just keeps checking distance
- Only goes forward again when it’s ≥ `GO_CM`

That’s the hysteresis in action.

---

## Timing controls you can tune

```python
SPEED = 70
BACKUP_S = 0.4
TURN_S = 0.5
time.sleep(0.05)
```

- **SPEED**: motor power (0–100, but small values may not move due to deadband)
- **BACKUP_S**: how long to reverse
- **TURN_S**: how long to turn in place
- **0.05s loop delay**: how often you read the sensor

**Good tuning tip:**  
Change only ONE number at a time and test.

---

## What functions from `picobot_lib` are being used?

- `bot.drive_forward(speed)` / `bot.drive_back(speed)` / `bot.drive_right(speed)`  
  Sets motor speed + direction (non-blocking).
- `bot.stop(brake=True/False)`  
  - `brake=True`: faster stop (hard stop)
  - `brake=False`: coast (glides to a stop)
- `bot.distance_cm()`  
  Reads ultrasonic distance and returns a number (cm) or `None`.
- `bot.oled_show_status(dist=?, state=?)`  
  Shows state + distance on the OLED.

---

# Ideas to improve maze solving (student-friendly upgrades)

Below are **incremental upgrades** (start simple, then level up).

## Level 1 upgrades (easy)

### A) Turn left OR right (random choice)
Right-turn-only can get stuck in loops. Add randomness:

- Sometimes turn left, sometimes right
- Or alternate turns each time you hit a wall

**Hint idea:** keep a variable `turn_dir = 1` and flip it each avoid.

---

### B) “Clearance check” after turning
After the turn, the robot might still be facing a wall.

Add a quick check:

1. Turn
2. Read distance again
3. If still too close → turn more (or back up more)

---

### C) Speed changes based on distance
Slow down when getting close:

- Far away → faster
- Getting close → slower
- Very close → stop + avoid

This makes motion smoother and safer.

---

## Level 2 upgrades (medium)

### D) Wall following (right-hand or left-hand rule)
Classic maze method:

- Keep your right side close to the wall (right-hand rule)
- Or keep your left side close (left-hand rule)

**Problem:** With only a *front* ultrasonic sensor, you can’t truly “see” the side wall.  
But you can approximate it by doing a **tiny “peek turn”**:
- Turn slightly right, measure distance, turn back
- That’s like a quick “side scan”

---

### E) Add a “stuck detector”
Sometimes the bot can get stuck vibrating in a corner.

Example stuck signs:
- It has avoided 5 times in 5 seconds
- Distance stays under 25 cm for too long

When stuck:
- Back up longer
- Do a bigger turn (e.g., 1.0 seconds)
- Or do a 180° turn

---

## Level 3 upgrades (advanced)

### F) Choose turns based on measurements (simple “decision making”)
Instead of always turning right:

1. Stop
2. Turn right a little → measure distance
3. Turn left a little → measure distance
4. Pick the direction with more space

This is the start of “robot planning”.

---

### G) Add a second distance sensor or side sensors
For real maze navigation, add sensors:
- Front + right (or front + left)
- Or IR distance sensors on the sides

Then wall-following becomes much easier and more reliable.

---

# Debug tips

- If distance reads `None` a lot:
  - Check wiring / power
  - Ensure the sensor is pointed at a surface (soft fabrics can absorb sound)
  - Try increasing `timeout_us` or reducing `samples` in `distance_cm()`

- If the robot drifts left/right while driving forward:
  - Adjust `LEFT_TRIM` / `RIGHT_TRIM` in `picobot_lib.py`

- If it “slams” into walls:
  - Increase `STOP_CM` (stop earlier)
  - Reduce `SPEED`

---

# Student TODO ideas (copy/paste)

Add these TODOs into `main.py` for students:

- TODO 1: Make the robot turn left sometimes.
- TODO 2: If the robot gets stuck, do a bigger backup + bigger turn.
- TODO 3: Slow down when distance is under 35 cm.
- TODO 4: After turning, check distance and turn again if still too close.
- TODO 5: Try a “scan” to pick the best direction.

---

## Safety reminder
Always test the maze code:
- In a clear area first (no stairs!)
- At lower speed first (like 50–60)
- With your hand ready to stop power if needed
