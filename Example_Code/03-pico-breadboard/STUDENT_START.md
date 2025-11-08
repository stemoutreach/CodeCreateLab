
# Student Starter — Pico Breadboard Lab

**Goal:** Debounced button input drives LED behavior. Optional buzzer/RGB patterns.

## Implement
1. Wire LED (GP15) and button (GP14 with PULL_DOWN or PULL_UP wiring).
2. Complete `read_button_debounced()` and verify single press/release events.
3. Implement `blink()` and the mini-challenge behavior (fast while held, slow 3× on release).

## Tips
- For `PULL_UP` wiring (button to GND), pressed reads `0`; invert logic.
- Use `ticks_ms()`/`ticks_diff()` for debounce timing (~30 ms).
