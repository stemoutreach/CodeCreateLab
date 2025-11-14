# 02 — Sense HAT Reaction Timer Lab

> ### Quick Summary
> **Level:** 02 • **Time:** 45–70 min  
> **Audience:** Grades 6–12  
> **Prereqs:** [00 — Python Basics](../Guides/00-python-basics.md), [01 — Python Functions](../Guides/01-python-functions.md), [02 — Sense HAT Guide](../Guides/02-sense-hat.md)  
> **Hardware:** Raspberry Pi 500 + Sense HAT (Raspberry Pi OS, Thonny)  
> **You’ll practice:** LED letters/colors, timing with `time`, joystick events, low_light/clear, safe loops & cleanup, simple state machines

# Why This Matters
Fast feedback loops make you a better engineer. This lab turns your Sense HAT into a tiny **reaction‑time game** that uses **input (joystick)**, **output (LEDs/text)**, and **timing**. You’ll combine multiple skills from the Guide to build something that feels like a real product.

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

> 🆘 **Need a hint?** If you’re stuck for 5–7 minutes, open **[STUDENT_START.md](../Example_Code/02-sense-hat-reaction-timer/STUDENT_START.md)** and reveal the Full Starter to compare with your approach.

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

**Goal**  
After each reaction round, briefly show live readings for temperature (°C), humidity (%RH), and pressure (hPa) for ~5 seconds, then return to the next round.

**Inputs & Outputs**  
- Inputs: the Sense HAT environment sensors.  
- Output: scrolling text and/or a simple mini‑graph on the LED matrix that is readable and not too bright.

**Design Constraints**  
- Keep the display legible: low_light on; contrasting text/background.  
- Keep the loop responsive: don’t block forever; return control to the main game.  
- Keep it tidy: clear or restore the screen when done.

**Where this fits**  
Call your intermission right after you display the player’s time and before you clear for the next round.

**Starter Tasks (no code yet)**  
1) Time window: choose an intermission duration (e.g., 5 seconds).  
2) Reading cadence: decide how often you’ll sample sensors (e.g., 3–5 updates/sec).  
3) Rounding: choose a readable precision (e.g., 1 decimal).  
4) Order/format: decide on a short, consistent label order like “T:…  H:…  P:…”.  
5) Return path: when time is up, exit the intermission cleanly back to the game loop.

**(Optional) Smoothing**  
Sensors can jitter. Average a small number of back‑to‑back readings before you display. Keep it simple (e.g., average of 3) so updates still feel live.

**(Optional) Tiny Bar Graph**  
Turn one metric into a quick visualization: map a value range to 0–8 LEDs and fill a column/row. Pick a color per metric (e.g., blue for humidity). Remember to clear when finished.

**Pseudocode (outline only)**  
- mark when the intermission should end (now + duration)  
- until time is up:  
  - read temperature, humidity, pressure  
  - optionally smooth (average a few)  
  - build a short text string (T, H, P) and show it OR update a tiny bar graph  
  - pause briefly so the display is readable  
- tidy up (clear or restore) and hand control back to the main loop

**Test Checklist**  
- Values update several times during the intermission window.  
- Numbers are readable and use consistent units (°C, %RH, hPa).  
- Display returns to the game without leftover pixels or glare.  
- Intermission works even after many rounds (no slowdown or crash).

**Stretch Ideas**  
- Add a one‑line note when a value is unusually high/low (e.g., “Dry!”).  
- Let the player skip the intermission early with a joystick press.  
- Replace text with mini‑graphs for two metrics at once (columns vs rows).


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

---

# Next Up
Ready for breadboarding? Move on to **[03 - Pico Breadboarding](../Guides/03-pico-breadboarding.md)**.
