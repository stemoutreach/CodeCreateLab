# 02 — Sense HAT Reaction Timer — STUDENT_START

These hints nudge you forward without giving away the full code. Try them in order.

## Part A — Reaction Timer (Core)

### 1) Timer accuracy
Your `start = time()` should happen **immediately after** you flip the screen to GO (green). If you start earlier, you’ll accidentally include drawing/scrolling time in the score.

### 2) Debounce the joystick
Only count the **first** middle press in your loop. Ignore `"held"` and `"released"` actions. A tiny sleep (≈10–20 ms) in your polling loop helps avoid busy‑waiting.

### 3) High score
Initialize `best_ms` to `None`. When you finish a round:
- If `best_ms` is `None` or the new value is smaller, update it.
- When showing the score, show the number first (e.g., `235 ms`), then a small celebration (✓ flash) if it’s a new best.

### 4) Loop structure
Use a **main guard** and a `try/finally` to ensure `sense.clear()` always runs, even if you press Stop in Thonny. Keep your round logic in a `while True:` loop.

---

## Optional Part B — Sensor Intermission (Temp • Humidity • Pressure)

After you display a player’s time, briefly show the environment readings. Do this **without** blocking your game forever.

### What to design (no code here—write your own!)
- **Duration:** Choose how long the intermission runs (e.g., 5 s).  
- **Update rate:** Decide how often you refresh readings (e.g., 3–5 times per second).  
- **Precision:** Pick a consistent number of decimals to display (often 1).  
- **Format:** Decide on a compact, readable label order like `T:…  H:…  P:…`.  
- **Exit:** Make sure the intermission ends on time and returns to the main loop.  

### Smoothing (optional)
Average a **few** back‑to‑back readings before displaying to reduce jitter. Keep it light so values still feel “live.”

### Tiny bar‑graph (optional)
Convert one metric into a quick LED bar: map the metric’s range to **0–8** LEDs high or wide. Choose readable colors and clear the display when done.

### Where to call it
Right after you show the round’s score and before you clear/reset for the next round.

---

## Quick self‑check
- Does the timer start exactly when the GO screen appears?  
- Do you get only **one** press per round?  
- Does your score show in **milliseconds** as an integer?  
- Does your code always **clear** the LEDs on exit?  
- If you built Part B, does it return to the game cleanly without leftover pixels?
