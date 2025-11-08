
# Student Starter — Sense HAT Mission Dashboard (Advanced)

**Goal:** Multi-mode dashboard with joystick navigation, icons, and threshold colors.

## Implement
1. Replace placeholder icons with real 8×8 pixel arrays.
2. In `render()`, choose the correct icon per mode and draw with `set_pixels()`.
3. Add an overlay option: briefly show the numeric value when `show_overlay` is True.
4. Keep the loop responsive (~5–10 FPS).

## Hints
- Use `sense.low_light = True` if colors are too bright.
- For overlays, consider a short `show_message(str(value))` or draw digits on one row.
- Debounce is built into `sense.stick` events fairly well; if needed, ignore repeats quickly.
