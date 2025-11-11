# 02 — Sense HAT Reaction Timer (Standalone Lab)

> ### Quick Summary
> **Level:** 02 • **Time:** 45–70 min  
> **Audience:** Grades 6–12  
> **Prereqs:** [00 — Python Basics](../Guides/00-python-basics.md), [01 — Python Functions](../Guides/01-python-functions.md), [02 — Sense HAT Guide](../Guides/02-sense-hat.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT (Raspberry Pi OS, Thonny)  
> **You’ll practice:** LED letters/colors, timing with `time`, joystick events, low_light/clear, safe loops & cleanup, simple state machines

# Why This Matters
Fast feedback loops make you a better engineer. This lab turns your Sense HAT into a tiny **reaction‑time game** that uses **input (joystick)**, **output (LEDs/text)**, and **timing**. You’ll combine multiple skills from the Guide to build something that feels like a real product.

---

# Standalone Setup & Checks
If this is your **only Sense HAT lab**, complete these quick checks first.

## Install & Import Check (2–3 min)
Create and run this tiny script in Thonny to confirm your Sense HAT works:
```python
from sense_hat import SenseHat
s = SenseHat()
s.low_light = True
s.clear(0, 20, 0)   # soft green
s.show_letter("✓")
```
If you see a green screen and a ✓, you’re good. Press **Stop** in Thonny, then add:
```python
s.clear()
```

## Mini Warm‑Ups (5–8 min)
1) **Color fill**: show **navy** background for 1 sec, then **clear**.  
2) **Letters**: cycle `["R","G","B"]` with different `text_colour`.  
3) **Joystick read**: print a line when **middle** is pressed.

```python
from sense_hat import SenseHat
from time import sleep
s = SenseHat(); s.low_light = True
s.clear(0,0,30); sleep(1); s.clear()
s.show_letter("R", text_colour=(255,0,0)); sleep(0.6)
s.show_letter("G", text_colour=(0,255,0)); sleep(0.6)
s.show_letter("B", text_colour=(0,0,255)); sleep(0.6); s.clear()
print("Press middle to continue…")
while True:
    for e in s.stick.get_events():
        if e.action == "pressed" and e.direction == "middle":
            print("Pressed!"); s.clear(); raise SystemExit
    sleep(0.01)
```

---

# What You’ll Build
A one‑button reaction game:
- Screen shows **“Ready”** → waits a **random** 1–3 seconds
- Matrix turns **green** (“GO!”)
- You press the **middle** joystick quickly
- The game displays your time in **milliseconds**
- Keeps track of a **best time (high score)** during the session

---

# Outcomes
By the end you can:
- Handle joystick events and debounce to capture a **single press**
- Use **timers** (`time.time()` / `sleep`) to measure milliseconds
- Display **letters/icons** and use **low_light** and **clear** safely
- Structure code with a simple **state machine** and **main‑guard**

---

# Steps

> 🆘 **Need a hint?** Open: `../Example_Code/02-sense-hat-reaction-timer/STUDENT_START.md`

## 1) Plan (2–3 min)
Sketch the game loop:
- Show “Ready” → wait a random delay → show green screen “GO”
- Start timer when green is shown; stop when **middle** is pressed
- Compute `elapsed_ms`, show it, update **best** if smaller
- After 2 seconds, reset to “Ready” and repeat

## 2) Build / Prep (3–5 min)
- Seat the Sense HAT firmly on the Pi.  
- Set **low_light** to true to reduce glare.  
- Decide on colors you’ll use for **waiting**, **go**, **error**, and **best** display.

## 3) Code (10–15 min)

### Skeleton Starter (start here)
Create `reaction_timer.py` and complete the **TODOs**:

```python
from sense_hat import SenseHat
from time import sleep, time
import random

# Colors (tweak to taste)
BLACK  = (0, 0, 0)
NAVY   = (0, 0, 30)
GREEN  = (0, 150, 0)
RED    = (180, 0, 0)
WHITE  = (255, 255, 255)

def show_ready(sense):
    sense.clear(NAVY)
    sense.show_message("Ready", scroll_speed=0.06, text_colour=WHITE, back_colour=NAVY)

def show_go(sense):
    sense.clear(GREEN)
    sense.show_letter("G", text_colour=WHITE, back_colour=GREEN)

def show_score(sense, ms, best_ms):
    # TODO: show the last time (e.g., "245 ms") then flash a ✓ if it's a new best
    pass

def wait_for_middle_press(sense):
    """Block until the joystick middle is pressed; return when it happens."""
    while True:
        for e in sense.stick.get_events():
            if e.action == "pressed" and e.direction == "middle":
                return
        sleep(0.01)

def main():
    sense = SenseHat()
    sense.low_light = True
    best_ms = None
    try:
        while True:
            show_ready(sense)
            # TODO: choose a random delay between 1.0 and 3.0 seconds
            # TODO: sleep for that delay, then call show_go(sense)
            start = time()  # TODO: move to the right place so timing is accurate
            wait_for_middle_press(sense)
            elapsed_ms = int((time() - start) * 1000)

            # TODO: update best_ms if None or elapsed_ms < best_ms
            # TODO: call show_score(sense, elapsed_ms, best_ms)

            # Small pause before next round
            sleep(1.2)
            sense.clear()
    finally:
        sense.clear()

if __name__ == "__main__":
    main()
```

## 4) Discovery (checklist + pseudocode) (8–12 min)
**Checklist**
- [ ] `low_light` reduces glare  
- [ ] Random delay uses `random.uniform(1.0, 3.0)` or `randint(10,30)/10`  
- [ ] Timer starts **exactly when** the screen turns green  
- [ ] Only the **first** middle press counts (no double triggers)  
- [ ] Show time as **`123 ms`** (integer)  
- [ ] Keep and display **best** time; celebrate with ✓

**Pseudocode**
```
loop forever:
  show_ready()
  delay = random between 1 and 3 seconds
  sleep(delay)
  show_go()
  start = now()
  wait for middle press
  elapsed_ms = (now() - start) * 1000
  if best is None or elapsed_ms < best:
      best = elapsed_ms
  show_score(elapsed_ms, best)
  short sleep
  clear
```

## 5) Test (5–8 min)
- Try multiple rounds; verify times look reasonable (200–500 ms is typical).  
- Confirm a **new best** triggers your celebration (✓, color change, etc.).  
- Press the **Stop** button in Thonny: LEDs should **clear** (cleanup).

## 6) Iterate (3–5 min)
- Improve the look and feel: fonts/colors/speeds.  
- Reduce accidental presses (e.g., ignore `"held"` or second presses).  
- Add a tiny intro (“Rdy?”, “3‑2‑1…”) if you have time.

---

# Extensions (choose one)
1) **False Start** — If the middle is pressed **before** GO, show a red “!” and restart the round.  
2) **Three‑Round Average** — Track last 3 results and display average.  
3) **Two‑Player** — Left press = Player A, Right press = Player B; display both times and who won.

---

# Optional Part B — Sensor Intermission (Temp • Humidity • Pressure)

If this is your **only** Sense HAT lab and you want to use the **environment sensors** from the Guide, add this intermission after each round.

## Goal
After showing a player's reaction time, display live readings for **temperature (°C)**, **humidity (%RH)**, and **pressure (hPa)** for ~5 seconds.

## Starter Snippet
```python
def show_env_intermission(sense, seconds=5):
    import time
    end = time.time() + seconds
    while time.time() < end:
        t = round(sense.get_temperature(), 1)
        h = round(sense.get_humidity(), 1)
        p = round(sense.get_pressure(), 1)
        sense.show_message(f"T:{t}C H:{h}% P:{p}h", scroll_speed=0.05, text_colour=(200,200,200))
```

**Where to call it:** right after `show_score(...)` in your main loop:
```python
show_score(sense, elapsed_ms, best_ms)
show_env_intermission(sense, seconds=5)  # <- add this
```

## (Optional) Smoothing
Sensor readings can jump around. Average a few samples:
```python
def avg3(a, b, c): return round((a+b+c)/3, 1)

def read_env_avg(sense):
    t = avg3(sense.get_temperature(), sense.get_temperature(), sense.get_temperature())
    h = avg3(sense.get_humidity(),    sense.get_humidity(),    sense.get_humidity())
    p = avg3(sense.get_pressure(),    sense.get_pressure(),    sense.get_pressure())
    return t, h, p
```

Then in your intermission loop, call `read_env_avg(sense)` and display those values.

## (Optional) Tiny Bar Graph
Turn readings into a quick bar graph (see Guide §8):
- Map **humidity** 0–100% to 0–8 LEDs high.
- Use **blue** bars for humidity, **green** rows for pressure, etc.
- Keep a dark background and clear on exit.


---

# Troubleshooting
- **Nothing on LEDs** → Ensure the HAT is seated; try `sense.clear()` at the start.  
- **High brightness** → Set `sense.low_light = True`.  
- **No joystick events** → Keep your loop running; check that you read only `"pressed"`.  
- **Weird times** → Make sure you set `start = time()` *right after* GO is shown.  
- **Crash on exit** → Wrap the loop in `try/finally` and call `sense.clear()`.

---

# Rubric (for coaches)
- **Complete (Meets)** — All items in Submission Checklist demonstrated; code readable with functions and cleanup.  
- **Strong (Exceeds)** — Extensions implemented cleanly; thoughtful UI (colors, pacing), comments, and small refactors (e.g., state enum).  
- **Developing (Partially Meets)** — Core loop works but timing off, or missing best‑time tracking/cleanup.  
- **Not Yet** — Does not run or missing major checklist items.
