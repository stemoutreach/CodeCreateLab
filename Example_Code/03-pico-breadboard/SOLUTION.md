
# Coach Solution — Pico Breadboard Lab

**Notes:**
- Debounce with `ticks_ms()`; 30–50 ms is usually enough for a clean edge.
- For PULL_UP wiring (button to GND), invert edge logic or switch to `Pin.PULL_UP` and interpret `0` as pressed.
- Mini-challenge patterns can be implemented by checking `btn.value()` inside a tight loop while pressed.
